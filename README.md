# blockchain-raspberry-pi

## What
This is the course project for the subject Blockchain and Cryprocurrency in the 6th semester of IIIT Allahabad. We have implemented how blockchain can be used to store information of IoT devices, specifically the status of GPIO Pins (on / off) in a Raspberry Pi, and temperature readings from thermal sensor emulator.

## Why
With a horde of IoT devices proliferating the day-to-day lives of people around the world, they often lack the authentication standards necessary to keep user data safe. Critical infrastructure will be damaged if hackers penetrate through these devices. Therefore, in order to ensure trust, authentication, and standardization across all elements of IoT, blockchain can be used.

## How
The details regarding the implementation, functionalities, results and demonstration can be found in the uploaded <a href="Report.pdf">report</a>. For usage, first clone this repository and then open a terminal in the project folder. Then the following commands need to be run in order:

1. `pip3 install -r requirements.txt`
2. `npm install`
3. `truffle compile`
4. `ganache-cli 2>&1 | tee logs`
5. `python3 app.py`
