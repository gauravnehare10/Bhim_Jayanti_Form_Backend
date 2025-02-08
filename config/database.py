import os
from dotenv import find_dotenv, load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient


dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

MONGO_URL = os.getenv("MONGO_URL")
SECRET_KEY = os.getenv("SECRET_KEY")

db_client = AsyncIOMotorClient(MONGO_URL)

registrations = db_client.Bhim_Jayanti.registrations
withdraw_registrations = db_client.Bhim_Jayanti.withdraw_registrations
user_collection = db_client.Bhim_Jayanti.user_collection
