from typing import Annotated
from database import SessionLocal, engine
from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from auth import get_current_user, router
import model

app = FastAPI()
app.include_router(router=router)
model.Base.metadata.create_all(bind=engine)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/", status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return {"User": user}
