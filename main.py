from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from models.models import RequestModel
from config.database import registrations, withdraw_registrations
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

@app.get("/get_data/{registration_id}", response_model=RequestModel)
async def get_data(registration_id: str):
    print(registration_id)
    reg_data = await registrations.find_one({'_id': registration_id})
    return reg_data

@app.put("/update/{registration_id}")
async def update(registration_id: str, data: RequestModel):
    request_data = dict(data)
    user_data = await registrations.find_one({"_id": registration_id})
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data Not Found")
    
    await registrations.update_one({"_id": registration_id}, {"$set": request_data})
    updated_data = await registrations.find_one({"_id": registration_id})
    return {"RegistrationId": registration_id}

@app.put("/withdraw/{registration_id}")
async def withdraw_registration(registration_id: str):
    user = await registrations.find_one({"_id": registration_id})
    if user:
        user["Withdraw"] = True
        await withdraw_registrations.insert_one(user)
        await registrations.delete_one({"_id": registration_id})
    else:
        HTTPException(status_code=404, detail="Not Found")

    return {"message": "Withdrawn successful, you will get refunded within a week."}