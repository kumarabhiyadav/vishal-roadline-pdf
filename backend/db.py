import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
load_dotenv() 
MONGO_DETAILS = os.getenv("MONGO_DETAILS")  # Your MongoDB URI
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.vishalroadline  # Database name
invoice_collection = database.get_collection("invoices")  # Collection name
