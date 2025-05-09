# Blockchain Smart Contract: DataKeyStorage

This contains a Solidity smart contract and associated scripts for securely storing and verifying encryption key hashes associated with IoT sensor data. The contract is deployed on the Ethereum Sepolia test network and is designed to integrate with an IoT and Azure Digital Twins system.

## Contract Overview

The `DataKeyStorage` contract allows an authorized owner (typically a backend system) to store SHA256 hashes of AES encryption keys used to encrypt healthcare-related IoT sensor data. The key hashes are indexed by sensor IDs and can be retrieved for verification purposes.

### Key Features

- `storeEncryptionKey(sensorId, keyHash)`: Stores a key hash against a sensor ID (owner-only).
- `getEncryptionKey(sensorId)`: Returns the key hash stored for a sensor ID.
- Emits `KeyStored` event with a timestamp upon successful storage.
- Maintains `keyCount` to track the number of stored entries.

## Project Structure

| Path                   | Description                            |
|------------------------|----------------------------------------|
| `contracts/`           | Contains the Solidity contract         |
| `scripts/deploy.js`    | Script to deploy the contract via Hardhat |
| `hardhat.config.js`    | Hardhat configuration file             |
| `.env`                 | Stores environment variables (excluded from version control) |
| `artifacts/`, `cache/` | Build output directories (ignored by git) |

## Prerequisites

- Node.js (v16+ recommended)
- Hardhat
- Infura project ID for Sepolia RPC
- Sepolia test account with ETH
- Etherscan API key for verification (optional)

## Setup

1. Install dependencies:

```bash
npm install
```

2. Create a `.env` file in the root directory:

```ini
INFURA_PROJECT_ID=your_infura_project_id
PRIVATE_KEY=your_private_key_without_0x
ETHERSCAN_API_KEY=your_etherscan_api_key
```

3. Compile the contract:

```bash
npx hardhat compile
```

## Deployment

Deploy the contract to Sepolia using the provided script:

```bash
npx hardhat run scripts/deploy.js --network sepolia
```

## Verification

If you configured your Etherscan API key in `.env`, you can verify the deployed contract:

```bash
npx hardhat verify --network sepolia <deployed_contract_address>
```

## Security Notes!!!

- Only the contract owner can call `storeEncryptionKey`.
- Ensure `.env` is excluded from source control (see `.gitignore`).
- Use secure methods to manage and back up your private key.

## Acknowledgments

- [Hardhat](https://hardhat.org/)
- [OpenZeppelin Contracts](https://github.com/OpenZeppelin/openzeppelin-contracts)

---

## About

This code is as a part of a Master's thesis project.

- Author: Xinjian Zhang
- [Github Link](https://github.com/Xinjian-Zhang)

---