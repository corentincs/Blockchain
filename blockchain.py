"""
This module contains the class Blockchain. A blockchain is a list of blocks and a mempool.
"""
import json
import random
import config
from block import Block, InvalidBlock
from transaction import Transaction
import utils


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
            # En période de test, on ajoute la transaction quoi qu'il arrive !
            self.mempool.append(transaction)

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
        #if block.valid_proof() and block.index == self.last_block.index +1 and self.last_block.hash() == block.previous_hash :
        self.blocks.append(block)
        for t in block.transactions : self.mempool.remove(t)
            
        #else : raise InvalidBlock
        return

    def __str__(self):
        """
        String representation of the blockchain
        :return: str
        """
        return str([str(block) for block in self.blocks])

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
