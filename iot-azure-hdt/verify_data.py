import os
import json
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from web3 import Web3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATA_FOLDER = "data"
TX_MAP_FILE = "blockchain_tx_map.json"
SEPOLIA_RPC_URL = os.getenv("SEPOLIA_RPC_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

# ABI with only storeEncryptionKey
contract_abi = [
    {
        "inputs": [
            {"internalType": "string", "name": "sensorId", "type": "string"},
            {"internalType": "bytes32", "name": "keyHash", "type": "bytes32"}
        ],
        "name": "storeEncryptionKey",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# Setup Web3 and contract
w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC_URL))
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

# Load blockchain_tx_map.json
tx_map = {}
if os.path.exists(TX_MAP_FILE):
    with open(TX_MAP_FILE, "r") as f:
        try:
            tx_map = json.load(f)
        except json.JSONDecodeError:
            tx_map = {}

# Find all .json sensor data files
json_files = sorted([f for f in os.listdir(DATA_FOLDER) if f.endswith(".json")])

total = len(json_files)
passed = 0
failed = 0
failed_files = []

for idx, json_file in enumerate(json_files, 1):
    base = os.path.splitext(json_file)[0]
    json_path = os.path.join(DATA_FOLDER, f"{base}.json")
    enc_path = os.path.join(DATA_FOLDER, f"{base}.enc")
    key_path = os.path.join(DATA_FOLDER, f"{base}.key")

    print(f"\nFile {idx} - Verifying: {base}")

    if not (os.path.exists(enc_path) and os.path.exists(key_path)):
        print("Missing .enc or .key file")
        failed += 1
        failed_files.append(base)
        continue

    try:
        with open(json_path, "r") as f:
            json_data = json.load(f)

        with open(key_path, "r") as f:
            key_hex = f.read().strip()
        key = bytes.fromhex(key_hex)

        with open(enc_path, "rb") as f:
            data = f.read()
        nonce = data[:12]
        ciphertext = data[12:-16]
        tag = data[-16:]

        aesgcm = AESGCM(key)
        decrypted = aesgcm.decrypt(nonce, ciphertext + tag, None)
        decrypted_data = json.loads(decrypted.decode("utf-8"))

        if decrypted_data == json_data:
            print("Decryption matched JSON")
        else:
            print("Decryption succeeded but content mismatch")
            failed += 1
            failed_files.append(base)
            continue

        tx_hash = tx_map.get(f"{base}.json")
        if not tx_hash:
            print("No transaction hash found in blockchain_tx_map.json")
            failed += 1
            failed_files.append(base)
            continue

        try:
            tx = w3.eth.get_transaction(tx_hash)
            func_obj, params = contract.decode_function_input(tx.input)
            onchain_key_hash = params.get('keyHash')
            local_key_hash = hashlib.sha256(key).digest()

            if onchain_key_hash == local_key_hash:
                print("Blockchain keyHash matched transaction input")
            else:
                print("Blockchain keyHash mismatch in transaction input")
                failed += 1
                failed_files.append(base)
                continue

            print(f"Matched transaction hash: {tx_hash}")

        except Exception as e:
            print(f"Failed to read or decode transaction: {e}")
            failed += 1
            failed_files.append(base)
            continue

        passed += 1

    except Exception as e:
        print(f"Exception during verification: {e}")
        failed += 1
        failed_files.append(base)

print("\n=== Verification Summary ===")
print(f"Total files verified: {total}")
print(f"Passed: {passed}")
print(f"Failed: {failed}")
if failed_files:
    print("Failed files: " + ", ".join(failed_files))
