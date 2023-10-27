from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta
from typing import List

app = FastAPI()
SECRET_KEY = "your-secret-key"

# Token expiration time (e.g., 1 hour)
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Database Models (using a list for simplicity)
class User(BaseModel):
    id: int
    email: str
    name: str
    hashed_password: str

class BlogPost(BaseModel):
    id: int
    title: str
    body: str
    author_id: int
    created_at: datetime

# Token
class Token(BaseModel):
    access_token: str
    token_type: str

# Simulated Database
users_db = []
blog_posts_db = []

# Password Hashing
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 Password Flow
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Create User
@app.post("/users/", response_model=User)
async def create_user(user: User):
    # Check if the user with the same email already exists
    if any(u["email"] == user.email for u in users_db):
        raise HTTPException(status_code=400, detail="User with this email already exists")
    hashed_password = password_context.hash(user.hashed_password)
    user_data = user.dict()
    user_data["hashed_password"] = hashed_password
    user_data["id"] = len(users_db) + 1  # Generate a unique user ID
    users_db.append(user_data)

    return user_data

# Secret key for signing the token (keep this secret!)


# Function to generate an access token
def create_access_token(data: dict):
    to_encode = data.copy()
    # Calculate the expiration time
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # Sign the token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

# User Login
@app.post("/login/", response_model=Token)
async def login(user_data: dict = Body(...)):
    print(user_data)
    email = user_data.get("email")
    password = user_data.get("password")
    print(email)
    
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password are required")
    
    user = authenticate_user(email, password)
    if user is None:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    # Generate and return an access token
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}



# Authenticate User
def authenticate_user(email: str, password: str):
    for user in users_db:
        if user["email"] == email and password_context.verify(password, user["hashed_password"]):
            return user

    return None

# Get Token
@app.post("/token/", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    return {"access_token": user["email"], "token_type": "bearer"}

# Create Blog Post
@app.post("/blog/", response_model=BlogPost)
async def create_blog_post(post: BlogPost, token: str = Depends(oauth2_scheme)):
    # Authenticate user based on the provided token
    user = authenticate_user(token, "")
    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    post_data = post.dict()
    post_data["author_id"] = user["id"]
    post_data["created_at"] = datetime.now()
    blog_posts_db.append(post_data)
    post_data["id"] = len(blog_posts_db)
    return post_data

# Get Blog Posts
@app.get("/blog/", response_model=List[BlogPost])
async def get_blog_posts():
    return blog_posts_db

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
