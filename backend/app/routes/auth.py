import jwt
import bcrypt
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from app.config import settings
from app.database import get_users_collection
from app.models.schemas import UserRegister, UserLogin, Token, TokenData

router = APIRouter(prefix="/auth", tags=["Authentication"])

# OAuth2 scheme for extracting token from header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Helper security functions
def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    # Generate salt and hash password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hashed representation."""
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

def create_access_token(data: dict) -> str:
    """Create a signed JWT token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Dependency to validate JWT token and return active user profile.
    Raises 401 if token is invalid or expired.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception
        
    users_col = get_users_collection()
    user = users_col.find_one({"username": token_data.username})
    if user is None:
        raise credentials_exception
    return user


# ==========================================
# Endpoints
# ==========================================

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_in: UserRegister):
    """
    Register a new student user.
    """
    users_col = get_users_collection()
    
    # Check if username is already taken
    existing_user = users_col.find_one({"username": user_in.username})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
        
    # Hash password and insert
    hashed_pwd = hash_password(user_in.password)
    user_doc = {
        "username": user_in.username,
        "password": hashed_pwd,
        "name": user_in.name,
        "age": user_in.age,
        "gender": user_in.gender,
        "created_at": datetime.utcnow().isoformat()
    }
    
    users_col.insert_one(user_doc)
    return {"message": "User registered successfully", "username": user_in.username}

@router.post("/login", response_model=Token)
def login(credentials: UserLogin):
    """
    Authenticate user and return JWT access token.
    """
    users_col = get_users_collection()
    
    # Locate user document
    user = users_col.find_one({"username": credentials.username})
    if not user or not verify_password(credentials.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # Generate token
    access_token = create_access_token(data={"sub": user["username"]})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user["username"],
        "name": user["name"]
    }
