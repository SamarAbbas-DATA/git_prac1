from fastapi import FastAPI 
from pydantic import BaseModel

app = FastAPI()

class Blog(BaseModel):
    title: str
    content: str

@app.get('/blog')
def get(abc: str = None):
    return {"message": f"No blog title provided {abc}"}


@app.post('/blog')
def post_blog(blog: Blog):
    return {"message": "Blog posted successfully", "blog": blog}

