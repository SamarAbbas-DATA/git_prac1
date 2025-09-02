from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from datetime import datetime

from blog.schemas import Blog
from blog.database import collection
router = APIRouter( prefix='/blogs', tags = ['blogs'])


# read all func 
@router.get("",response_model=List[Blog])
def get_blogs():
    blogs = list(collection.find({}, {"_id": 0}))
    return blogs

# read by title func
@router.get("/get", response_model=List[Blog])
def search_blog(title: str = Query(..., description="enter title")):
    blg = list(collection.find({"title": title}, {"_id": 0}))
    if not blg:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blg

# CREATE
@router.post("")
def create_blog(blog: Blog):
    blog_dict = blog.dict()
    blog_dict["created_at"] = datetime.utcnow()
    result = collection.insert_one(blog_dict)
    # Keep return shape consistent with your current code
    blog_dict["_id"] = str(result.inserted_id)
    return blog_dict

# UPDATE — /blogs/update
@router.put("/update")
def update_blog(
    old_title: str = Query(..., description="Current title"),
    new_title: Optional[str] = None,
    new_content: Optional[str] = None,
):
    update_data = {}
    if new_title:
        update_data["title"] = new_title
    if new_content:
        update_data["content"] = new_content

    if not update_data:
        raise HTTPException(status_code=400, detail="No new data provided")

    result = collection.update_one({"title": old_title}, {"$set": update_data})

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Blog not found")

    return {"msg": f"Blog '{old_title}' updated", "new_data": update_data}

# DELETE — /blogs/delete
@router.delete("/delete")
def delete_blog(title: str = Query(..., description="Title to delete")):
    result = collection.delete_one({"title": title})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Blog not found")
    return {"msg": f"Blog with title '{title}' deleted"}