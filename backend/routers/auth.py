from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.schemas.user import UserCreate, UserLogin, UserOut
from backend.models.user import User
from backend.core import auth, database

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(data: UserCreate, db: Session = Depends(database.get_db)):
    if db.query(User).filter_by(username=data.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed = auth.hash_password(data.password)
    user = User(username=data.username, email=data.email, hashed_password=hashed)
    db.add(user)
    db.commit()
    return {"message": "User created"}


@router.post("/login")
def login(data: UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(User).filter_by(username=data.username).first()
    if not user or not auth.verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = auth.create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
def get_me(user: User = Depends(auth.get_current_user)):
    return user


@router.get("/", response_model=list[UserOut])
def list_users(db: Session = Depends(database.get_db)):
    return db.query(User).all()
