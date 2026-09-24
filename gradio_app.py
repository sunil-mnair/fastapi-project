import gradio as gr
import requests

USERS_API_URL = "http://127.0.0.1:8000/users"

auth_token = None

def api_error(response):
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        return {"status_code": response.status_code, "detail": response.text}


def login_user(email,password):
    global auth_token
    response = requests.post(
        "http://127.0.0.1:8000/users/login",
        json={
            "email": email,
            "password": password
        }
    )

    data = response.json()
    if "access_token" in data:
        auth_token = data["access_token"]

    return data

def get_profile():

    global auth_token

    response = requests.get(
        "http://127.0.0.1:8000/users/profile",

        headers={
            "Authorization":
                f"Bearer {auth_token}"
        }
    )

    return response.json()

def ask_a_openai(prompt):
    response = requests.post(
        "http://127.0.0.1:8000/chatbot/chat",
        json={"prompt": prompt},
        headers={
            "Authorization":
                f"Bearer {auth_token}"
        }
    )
    return response.json()

def create_user(name, email, age, phone, password):
    if age is None:
        return {"detail": "Age is required."}
    user_data = {"name": name, "email": email, "age": int(age), "phone": phone or None,"password": password} 
    try:
        response = requests.post(USERS_API_URL, json=user_data, timeout=10)
        return response.json() if response.ok else api_error(response)
    except requests.RequestException as error:
        return {"detail": f"Could not connect to FastAPI: {error}"}

def list_users(search, page, limit):
    params = {"page": int(page), "limit": int(limit)}
    if search and search.strip():
        params["search"] = search.strip()
    try:
        response = requests.get(USERS_API_URL, params=params, timeout=10)
        return response.json() if response.ok else api_error(response)
    except requests.RequestException as error:
        return {"detail": f"Could not connect to FastAPI: {error}"}

def get_user_by_id(user_id):
    if user_id is None:
        return {"detail": "User ID is required."}
    try:
        response = requests.get(f"{USERS_API_URL}/{int(user_id)}", timeout=10)
        return response.json() if response.ok else api_error(response)
    except requests.RequestException as error:
        return {"detail": f"Could not connect to FastAPI: {error}"}

def ask_assistant(
    question,
    model
):
    response = requests.post(
    "http://127.0.0.1:8000/assistant",

    json={
        "question":
            question,

        "model":
            model
    }
)

    return response.json()

with gr.Blocks(title="FastAPI User Management") as demo:
    gr.Markdown("# FastAPI User Management")
    gr.Markdown("This Gradio application communicates with the FastAPI User API.")
    with gr.Tab("Login"):

        email_input = gr.Textbox(
            label="Email"
        )

        password_input = gr.Textbox(
            label="Password",
            type="password"
        )

        login_button = gr.Button(
            "Login"
        )

        login_output = gr.JSON()

        login_button.click(
            fn=login_user,
            inputs=[
                email_input,
                password_input
            ],
            outputs=login_output
        )
    with gr.Tab("Profile"):
        profile_button = gr.Button(
            "Get Profile"
        )

        profile_output = gr.JSON()

        profile_button.click(
            fn=get_profile,
            outputs=profile_output
        )

    with gr.Tab("Create User"):
        create_name = gr.Textbox(label="Name")
        create_email = gr.Textbox(label="Email")
        create_age = gr.Number(label="Age", minimum=1, maximum=119)
        create_phone = gr.Textbox(label="Phone", placeholder="Optional")
        create_password = gr.Textbox(label="Password", type="password") 
        create_button = gr.Button("Create User")
        create_output = gr.JSON(label="API Response")
        create_button.click(fn=create_user, inputs=[create_name, create_email, create_age, create_phone, create_password], outputs=create_output)
    with gr.Tab("List and Search Users"):
        search_input = gr.Textbox(label="Search", placeholder="Search by name or email")
        page_input = gr.Number(label="Page", value=1, minimum=1)
        limit_input = gr.Number(label="Page Size", value=10, minimum=1, maximum=100)
        list_button = gr.Button("Get Users")
        list_output = gr.JSON(label="Users")
        list_button.click(fn=list_users, inputs=[search_input, page_input, limit_input], outputs=list_output)
    with gr.Tab("Get User by ID"):
        user_id_input = gr.Number(label="User ID", minimum=1)
        get_button = gr.Button("Get User")
        user_output = gr.JSON(label="User")
        get_button.click(fn=get_user_by_id, inputs=user_id_input, outputs=user_output)
    with gr.Tab("Chat with OpenAI"):
        prompt_input = gr.Textbox(label="Prompt")
        chat_button = gr.Button("Ask OpenAI")
        chat_output = gr.JSON(label="Response")
        chat_button.click(fn=ask_a_openai, inputs=[prompt_input], outputs=chat_output)
    with gr.Tab("Business Assistant"):
        question_input = gr.Textbox(
            label="Question"
        )
        model_dropdown = gr.Dropdown(
            [
                "OpenAI",
                "Claude"
            ],

            value="OpenAI",

            label="Model"
        )
        ask_button = gr.Button(
            "Ask"
        )
        answer_output = gr.JSON(label="Answer")

        ask_button.click(
        fn=ask_assistant,

        inputs=[
            question_input,
            model_dropdown
        ],

        outputs=answer_output
    )


if __name__ == "__main__":
    demo.launch()
