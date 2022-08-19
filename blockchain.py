import hashlib
import json
from time import time

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        # Create the genesis block
        self.new_block(previous_hash = '1', proof = 100)

    def new_block(self):
        # Creates a new Block and adds it to the blcokchain
        # :param proof: <int> The proof given by the Proof of Work algorithm
        # :param previous_hash: (Optional) <str> Hash of the previous block
        # :return: <dict> New Block
        block = {
            'index'     : len(self.chain) + 1,
            'timestamp' : time(),
            'transactions' : self.pending_transactions,
            'proof' : proof,
            'previous_hash' : previous_hash or self.hash(self.chain[-1])

        }

    def new_transaction(self, sender, recipient, amount):
        # Adds a new transaction to the list of transactions
        # Creates a new transaction to go into the next mined block
        # :param sender: <str> Address of the Sender
        # :param recipient: <str> Address of the Recipient
        # :param amount: <int> Amount
        # :return: <int> The index of the Block that will hold this transaction
        self.pending_transactions.append({
            "sender" : sender,
            "recipient" : recipient,
            "amount" : amount
        })
        
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        # Hashes a Block
        pass

    @property
    def last_block(self):
        # Returns the last Block in the chain
        pass


if __name__=="__main__":
    blockchain = Blockchain()
    print(blockchain.chain)