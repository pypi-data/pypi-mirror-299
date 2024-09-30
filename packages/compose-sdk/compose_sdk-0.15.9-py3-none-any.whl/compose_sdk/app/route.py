# A completely made up suffix that we use to make sure our autogenerated
# routes don't conflict with user-provided routes.
AUTOGEN_SUFFIX = "1nt3rn$$l-aaut0geN"


def auto_generate_route(name: str) -> str:
    dashed = name.replace(" ", "-")
    return f"{dashed}-{AUTOGEN_SUFFIX}"
