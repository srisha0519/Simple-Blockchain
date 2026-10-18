
import hashlib
import json
import time


class Block:
    def __init__(self, index, timestamp, data, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }

        encoded_data = json.dumps(
            block_data, sort_keys=True
        ).encode()

        return hashlib.sha256(encoded_data).hexdigest()

    def mine_block(self, difficulty):
        target = "0" * difficulty

        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()

        print(f"Block {self.index} mined: {self.hash}")


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 3

    def create_genesis_block(self):
        return Block(
            0, time.time(), "Genesis Block", "0"
        )

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        previous_block = self.get_latest_block()

        new_block = Block(
            len(self.chain),
            time.time(),
            data,
            previous_block.hash
        )

        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False

            if current.previous_hash != previous.hash:
                return False

            if not current.hash.startswith(
                "0" * self.difficulty
            ):
                return False

        return True

    def display_chain(self):
        for block in self.chain:
            print("\n" + "=" * 50)
            print(f"Block Index: {block.index}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Data: {block.data}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Nonce: {block.nonce}")
            print(f"Hash: {block.hash}")


if __name__ == "__main__":
    blockchain = Blockchain()

    print("SIMPLE BLOCKCHAIN PROJECT")
    print("-" * 50)

    blockchain.add_block({
        "sender": "Alice",
        "receiver": "Bob",
        "amount": 10
    })

    blockchain.add_block({
        "sender": "Bob",
        "receiver": "Charlie",
        "amount": 5
    })

    blockchain.display_chain()

    print("\nIs blockchain valid?",
          blockchain.is_chain_valid())

    print("\nTesting tampering...")
    blockchain.chain[1].data = {
        "sender": "Alice",
        "receiver": "Bob",
        "amount": 1000
    }

    print("Is blockchain valid after tampering?",
          blockchain.is_chain_valid())