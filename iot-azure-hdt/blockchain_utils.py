import hashlib
import json
import os
from web3 import Web3
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from config import SEPOLIA_RPC_URL, PRIVATE_KEY, CONTRACT_ADDRESS

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
    },
    {
        "inputs": [{"internalType": "string", "name": "sensorId", "type": "string"}],
        "name": "getEncryptionKey",
        "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "stateMutability": "view",
        "type": "function"
    }
]

w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)
w3.eth.default_account = account.address
data_key_storage = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

TX_RECORD_FILE = "blockchain_tx_map.json"

def encrypt_file(filename):
    with open(filename, "rb") as f:
        plaintext = f.read()
    key = AESGCM.generate_key(bit_length=256)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    enc_filename = filename.replace(".json", ".enc")
    with open(enc_filename, "wb") as f:
        f.write(nonce + ciphertext)
    print(f"Encrypted and saved: {enc_filename}")

    key_filename = filename.replace(".json", ".key")
    with open(key_filename, "w") as f:
        f.write(key.hex())
    print(f"Encryption key saved to {key_filename}")

    return key

def store_key_on_blockchain(sensor_ids_str, encryption_key, filename):
    key_hash = hashlib.sha256(encryption_key).digest()
    try:
        nonce_val = w3.eth.get_transaction_count(w3.eth.default_account, 'pending')
        tx = data_key_storage.functions.storeEncryptionKey(sensor_ids_str, key_hash).build_transaction({
            'from': w3.eth.default_account,
            'nonce': nonce_val,
            'gas': 100000,
            'gasPrice': w3.eth.gas_price
        })
        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_hex = tx_hash.hex()
        print(f"Blockchain Tx: {tx_hex}")

        # update record
        tx_map = {}
        if os.path.exists(TX_RECORD_FILE):
            with open(TX_RECORD_FILE, "r") as f:
                try:
                    tx_map = json.load(f)
                except json.JSONDecodeError:
                    pass
        tx_map[os.path.basename(filename)] = tx_hex
        with open(TX_RECORD_FILE, "w") as f:
            json.dump(tx_map, f, indent=2)
    except Exception as e:
        print(f"Blockchain error: {e}")
