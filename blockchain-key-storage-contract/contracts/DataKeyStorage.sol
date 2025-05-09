// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";

contract DataKeyStorage is Ownable {
    // Mapping of sensor ID to encryption key hash
    mapping(string => bytes32) private keyStorage;
    uint256 public keyCount;

    event KeyStored(string indexed sensorId, bytes32 keyHash, uint256 timestamp);

    constructor() Ownable(msg.sender) {}

    // Stores encrypted key hash (accessible by contract owner only)
    function storeEncryptionKey(string memory sensorId, bytes32 keyHash) external onlyOwner {
        keyStorage[sensorId] = keyHash;
        keyCount++;
        emit KeyStored(sensorId, keyHash, block.timestamp);
    }

    function getEncryptionKey(string memory sensorId) external view returns (bytes32) {
        return keyStorage[sensorId];
    }
}
