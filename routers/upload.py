from importlib.metadata import files
import os
from fastapi import APIRouter, HTTPException, File, UploadFile

import httpx

router = APIRouter(tags=["Upload"], prefix="/upload")

ALLOWED_EXTENSIONS = [
    ".pdf",
    ".docx",
    ".xlsx",
    ".csv"
]

@router.get("/quote")
async def quote():

    async with httpx.AsyncClient() as client:

        response = await client.get(
            "https://echoes.soferity.com/api/quotes"
        )

        return response.json()


#EndPoint to Upload Files
@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    filename = file.filename.lower()

    if not any(
        filename.endswith(ext)
        for ext
        in ALLOWED_EXTENSIONS
    ):
        raise HTTPException(
            status_code=400,
            detail="File type not allowed"
        )


    filepath = os.path.join(
        "uploads",
        file.filename
    )

    with open(
        filepath,
        "wb"
    ) as buffer:

        content = await file.read()

        buffer.write(content)

    return {
        "message":
            "File uploaded",

        "filename":
            file.filename
    }

@router.get("/files")
def get_files():
    files = os.listdir("uploads")
    return {"files": files}
