# Nivida Frontend

Ready-made frontend for the Nivida Blockchain-Based Transparent and Tamper-Resistant E-Bidding System.

## Run
Open `index.html` in a browser, or use VS Code Live Server.

## Connect your FastAPI backend
Edit `js/config.js`:
- `API_BASE_URL`
- endpoint paths if your backend routes differ

The frontend is designed to work with your existing backend. It includes a mock-data fallback so the UI can be previewed before the API is connected.

## Blockchain
Edit `blockchain/contract-config.js`:
- `CONTRACT_ADDRESS`
- `CONTRACT_ABI`
- `GANACHE_RPC_URL`

MetaMask connection is already scaffolded in `js/blockchain.js`.

## Main pages
- `index.html` - login
- `dashboard.html` - dashboard
- `tenders.html` - tender list
- `create-tender.html` - create tender
- `tender-details.html` - tender details
- `place-bid.html` - place bid
- `my-bids.html` - bidder bids
- `audit.html` - audit trail
- `verification.html` - hash verification
- `reports.html` - reports
