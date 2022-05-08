import time
from random import randint
from app import contract_instance, w3
from globals import *

def log_values():
    # open 'temp' file
    f = open(PATH_TO_DEVICES, "a")
    # initialize the temperature value
    temperature = randint(-100, 200)    
    while True:
        # log the temperature value in the file
        f.write(str(temperature) + "\n")
        f.flush()
        # simulataneously initiate a transaction
        contract_instance.functions.control(
            TEMP_PIN, True, 1, temperature
        ).transact({
            'from': w3.eth.accounts[0]
        })
        # change temperature value
        temperature += randint(-3, 3)
        time.sleep(2)
        
if __name__ == "__main__":
    log_values()
