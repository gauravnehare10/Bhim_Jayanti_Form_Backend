from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from models.models import RequestModel
from config.database import registrations, withdraw_registrations
import uuid
from datetime import datetime


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
    if not request_data["transport"] == "car":
        request_data["carPool"] = False
        request_data["carPoolSeats"] = 0

    if not request_data["accommodation"] == "home":
        request_data["homeSpace"] = False
        request_data["homeSpaceCount"] = 0

    request_data["_id"] = str(uuid.uuid4())
    request_data["registered_at"] = datetime.utcnow()
    registered_data = await registrations.insert_one(request_data)
    return {"RegistrationId": request_data["_id"]}

@app.get("/get_data/{registration_id}")
async def get_data(registration_id: str):
    reg_data = await registrations.find_one({'_id': registration_id})
    return reg_data

@app.put("/update/{registration_id}")
async def update(registration_id: str, data: RequestModel):
    request_data = dict(data)
    if not request_data["transport"] == "car":
        request_data["carPool"] = False
        request_data["carPoolSeats"] = 0

    if not request_data["accommodation"] == "own":
        request_data["homeSpace"] = False
        request_data["homeSpaceCount"] = 0

    request_data["registered_at"] = datetime.utcnow()
    user_data = await registrations.find_one({"_id": registration_id})
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data Not Found")
    
    await registrations.update_one({"_id": registration_id}, {"$set": request_data})
    updated_data = await registrations.find_one({"_id": registration_id})
    return {"RegistrationId": registration_id}

@app.delete("/withdraw/{registration_id}")
async def withdraw_registration(registration_id: str):
    user = await registrations.find_one({"_id": registration_id})
    if user:
        user["Withdraw"] = "pending"
        await withdraw_registrations.insert_one(user)
        await registrations.delete_one({"_id": registration_id})
    else:
        HTTPException(status_code=404, detail="Not Found")

    return {"message": "Withdrawal requested successful, you will get refunded within a week."}