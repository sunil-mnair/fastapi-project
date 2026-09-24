import json

from openai import OpenAI

from config.settings import (
    OPENAI_API_KEY
)

from tools.registry import (
    execute_tool
)


# OpenAI Client
client = OpenAI(
    api_key=OPENAI_API_KEY
)

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_application_name",
            "description": "Get the application name.",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_users",
            "description": "List all users.",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_user",
            "description": "Get a user by numeric ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The user's ID.",
                    }
                },
                "required": ["user_id"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_uploaded_files",
            "description": "List all uploaded files.",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        },
    },
]


# Chat Function
def ask_openai(prompt: str):
    messages = [{"role": "user", "content": prompt}]

    while True:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )
        message = response.choices[0].message

        if not message.tool_calls:
            return message.content

        messages.append(message.model_dump(exclude_none=True))
        for tool_call in message.tool_calls:
            arguments = json.loads(tool_call.function.arguments or "{}")
            result = execute_tool(tool_call.function.name, **arguments)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result),
                }
            )

