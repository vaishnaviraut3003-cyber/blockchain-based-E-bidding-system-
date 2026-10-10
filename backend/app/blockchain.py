from web3 import Web3
import json
import os

# ==========================================
# 1. CONNECT TO GANACHE
# ==========================================

GANACHE_URL = "http://127.0.0.1:7545"

w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

if w3.is_connected():
    print("✅ Connected to Ganache")
    print("Chain ID:", w3.eth.chain_id)
    print("Latest Block:", w3.eth.block_number)
else:
    print("❌ Could not connect to Ganache")


# ==========================================
# 2. SMART CONTRACT DETAILS
# ==========================================

CONTRACT_ADDRESS = "0x73ccdf891ca9B105F58e336b85dE82378A0Ae9eC"

ABI_PATH = os.path.join(
    os.path.dirname(__file__),
    "abi.json"
)

with open(ABI_PATH, "r") as file:
    CONTRACT_ABI = json.load(file)

contract = w3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT_ADDRESS),
    abi=CONTRACT_ABI
)


# ==========================================
# 3. CHECK SMART CONTRACT
# ==========================================

try:
    contract.functions.getBidHash("1").call()
    print("✅ Smart contract found on blockchain")
except Exception as e:
    print("⚠️ Contract connection check failed:")
    print(e)


# ==========================================
# 4. STORE BID HASH ON BLOCKCHAIN
# ==========================================

def store_bid_hash(bid_id, bid_hash):

    account = w3.eth.accounts[0]

    nonce = w3.eth.get_transaction_count(account)

    transaction = contract.functions.storeBidHash(
        str(bid_id),
        str(bid_hash)
    ).build_transaction({
        "from": account,
        "nonce": nonce,
        "gas": 3000000,
        "gasPrice": w3.to_wei("20", "gwei")
    })

    tx_hash = w3.eth.send_transaction(transaction)

    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print("\n====================================")
    print("       BLOCKCHAIN BID STORAGE")
    print("====================================")
    print("Bid ID:", bid_id)
    print("Bid Hash:", bid_hash)
    print("Transaction Hash:", tx_hash.hex())
    print("Block Number:", receipt.blockNumber)
    print("Gas Used:", receipt.gasUsed)
    print("✅ Hash stored on blockchain")
    print("====================================\n")

    return tx_hash.hex()


# ==========================================
# 5. READ BID HASH FROM BLOCKCHAIN
# ==========================================

def get_bid_hash(bid_id):

    result = contract.functions.getBidHash(
        str(bid_id)
    ).call()

    blockchain_hash = result[0]

    return blockchain_hash


# ==========================================
# 6. VERIFY BID HASH
# ==========================================

def verify_bid_hash(bid_id, original_hash):

    blockchain_hash = get_bid_hash(bid_id)

    if blockchain_hash == original_hash:
        return True
    else:
        return False


# ==========================================
# 7. TEST BLOCKCHAIN CONNECTION
# ==========================================

if __name__ == "__main__":

    print("\n====================================")
    print("       BLOCKCHAIN TEST")
    print("====================================")

    print("Connected:", w3.is_connected())
    print("Chain ID:", w3.eth.chain_id)
    print("Latest Block:", w3.eth.block_number)
    print("Contract:", CONTRACT_ADDRESS)

    print("\nTesting bid hash storage...")

    test_bid_id = "1"
    test_hash = "abc123testhash"

    try:

        tx_hash = store_bid_hash(
            test_bid_id,
            test_hash
        )

        print("Transaction successful!")
        print("TX Hash:", tx_hash)

        stored_hash = get_bid_hash(
            test_bid_id
        )

        print("\nHash stored on blockchain:")
        print(stored_hash)

        result = verify_bid_hash(
            test_bid_id,
            test_hash
        )

        print("\nVerification result:")

        if result:
            print("✅ HASH MATCHES")
        else:
            print("❌ HASH DOES NOT MATCH")

    except Exception as e:

        print("\n❌ Blockchain test failed")
        print("Error:", e)