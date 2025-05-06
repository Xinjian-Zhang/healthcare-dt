import os
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
SEPOLIA_RPC_URL = os.getenv("SEPOLIA_RPC_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
ADT_INSTANCE_URL = os.getenv("ADT_INSTANCE_URL")

# Serial port configuration
SERIAL_PORT = "COM4"
BAUD_RATE = 115200
READ_INTERVAL = 5
