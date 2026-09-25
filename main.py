from fastapi import FastAPI
from routers.users import router as users_router
from routers.clients import router as clients_router
from routers.upload import router as upload_router
from routers.chatbot import router as chatbot_router
from routers.assistant import router as assistant_router

import gradio as gr
from gradio_app import demo

app = FastAPI()

app.include_router(users_router)
app.include_router(clients_router)
app.include_router(upload_router)
app.include_router(chatbot_router)
app.include_router(assistant_router)

from database.database import Base, engine
Base.metadata.create_all(bind=engine)


app = gr.mount_gradio_app(app, demo, "/gradio")





