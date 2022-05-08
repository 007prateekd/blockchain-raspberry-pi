pragma solidity ^0.5.0;

contract myContract {
  address owner;

  constructor() public {
    owner = msg.sender;
  }

  struct pin {
    // whether the pin is a temperature sensor
    bool isTempSens; 
    // status of each pin - on or off
    uint256 status;
    // temperature of sensor - 10000 if not a temperature sensor or the sensor is off
    uint256 temp;    
  }

  // stores the information for each pin in a mapping
  mapping(uint256 => pin) public pinStatus;

  // controls the pin by changing the values in the structure of a pin
  function control(uint256 _pin, bool _isTempSens, uint256 _status, uint256 _temp) public {
    require(msg.sender == owner);
    pinStatus[_pin].isTempSens = _isTempSens;
    pinStatus[_pin].status = _status;
    if (_isTempSens == true) {
        pinStatus[_pin].temp = _temp;
    }
  }
}


