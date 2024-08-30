import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

app = FastAPI()

IMAGES_DIR = "media"

templates = Jinja2Templates(directory="templates")

app.mount("/media", StaticFiles(directory="media"), name="media")
app.mount("/static", StaticFiles(directory="templates"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    folders = []
    for folder_name in os.listdir("media"):
        folder_path = os.path.join("media", folder_name)
        if os.path.isdir(folder_path):
            files = os.listdir(folder_path)
            file_info = []
            for file in files:
                file_path = os.path.join(folder_path, file)
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    file_info.append({'name': file, 'type': 'image'})
                elif file.lower().endswith(('.mp4', '.avi', '.mov')):
                    file_info.append({'name': file, 'type': 'video'})
                else:
                    file_info.append({'name': file, 'type': 'unknown'})
            folders.append({
                "name": folder_name,
                "files": file_info
            })

    folders.sort(key=lambda x: int(x["name"]))

    return templates.TemplateResponse("index.html", {"request": request, "folders": folders})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
