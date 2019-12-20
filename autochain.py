import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4

import requests
from flask import Flask, jsonify, request

"""

A decentralized peer ­to­ peer blockchain for the network for automobile ownership.
The idea is to have a way to ensure that at every trasaction is tracked and accounted.
The concept that all the digital events or each transaction that have been executed are encoded in the public ledger
Vec_id listed here could correspond to the serial id of the Vehicle.

"""

class Autochain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()

        # Create the first block - Let there be light
        self.new_block(previous_hash='1', proof=100)

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
        """
        Blockchain validation
        return: True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof'], last_block['previous_hash']):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        This is our network consensus algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        Our logic here is that the longest chain is the most valid chain.
        return: True if our chain was replaced, False if not
        """

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

                # Check to see if length is longer than current and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False

    def new_block(self, proof, previous_hash):
        """
        Create a new block in the blockchain.
        We use the hash of the previous block as part of the immutability of the blockchain
        proof: The proof given by the proof of work algorithm
        previous_hash: Hash of previous block
        return: New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, owner, receiver, amount, vec_id):
        """
        Creates a new transaction thats queued for the next mined Block
        owner: ID of the current vehicle owner
        receiver: ID of the buyer 
        amount: Amount paid in the transaction
        vec_id: Unique vehicle id for the vehicle that's being transacted
        return: The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            'owner': owner,
            'receiver': receiver,
            'amount': amount,
            'vec_id':vec_id
            
        })
        """
        You can include a validation function here <optional>.
        The goal of such a function would be to check against a database to see if it's a valid vehicle serial ID.
        """

        return self.last_block['index'] + 1
    
    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Every block in the network needs a signature -> Reinforces uniqueness and immutability
        We can do that by hashing our block dictionary with SHA-256 hash.
        Creates a SHA-256 hash of a Block
        block: block dictionary
        return: hashed string
        """
        
        """
        The entire dictionary will be hashed.
        We must make sure that the information in the Dictionary is ordered, 
        or we'll have inconsistent hashes across different transactions.
        """

        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_block):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes
         - Where p is the previous proof, and p' is the new proof
         
        last_block: last Block
        return: proof as an integer number
        """

        last_proof = last_block['proof']
        last_hash = self.hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        """
        Validates the Proof
        last_proof: Previous Proof
        proof: Current Proof
        last_hash: The hash of the Previous Block
        return: True if correct, False if not.
        """

        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


# Instantiate the Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Autochain()


@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    # Reward transactions have vec_id as 0 to distinguish them.
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
    required = ['owner', 'receiver', 'amount', 'vec_id']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['owner'], values['receiver'], values['amount'], values['vec_id'])

    response = {'message': f'Transaction in queue to be added to Block {index}. Hit mine to record the transaction'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods = ['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message'     : 'New nodes have been added',
        'total_nodes' : list(blockchain.nodes)
    }

    return jsonify(response), 201

@app.route('/nodes/resolve', methods = ['GET'])
def consensus():
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

    return jsonify(response), 200        

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    """
    Change the port number in the parameter: default - to fire up different nodes in the same system.
    The default port number is 5000
    """
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
