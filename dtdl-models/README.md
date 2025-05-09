# Azure Digital Twins DTDL Models for Healthcare DT System

This directory contains a collection of DTDL (Digital Twins Definition Language) interface models designed for a smart patient room Healhcare DT system. The models define digital representations of patients, sensors, and rooms in a hospital environment using Azure Digital Twins.

## Overview

These models describe patient-related physiological data (body temperature, heart rate, SpO₂), room environment conditions (temperature, humidity), and the digital representation of a patient and room. They define data properties and relationships between components.

## Directory Contents

| File                            | Description                              |
|---------------------------------|------------------------------------------|
| `patient_model.json`            | Main patient twin interface with demographics and sensor relationships |
| `body_temperature_model.json`   | Body temperature sensor interface        |
| `heart_rate_model.json`         | Heart rate sensor interface              |
| `spO2_model.json`               | SpO₂ sensor interface                    |
| `room_model.json`               | Room interface with temperature/humidity sensor links |
| `room_temperature_model.json`   | Room temperature sensor interface        |
| `room_humidity_model.json`      | Room humidity sensor interface           |
| `read-files.ps1`                | PowerShell utility to display all model files (for debugging or listing) |

## Key Concepts

### Interface Composition

Each model follows the standard DTDL v2 structure:
- `@id`: A unique Digital Twin Model Identifier (DTMI)
- `@type`: All models are of type `Interface`
- `@context`: Set to `dtmi:dtdl:context;2`
- `contents`: A list of properties or relationships relevant to the model

### Patient Model Relationships

The `patient_model.json` defines the following relationships:
- `hasBodyTemperature`: Links to body temperature interface
- `hasHeartRate`: Links to heart rate interface
- `hasSpO2`: Links to SpO₂ interface
- `assignedToRoom`: Links to the room the patient occupies

### Room Model Relationships

The `room_model.json` defines:
- `hasTemperatureSensor`: Links to temperature sensor interface
- `hasHumiditySensor`: Links to humidity sensor interface

## Conventions

- **Sensor ID fields**: All sensor interfaces include a unique identifier field (e.g., `BodyTemperatureSensorId`, `SpO2SensorId`)
- **Status fields**: Each sensor model includes a `Status` field indicating sensor or measurement state (e.g., Normal, Too High, Too Low)
- **Data types**: All physiological readings are `double`, IDs are `string`, and some patient attributes (like age) use `integer`

## Usage

These models can be registered into your Azure Digital Twins instance using the Azure CLI or SDKs:

```bash
az dt model upload --dt-name <your-instance-name> --models <path-to-models>/*.json
```

You can then instantiate twins based on these interfaces and establish relationships among them programmatically or via the Azure Digital Twins Explorer.


## Twin Graph Example

Twin Graph allows you to query and visualize the relationships and properties of digital twins. In this directory, a example twin graph is provided.

`twin_graph (Exported at Mon Apr 28 2025 012526 GMT+3 EEST).json`


## Dependencies

- [DTDL v2 specification](https://learn.microsoft.com/en-us/azure/digital-twins/concepts-models)
- [Azure CLI or SDK](https://learn.microsoft.com/en-us/azure/digital-twins/quickstart-cli)

---

## About

This code is as a part of a Master's thesis project.

- Author: Xinjian Zhang
- [Github Link](https://github.com/Xinjian-Zhang)

---