from fastapi import FastAPI , Depends
from blog.schemas import Blog , User
from blog.database import collection , collection2
from typing import List
from fastapi import Query
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime , timedelta
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi.security import OAuth2PasswordBearer               
from blog.auth import create_access_token, verify_token, ACCESS_TOKEN_EXPIRE_MINUTES
from routers.blogs import router as blog_router



app = FastAPI()

app.include_router(blog_router)

'''
# func to create blog
@app.post("/blog")
def create_blog(blog: Blog):
    blog_dict = blog.dict()
    blog_dict['created_at'] = datetime.utcnow()
    result = collection.insert_one(blog_dict)
    blog_dict["_id"] = str(result.inserted_id)
    return blog_dict



# func to show all blogs
@app.get("/blogs",response_model=List[Blog])
def get_blogs():
    blogs = list(collection.find({}, {"_id": 0}))
    return blogs
# func to search blog by title
@app.get('/blogs/get' , response_model=List[Blog])
def search_blog(title: str = Query(..., description ='enter title')):
    blg = list(collection.find({"title":title}, {"_id": 0}))
    if not blg:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blg


# DELETE func
@app.delete("/blogs/delete")
def delete_blog(title: str = Query(..., description="Title to delete")):
    result = collection.delete_one({"title": title})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Blog not found")
    return {"msg": f"Blog with title '{title}' deleted"}

#  UPDATE function
@app.put("/blogs/update")
def update_blog(
    old_title: str = Query(..., description="Current title"),
    new_title: str | None = None,
    new_content: str | None = None
):
    update_data = {}
    if new_title: 
        update_data["title"] = new_title
    if new_content: 
        update_data["content"] = new_content

    if not update_data:
        raise HTTPException(status_code=400, detail="No new data provided")

    result = collection.update_one(
        {"title": old_title},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Blog not found")

    return {"msg": f"Blog '{old_title}' updated", "new_data": update_data}
'''
pwd_contex = CryptContext(schemes =['bcrypt'], deprecated = 'auto')

# creating user 
@app.post('/users')
async def create_user(user :User):
    new_dict = user.dict()
    new_dict['password'] = pwd_contex.hash(user.password)
    result = collection2.insert_one(new_dict)
    new_dict['_id'] = str(result.inserted_id)
    return new_dict

@app.get('/users', response_model=List[User])
async def get_users(username: str = Query(..., description ='enter title')):
    users = list(collection2.find({'username':username}, { "password": 0}))
    return users

#-- scheduler 
def cleanup_old_blogs():
    # Example: delete blogs older than 1 day
    cutoff = datetime.utcnow() - timedelta(days=1)
    result = collection.delete_many({"created_at": {"$lte": cutoff}})
    print(f"[{datetime.utcnow()}] Cleaned {result.deleted_count} old blogs")

scheduler = BackgroundScheduler()
scheduler.add_job(cleanup_old_blogs, CronTrigger(hour=9, minute=7))  # run every midnight
scheduler.start()

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    scheduler.shutdown() 


fake_users = {'alex': 'secret'}

@app.post('/login')
def login(user : User):
    if user.username in fake_users and fake_users[user.username] == user.password:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=400, detail="Invalid Credentials")
    
from fastapi.security import HTTPBearer
oauth2_scheme = HTTPBearer()

@app.get('/login')
def read_secure_data(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    username: str = payload.get("sub")
    return {"msg": f"Hello, {username}. This is secured data."}