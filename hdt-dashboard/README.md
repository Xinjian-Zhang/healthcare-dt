# Healthcare Digital Twins Dashboard - with ADT, DeepSeek AI

It project is a simple healthcare dashboard that integrates Azure Digital Twins (ADT) and DeepSeek AI to monitor patient health data in real-time. The application retrieves patient and room data from Azure Digital Twins, monitors various health metrics, and provides AI-generated clinical suggestions based on the data.

## Features

- User login and authentication
- Patient and room data retrieval from Azure Digital Twins
- Real-time sensor monitoring (body temp, heart rate, SpO2, room temp/humidity)
- Alert logic for abnormal conditions
- AI-generated clinical suggestions using DeepSeek (OpenAI-compatible API)

## Project Structure

```
project/
├── main.py
├── .env
├── users.json
├── requirements.txt
├── web/
│   ├── login.html
│   └── dashboard.html
├── core/
│   ├── auth.py
│   ├── adt_client.py
│   ├── data_retrieval.py
│   └── ai_suggestion.py
├── utils/
│   └── config.py
```

## Setup Instructions


1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up your `.env` file with Azure and DeepSeek credentials:

   ```
      SEPOLIA_RPC_URL=your_rpc_url
      CONTRACT_ADDRESS=your_contract_address
      PRIVATE_KEY=your_private_key
      ADT_INSTANCE_URL=your_adt_instance_url
      DEEPSEEAK_API_KEY=your_deepseek_api_key
      DEEPSEEAK_BASE_URL=https://api.deepseek.com/v1
   ```

3. Run the app:
   ```bash
   python main.py
   ```

## Requirements

See `requirements.txt` for dependencies.

Run the following command to install the required packages:

```bash
pip install -r requirements.txt
```

## Notes

- You must have Azure credentials properly configured for `DefaultAzureCredential` to work.
- The DeepSeek API is used via the OpenAI-compatible interface.

## Security Notes!!!

All sensitive information in `.env` must be excluded from version control.

## About

This code is as a part of a Master's thesis project.

- Author: Xinjian Zhang
- [Github Link](https://github.com/Xinjian-Zhang)

---