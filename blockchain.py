from flask import Flask, jsonify, request
import hashlib
import json
from uuid import uuid4
from time import time
class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        # Create the genesis block
        self.new_block(previous_hash = '1', proof = 100)

    def new_block(self, proof, previous_hash = None):
        """
        Creates a new Block and adds it to the blcokchain
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of the previous block
        :return: <dict> New Block
        """
        block = {
            'index'     : len(self.chain) + 1,
            'timestamp' : time(),
            'transactions' : self.pending_transactions,
            'proof' : proof,
            'previous_hash' : previous_hash or self.hash(self.chain[-1])

        }

        # Reset the current list of transactions
        self.pending_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined block
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        """

        self.pending_transactions.append({
            "sender" : sender,
            "recipient" : recipient,
            "amount" : amount
        })
        
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: <dict> Block
        :return: <str>
        """
        # We must make sure that the Dictionary is ordered, or we will have inconsistent hashes
        block_string = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @staticmethod
    def proof_of_work(block):
        """
        Proof-of-Work algorithm.
        Iterate the "proof" field until the conditions are satisfied.
        :param block: <dict>
        """
        while not Blockchain.valid_proof(block):
            block["proof"] += 1

    @staticmethod
    def valid_proof(block):
        """
        The Proof-of-Work conditions.
        Check if the hash of the block starts with 4 zeroes.
        Higher difficulty == more zeroes, lower difficulty == less.
        :param block: <dict>
        """
        return Blockchain.hash(block)[:4] == "0000"

    @property
    def last_block(self):
        """Returns the last Block in the chain"""
        return self.chain[-1]

    # Instance our Node
    app = Flask(__name__)

    # Generate a globally unique address for this node
    node_identifier = str(uuid4()).replace('-', '')

    # Instance the Blockchain
    blockchain = Blockchain();

    @app.route('/mine', methods = ["GET"])
    def mine():
        return "We will mine a new block"

    @app.route('/transactions/new', methods = ["POST"])
    def new_transaction():
        return "We will add a new transaction"

    @app.route('/chain', methods = ["GET"])
    def full_chain():
        response = {
            'chain': blockchain.chain,
            'length': len(blockchain.chain)
        }
        return jsonify(response), 200

    if __name__=="__main__":
        app.run(host='0.0.0.0', port=5000)

if __name__=="__main__":
    blockchain = Blockchain()
    blockchain.proof_of_work(blockchain.last_block)
    print(blockchain.hash(blockchain.last_block))

    blockchain.new_transaction("Alice", "Bob", 50)
    blockchain.new_block(0)
    print(blockchain.hash(blockchain.last_block))