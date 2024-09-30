from typing import Dict, List, Set, TypedDict, Union
import importlib.metadata
from .api import ApiHandler
from .scheduler import Scheduler
from .app import AppDefinition, AppRunner, PageParams
from .core import EventType

# get package version
try:
    package_version = importlib.metadata.version(__package__)
except importlib.metadata.PackageNotFoundError:
    package_version = None

package_name = "compose-python"


class Theme(TypedDict):
    text_color: str
    background_color: str
    primary_color: str


def ensure_unique_routes(apps: List[AppDefinition]) -> None:
    """
    Ensures that all routes are unique. Edits the apps in place and does not
    return anything.

    :param apps: The apps to ensure uniqueness for.
    """
    routes: Set[str] = set()

    for app in apps:
        if app.route in routes:
            if not app.is_auto_generated_route:
                raise ValueError(f"Duplicate route: {app.route}")
            else:
                # If an auto-generated route conflicts with an existing route,
                # we'll just append a random string to the end of the auto-generated
                # route to make it unique.
                new_route_name = f"{app.route}7"
                app.set_route(new_route_name, True)

        routes.add(app.route)


def get_apps_by_route(apps: List[AppDefinition]) -> Dict[str, AppDefinition]:
    return {app.route: app for app in apps}


def camelCaseTheme(theme: Theme):
    return {
        "textColor": theme["text_color"],
        "backgroundColor": theme["background_color"],
        "primaryColor": theme["primary_color"],
    }


class ComposeClient:
    def __init__(
        self,
        *,
        api_key: str,
        apps: List[AppDefinition] = [],
        theme: Union[Theme, None] = None,
        DANGEROUS_ENABLE_DEV_MODE: bool = False,
    ):
        if api_key is None:  # type: ignore
            raise ValueError("Missing 'api_key' field in Compose.Client constructor")

        if apps is None:  # type: ignore
            raise ValueError(
                "Missing 'apps' field in Compose.Client constructor. If you don't "
                "want to pass any apps, you can pass an empty list."
            )

        if theme is not None:
            required_keys = ["primary_color", "text_color", "background_color"]
            for key in required_keys:
                if key not in theme:
                    raise ValueError(
                        f"Missing '{key}' in theme. All of {required_keys} are required."
                    )
                if (
                    not isinstance(theme[key], str)
                    or not theme[key].startswith("#")
                    or len(theme[key]) != 7
                ):
                    raise ValueError(
                        f"Invalid hex color for '{key}'. It should be a string starting with '#' followed by 6 hexadecimal characters."
                    )

        self.theme = theme
        self.api_key = api_key
        self.is_development = DANGEROUS_ENABLE_DEV_MODE

        ensure_unique_routes(apps)
        self.app_definitions = get_apps_by_route(apps)

        self.scheduler = Scheduler()

        self.api = ApiHandler(
            self.scheduler,
            self.is_development,
            self.api_key,
            package_name,
            package_version,
        )
        self.app_runners: Dict[str, AppRunner] = {}

    def connect(self) -> None:
        self.scheduler.initialize(True)
        self.__connect_ws()

    def connect_async(self) -> None:
        self.scheduler.initialize(False)
        self.__connect_ws()

    def __connect_ws(self) -> None:
        self.api.add_listener(
            "browser-listener",
            lambda event: self.scheduler.create_task(self.handle_browser_event(event)),
        )

        self.api.connect(
            {
                "type": EventType.SdkToServer.INITIALIZE,
                "apps": self.summarize_apps(),
                "theme": camelCaseTheme(self.theme) if self.theme is not None else None,
                "packageVersion": package_version,
                "packageName": package_name,
            }
        )

    def summarize_apps(self) -> List[Dict]:
        return [
            app_definition.summarize()
            for app_definition in self.app_definitions.values()
        ]

    async def handle_browser_event(self, event: Dict) -> None:
        if event["type"] == EventType.ServerToSdk.START_EXECUTION:
            await self.execute_app(
                event["appRoute"],
                event["executionId"],
                event["sessionId"],
                event["params"],
            )
            return

        if event["type"] == EventType.ServerToSdk.CHECK_EXECUTION_EXISTS:
            exists = event["executionId"] in self.app_runners

            if not exists:
                await self.api.send(
                    {
                        "type": EventType.SdkToServer.EXECUTION_EXISTS_RESPONSE,
                        "executionId": event["executionId"],
                        "exists": exists,
                    },
                    event["sessionId"],
                )

            return

        runner = self.app_runners.get(event["executionId"])

        if runner is None:
            return

        elif event["type"] == EventType.ServerToSdk.FILE_TRANSFER:
            runner.on_file_transfer(event["fileId"], event["fileContents"])

        if event["type"] == EventType.ServerToSdk.ON_CLICK_HOOK:
            await runner.on_click_hook(event["componentId"], event["renderId"])

        elif event["type"] == EventType.ServerToSdk.ON_SUBMIT_FORM_HOOK:
            await runner.on_submit_form_hook(
                event["formComponentId"], event["renderId"], event["formData"]
            )

        elif (
            event["type"] == EventType.ServerToSdk.ON_ENTER_HOOK
            or event["type"] == EventType.ServerToSdk.ON_SELECT_HOOK
            or event["type"] == EventType.ServerToSdk.ON_FILE_CHANGE_HOOK
        ):
            await runner.on_input_hook(
                event["type"], event["componentId"], event["renderId"], event["value"]
            )

        elif event["type"] == EventType.ServerToSdk.ON_TABLE_ROW_ACTION_HOOK:
            await runner.on_table_row_action_hook(
                event["componentId"],
                event["renderId"],
                event["actionIdx"],
                event["value"],
            )

        elif event["type"] == EventType.ServerToSdk.ON_CONFIRM_RESPONSE_HOOK:
            await runner.on_confirm_response_hook(
                event["componentId"], event["response"]
            )

    async def execute_app(
        self,
        app_route: str,
        execution_id: str,
        browser_session_id: str,
        params: PageParams,
    ) -> None:
        if app_route not in self.app_definitions:
            return

        app_definition = self.app_definitions[app_route]

        runner = AppRunner(
            self.scheduler, self.api, app_definition, execution_id, browser_session_id
        )

        self.scheduler.create_task(runner.execute(params))

        self.app_runners[execution_id] = runner
