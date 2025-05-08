import os
from azure.digitaltwins.core import DigitalTwinsClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

ADT_INSTANCE_URL = os.getenv("ADT_INSTANCE_URL")
if not ADT_INSTANCE_URL:
    raise Exception("ADT_INSTANCE_URL must be set in .env")

# Singleton pattern for ADT client
credential = DefaultAzureCredential()
adt_client = DigitalTwinsClient(ADT_INSTANCE_URL, credential)
