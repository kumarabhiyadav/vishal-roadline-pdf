import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# Load environment variables from .env file
load_dotenv()

# Get the Mongo URI and DB name
MONGO_DETAILS = os.getenv("MONGO_DETAILS")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

# Connect to MongoDB
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client[MONGO_DB_NAME]  # Use env-defined DB name
invoice_collection = database.get_collection("invoices")
