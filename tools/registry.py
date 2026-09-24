from tools.user_tools import (
    get_application_name,
    list_users,
    get_user,
    list_uploaded_files
)

TOOLS = {
    "get_application_name":
        get_application_name,

    "list_users":
        list_users,

    "get_user":
        get_user,

    "list_uploaded_files":
        list_uploaded_files
}


# Execute a Tool by Name
def execute_tool(
    tool_name,
    **kwargs
):
    # Search for the Tool
    tool = TOOLS.get(
        tool_name
    )
 
    # Validate 
    if not tool:

        return {
            "error":
                "Unknown tool"
        }

    return tool(
        **kwargs
    )
