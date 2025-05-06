from azure.digitaltwins.core import DigitalTwinsClient
from azure.identity import DefaultAzureCredential
from datetime import datetime

from config import ADT_INSTANCE_URL

credential = DefaultAzureCredential()
adt_client = DigitalTwinsClient(ADT_INSTANCE_URL, credential)

def upsert_property(twin_id, property_name, value):
    try:
        twin = adt_client.get_digital_twin(twin_id)
        op = "replace" if property_name in twin else "add"
        patch = [{"op": op, "path": f"/{property_name}", "value": value}]
        adt_client.update_digital_twin(twin_id, patch)
        print(f"[{datetime.now().isoformat()}] {op.upper()} {twin_id} {property_name}: {value}")
    except Exception as e:
        print(f"Error updating {twin_id} {property_name}: {e}")

def update_status(twin_id, status):
    patch = [{"op": "replace", "path": "/Status", "value": status}]
    try:
        adt_client.update_digital_twin(twin_id, patch)
        print(f"[{datetime.now().isoformat()}] Status updated: {twin_id} -> {status}")
    except Exception as e:
        print(f"Error updating {twin_id} status: {e}")

def get_twin_property(twin_id, property_name):
    try:
        twin = adt_client.get_digital_twin(twin_id)
        return twin.get(property_name)
    except Exception as e:
        print(f"Error reading {property_name} from {twin_id}: {e}")
        return None
