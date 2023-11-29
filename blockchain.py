"""
This module contains the class Blockchain. A blockchain is a list of blocks and a mempool.
"""
import json
import random
import config
from block import Block, InvalidBlock
from transaction import Transaction
import utils

import requests
from uuid import uuid4

from flask import Flask, jsonify, request


class Blockchain(object):
    def __init__(self):
        self.mempool = []
        self.blocks = [Block()]

    @property
    def last_block(self):
        return self.blocks[-1]

    def add_transaction(self, transaction):
        """
        Add a new transaction to the mempool. Return True if the transaction is valid and not already in the mempool.
        :param transaction:
        :return: True or False
        """
        if transaction.verify() and transaction not in self.mempool and utils.str_to_time(transaction.date) >= utils.str_to_time(utils.get_time()) : 
            self.mempool.append(transaction)
            return True
        else : 
            return False

    def new_block(self, block=None):
        """
        Create a new block from transactions choosen in the mempool.
        :param block: The previous block. If None, the last block of the chain is used.
        :return: The new block
        """
        if not block : 
            block = self.last_block
        
        data = {
            "index" : block.index + 1,
            "timestamp" : utils.get_time(),
            "transactions" : self.mempool[0:min(config.blocksize, len(self.mempool))] ,
            "proof" : 0,
            "previous_hash" : block.hash()
            }

        return Block(data)

    def extend_chain(self, block):
        """
        Add a new block to the chain if it is valid (index, previous_hash, proof).
        :param block: A block
        :raise InvalidBlock if the block is invalid
        """
        if block.valid_proof() and block.index == self.last_block.index +1 and self.last_block.hash() == block.previous_hash :
            self.blocks.append(block)
            for t in block.transactions : self.mempool.remove(t)
            
        else : raise InvalidBlock
        return

    def __str__(self):
        """
        String representation of the blockchain
        :return: str
        """
        self.log()
        return ""
    def validity(self):
        """
        Check the validity of the chain.
        - The first block must be the genesis block
        - Each block must be valid
        - Each block must point to the previous one
        - A transaction can only be in one block
        :return: True if the chain is valid, False otherwise
        """
        genesis = self.blocks[0] == Block() 
        validity = [block.validity() for block in self.blocks] == [True]*len(self)
        chain = [self.blocks[i].hash() == self.blocks[i+1].previous_hash for i in range(len(self) - 1 )] == [True]*(len(self)-1)
        all_transaction = []
        for b in self.blocks : 
            for transaction in b.transactions : 
                if transaction in all_transaction : 
                    return False 
                else :
                    all_transaction.append(transaction)

        return genesis and validity and chain
    
    def __len__(self):
        """
        Return the length of the chain
        :return:
        """
        return len(self.blocks)

    def merge(self, other):
        """
        Modify the blockchain if other is longer and valid.
        :param other:
        :return:
        """
        if len(other) > len(self) and other.validity() : 
            self.blocks = other.blocks[:]

            all_transaction = []
            for b in self.blocks : 
                for transaction in b.transactions : 
                    all_transaction.append(transaction)
            for transaction in self.mempool : 
                if transaction in all_transaction : self.mempool.remove(transaction)
            
            for transaction in other.mempool : 
                if transaction not in self.mempool() : 
                    self.mempool.append(transaction)
        
        return self 

    def log(self):
        
        Transaction.log(self.mempool)

        for b in self.blocks:
            b.log()

# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200
  
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

#curl -X POST -H "Content-Type: application/json" -d '{
# "nodes": ["http://127.0.0.1:5000/"]}' "http://localhost:5000/nodes/register"

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)