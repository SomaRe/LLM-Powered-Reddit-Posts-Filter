from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from database import get_all_posts

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    posts = get_all_posts()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "posts": posts
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)