from mcp.server.mcp import MCPServer

from tools.user_tools import (
    get_application_name,
    get_user,
    list_users,
    list_uploaded_files
)


mcp = MCPServer(
    "FastAPI Tutorial Server"
)


@mcp.tool(description="Get the application name")
def application_name():
    return get_application_name()

@mcp.tool(description="List all uploaded files")
def uploaded_files():
    return list_uploaded_files()

@mcp.tool(description="List all users")
def users():
    return list_users()

@mcp.tool(description="Get a specific user by ID")
def user(user_id:int):
    return get_user(user_id)

if __name__ == "__main__":
    mcp.run()

