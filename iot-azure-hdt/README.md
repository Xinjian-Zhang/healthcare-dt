# IoT-Azure-HDT (a Healthcare Digital Twin System) 

A Python-based system for healthcare data collection, real-time monitoring, and secure storage. It integrates **IoT sensor data**, **Azure Digital Twins**, **AES encryption**, and **Ethereum Sepolia blockchain** to provide a verifiable and tamper-proof health data pipeline.

---

## Project Structure

| File / Folder         | Description |
|-----------------------|-------------|
| `main.py`             | Main runtime loop: reads serial data, evaluates status, updates Digital Twins, aggregates data |
| `config.py`           | Stores configuration constants and loads `.env` |
| `adt_utils.py`        | Functions for interacting with Azure Digital Twins |
| `sensors.py`          | Sensor status evaluation and decision logic |
| `parser.py`           | Parses serial input into structured sensor data |
| `aggregator.py`       | Collects data over time, saves `.json`, `.enc`, `.key` |
| `blockchain_utils.py` | Stores AES key hash on Ethereum Sepolia |
| `verify_data.py`      | Verifies `.json`/`.enc`/`.key` files and blockchain tx hash consistency |
| `.env`                | Environment variable file (do **NOT** commit sensitive keys) |
| `blockchain_tx_map.json` | Local record mapping `.json` file to transaction hash |
| `data/`               | Folder where all collected `.json`, `.enc`, `.key` files are stored |

---

## Setup

1. **Install dependencies**:

```bash
pip install -r requirements.txt
```

2. Prepare `.env` file:

```ini
# .env

# Blockchain
SEPOLIA_RPC_URL=https://sepolia.infura.io/v3/your_project_id
CONTRACT_ADDRESS=0xYourContractAddress
PRIVATE_KEY=0xYourPrivateKey

# Azure Digital Twins
ADT_INSTANCE_URL=https://your-instance.api.wus2.digitaltwins.azure.net
```

3. Connect your serial device (e.g., Arduino/ESP8266)

Update the correct serial port in config.py:

```python
SERIAL_PORT = "COM4"  # or /dev/ttyUSB0 for Linux
```

4. Run the System

```bash
python main.py
```

The system will:
- Collect sensor data via serial or simulation 
- Evaluate patient and room status 
- Update Azure Digital Twins with latest values and alerts
- Periodically aggregate data to `.json `
- Encrypt it to `.enc` using AES-GCM
- Store `SHA256(key`)` on Ethereum Sepolia
- Map tx hash to file via `blockchain_tx_map.json`

---

## Data Verification

To verify data consistency after collection:

1. Step 1: Ensure `data/` contains matching files:

```
data/
├── sensor_data_timestamp.json
├── sensor_data_timestamp.enc
├── sensor_data_timestamp.key
```
And blockchain_tx_map.json contains:

```json
{
  "sensor_data_timestamp.json": "tx_hash_here"
}
```
2. Step 2: Run the verification script:

```bash
python verify_data.py
```

It will:
- Decrypt `.enc` using `.key` and compare to `.json`
- Compute SHA256(key) and compare with on-chain transaction input
- Report pass/fail for each file and give a final summary

### Sample Output:
```
File 1 - Verifying: sensor_data_20250425T012813
Decryption matched JSON
Blockchain keyHash matched transaction input
Matched transaction hash: 0xe2d7...

=== Verification Summary ===
Total files verified: 1
Passed: 1
Failed: 0

```

## Security Notes!!!
- `.key` files are stored locally for verification, but should be encrypted or stored in a secure key vault in production.
- `blockchain_tx_map.json` is the local mapping file. If lost, you must query tx hash manually.
- All sensitive information in `.env` must be excluded from version control.

---

## About

This code is as a part of a Master's thesis project.

- Author: Xinjian Zhang
- [Github Link](https://github.com/Xinjian-Zhang)

---