from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import shutil, os

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print("DB Session Error:", e)
        raise HTTPException(status_code=500, detail="Internal DB Error")
    finally:
        db.close()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

coffee_data = {
    1: {"name": "Espresso", "instructions": "Brew under pressure."},
    2: {"name": "Latte", "instructions": "Add steamed milk to espresso."},
    3: {
        "name": "Cappuccino",
        "instructions": "Use equal parts espresso, milk, and foam.",
    },
}


@app.get("/")
def root():
    return RedirectResponse(url="/docs")  # "/redoc"


@app.get("/coffees")
def get_coffees():
    return list(coffee_data.values())


@app.get("/brew/{coffee_id}")
def brew_coffee(coffee_id: int):
    if coffee_id not in coffee_data:
        raise HTTPException(status_code=404, detail="Coffee not found")
    return coffee_data[coffee_id]


@app.post("/upload-recipe")
async def upload_recipe(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename}
