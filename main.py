from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from models.models import RequestModel
from config.database import registrations
import uuid


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/register')
async def register(data: RequestModel):
    request_data = dict(data)
    request_data["_id"] = str(uuid.uuid4())
    registered_data = await registrations.insert_one(request_data)
    return {"RegistrationId": request_data["_id"]}


@app.put("/update/{registration_id}")
async def update(registration_id: str, data: RequestModel):
    request_data = dict(data)
    user_data = await registrations.find_one({"RegistrationId": registration_id})
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data Not Found")
    
    updated_data = await registrations.update_one({"RegistrationId": registration_id}, {"$set": request_data})