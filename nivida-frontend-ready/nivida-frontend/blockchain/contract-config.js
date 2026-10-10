// Replace these placeholders with your deployed Solidity contract details.
// Do NOT put private keys or seed phrases in frontend files.

const CONTRACT_ADDRESS = "0x4bc23b202ba76545dbe79649cbd86741b7e8a8ec";

const CONTRACT_ABI = [
 [
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "string",
				"name": "bidId",
				"type": "string"
			},
			{
				"indexed": false,
				"internalType": "string",
				"name": "bidHash",
				"type": "string"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			}
		],
		"name": "BidHashStored",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_bidId",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_bidHash",
				"type": "string"
			}
		],
		"name": "storeBidHash",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_bidId",
				"type": "string"
			}
		],
		"name": "getBidHash",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
];
