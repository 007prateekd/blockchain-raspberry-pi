import json
from web3 import Web3, HTTPProvider
from RPiSim.GPIO import GPIO
from flask import Flask, render_template
import sys
import os
from subprocess import Popen, PIPE, STDOUT
from globals import *
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# in order of positions in Raspberry Pi
pin_list = [14, 15, 18, 23, 24, 25, 8, 7, 12, 16, 20, 21, 2, 3, 4, 17, 27, 22, 10, 9, 11, 5, 6, 13, 19, 26]
pin_to_actuator = {
    'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
    'ten': 10, 'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15, 'sixteen': 16,
    'seventeen': 17, 'eighteen': 18, 'nineteen': 19, 'twenty': 20, 'twentyone': 21, 'twentytwo': 22,
    'twentythree': 23, 'twentyfour': 24, 'twentyfive': 25, 'twentysix': 26, 'twentyseven': 27                   
}

# set up every channel as an output channel
for pin in pin_list:
    GPIO.setup(pin, GPIO.OUT)

# using compiled smart contract
contract = json.load(open('./build/contracts/myContract.json'))
abi = contract['abi']
bytecode = contract['bytecode']

# initialise a web3.py instance
w3 = Web3(HTTPProvider("http://localhost:8545/"))

# instantiate and deploy contract
contract = w3.eth.contract(abi=abi, bytecode=bytecode)

# get transaction hash from deployed contract
tx_hash = contract.constructor().transact({'from': w3.eth.accounts[0], 'gas': 410000})

# get transaction receipt to get contract address
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# deployed contract instance
contract_instance = w3.eth.contract(abi=abi, address=tx_receipt.contractAddress)
contract_instance.functions.control(TEMP_PIN, True, 0, 1000).transact({'from': w3.eth.accounts[0]})

# print initial values of each pin
print("=" * 41)
print("Pin\t[IsTempSens, Status, Temperature]")
print("=" * 41)
for pin in pin_list:
    print(pin, '\t\t{}'.format(contract_instance.functions.pinStatus(pin).call()))

app = Flask(__name__)

@app.route("/")
def index():
    '''
    opens the home page which allows us to click
    ON or OFF to change the status of each pin
    '''
    return render_template('index.html')
    
@app.route("/trans")
def trans():
    '''
    opens a new page which helps in displaying the logs
    of all the transactions that have taken place till now
    '''
    return render_template('trans.html')
	
@app.route("/<pin>/<action>")
def control(pin, action):
    # actuator configuration
    actuator = pin_to_actuator[pin]
    config = 1 if action == 'on' else 0
    old_status = contract_instance.functions.pinStatus(actuator).call()[1]
    
    if actuator == TEMP_PIN:
        global PROCESS
        if action == 'on':
            # start simulating temperature sensor
            PROCESS = Popen([sys.executable, 'virtual_temp.py'], 
                             stdout=PIPE, stderr=STDOUT)
        else:
            # stop simulation
            PROCESS.terminate()
            tx_hash = contract_instance.functions.control(TEMP_PIN, True, 0, 1000).transact({'from': w3.eth.accounts[0]})
            print('Transaction submitted:', tx_hash.hex())
            # remove device file
            os.remove(PATH_TO_DEVICES) 
    else:
        # if actuator is already on, do nothing
        if old_status == config:
            return render_template('index.html')
        # submit a transaction to change the pin structure of the actuator
        tx_hash = contract_instance.functions.control(actuator, False, config, 1000).transact({'from': w3.eth.accounts[0]})
        print('Transaction submitted:', tx_hash.hex())

    print(f'Pin {actuator} Status Changed: {config}')
    # change the status of the pin in virtual Raspberry Pi
    if config == 1:
        GPIO.output(actuator, GPIO.HIGH)
    else:
        GPIO.output(actuator, GPIO.LOW)
    return render_template('index.html')

if __name__ == '__main__':
    # run the flask app
    app.run(port=8000, host='0.0.0.0', debug=True, use_reloader=False)
