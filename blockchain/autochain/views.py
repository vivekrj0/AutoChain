from django.shortcuts import render,HttpResponse
from time import time
from uuid import uuid4
from urllib.parse import urlparse

import json
import hashlib
import requests


class Autochain():
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash=1, proof=100)
        self.nodes = set()


    def register_node(self, address):
        """
        Add new node to the list of nodes
        address: Address of node. Eg. 'http://192.168.0.5:5000'
        """

        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'.
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')

    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            if block['previous_hash'] != self.hash(last_block):
                return False

            if not self.valid_proof(last_block['proof'], block['proof'], last_block['previous_hash']):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):

        neighbours = self.nodes
        new_chain = None

        # Look only for chains longer than current
        max_length = len(self.chain)

        # Find and verify the chains from all the nodes in network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True

        return False

    def new_block(self, proof, previous_hash=None):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": time(),
            "transactions": self.current_transactions,
            "proof": proof,
            "previous_hash": previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, owner, receiver, amount, vec_id):
    
        self.current_transactions.append({
            'owner': owner,
            'receiver': receiver,
            'amount': amount,
            'vec_id':vec_id
            
        })
        return self.last_block['index'] + 1


    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_block):
        last_proof = last_block['proof']
        last_hash = self.hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


node_identifier = str(uuid4()).replace("-", "")
# Instantiate the Blockchain
blockchain = Autochain()


def mine(request):
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)
    print(proof)
    blockchain.new_transaction(
        owner="0",
        receiver=node_identifier,
        amount=1,
        vec_id=0
    )
    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)
    response = {
        "message": "New Block Forged",
        "index": block["index"],
        "transactions": block["transactions"],
        "proof": block["proof"],
        "previous_hash": block["previous_hash"],
    }
    print(response)
    return HttpResponse(json.dumps(response))


def new_transaction(request):
    values = {
        "owner": "one address",
        "receiver": "other address",
        "amount": 5,
        "vec_id": 12345
    }

    # Check that the required fields are in the POST'ed data
    required = ['owner', 'receiver', 'amount', 'vec_id']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['owner'], values['receiver'], values['amount'], values['vec_id'])

    response = {'message': f'Transaction in queue to be added to Block {index}. Hit mine to record the transaction'}
    return HttpResponse(json.dumps(response))


def full_chain(request):
    response = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain),
    }
    return HttpResponse(json.dumps(response))

def register_nodes(request):
    values = {
        "owner": "one address",
        "receiver": "other address",
        "amount": 5,
        "vec_id": 12345
    }


    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message'     : 'New nodes have been added',
        'total_nodes' : list(blockchain.nodes)
    }
    return HttpResponse(json.dumps(response))

def consensus(request):
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message'   : 'Our Chain was replaced',
            'new_chain' : blockchain.chain
        }
    else:
        response = {
            'message' : 'Our chain is authoritative',
            'chain' : blockchain.chain
        }
    return HttpResponse(json.dumps(response))