// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BidStorage {

    struct Bid {
        string bidId;
        string bidHash;
        uint256 timestamp;
    }

    mapping(string => Bid) private bids;

    event BidHashStored(
        string bidId,
        string bidHash,
        uint256 timestamp
    );

    function storeBidHash(
        string memory _bidId,
        string memory _bidHash
    ) public {

        bids[_bidId] = Bid(
            _bidId,
            _bidHash,
            block.timestamp
        );

        emit BidHashStored(
            _bidId,
            _bidHash,
            block.timestamp
        );
    }

    function getBidHash(
        string memory _bidId
    ) public view returns (
        string memory,
        uint256
    ) {

        Bid memory bid = bids[_bidId];

        return (
            bid.bidHash,
            bid.timestamp
        );
    }
}