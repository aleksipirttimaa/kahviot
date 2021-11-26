# KahvIOT

## This repository

- `node`: A temperature sensor that consists of an ESP32 and a DS18B20 compatible temperature sensor
- `api`: HTTP API that exports submitted measurements to prometheus

## Node

The node consists of:

- An ESP32
- A DS18B20 temperature sensor
- Some 3 pin flat cable
- A project case
- A 5V power supply

The software running on the ESP32 is implemented with "Arduino core for ESP32". This environment was selected as it seemed easy and quick.

For building and flashing the firmware you'll need:

- Arduino IDE
- `esp32` from the Arduino IDE Boards Manager 
- `DallasTemeprature.h` from the Arduino IDE Library Manager
