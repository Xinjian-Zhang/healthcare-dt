


          
# Medical IoT Digital Twin System

This repository contains a comprehensive implementation of a `Blockchain-Enabled Digital Twins in Healthcare`, some critical codes are collectively stored here.

## Project Contents

### 1. IoT Firmware (healthcare-iot-firmware)
- Location: `/healthcare-iot-firmware/`
- Description: Arduino firmware for patient vital sign data acquisition
- Supported Sensors:
  - MAX30105 (Heart Rate & SpO2)
  - MAX30205 (Body Temperature)
  - AM2320 (Ambient Temperature & Humidity)
  - SSD1306 OLED Display

### 2. Azure Digital Twin - IoT Data Processing Service (iot-azure-hdt)
- Location: `/iot-azure-hdt/`
- Core Functions:
  - IoT device data ingestion
  - Data encryption and blockchain key storage
  - Azure Digital Twins (ADT) state management
  - Data validation utilities

### 3. Blockchain Smart Contract -  Key Storage(blockchain-key-storage-contract)
- Location: `/blockchain-key-storage-contract/`
- Description: Ethereum-based smart contract for encrypted data key hash storage
- Tech Stack: Solidity, Hardhat, OpenZeppelin

### 4. Healthcare Digital Twin Dashboard (hdt-dashboard)
- Location: `/hdt-dashboard/`
- Features:
  - Real-time patient monitoring interface
  - Environmental parameter visualization
  - DeepSeek AI integration for health insights

### 5. Digital Twin Models (dtdl-models)
- Location: `/dtdl-models/`
- Content: Azure Digital Twins Definition Language (DTDL) models
- Model Types:
  - Patient model (ParentDT)
  - Room model  (ParentDT)
  - Sensor models (ChildDTs)

## Security Considerations

- Environment variables stored in `.env` files (gitignored always!)
- Secure storage requirements for encryption keys and blockchain transaction mappings
- Production deployment security hardening guidelines

## Author
- Xinjian Zhang
- [GitHub Profile](https://github.com/Xinjian-Zhang)

---

> Note: This implementation serves as a prototupe of `Blckchain-Enabled Digital Twins in Healthcare` for a Master's thesis project.

        