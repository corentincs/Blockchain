from flask import Flask, jsonify, request, render_template, redirect
from blockchain import Blockchain
from block import Block, InvalidBlock
from transaction import Transaction
import requests
from uuid import uuid4

# Instantiate our Node
app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key_here'
# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    new_block = blockchain.new_block()
    blockchain.extend_chain(new_block)

    return redirect('/avancement')

#curl -X POST -H "Content-Type: application/json" -d '{
# "message": "I put my vote"}' "http://localhost:5000/transactions/new"


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': str(blockchain),
        'mempool':str(blockchain.mempool),
        'length': len(blockchain.blocks),
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


from forms import TransactionForm

@app.route('/', methods=['GET'])
def accueil():
    return render_template('accueil.html')



@app.route('/voter', methods=['GET', 'POST'])
def voter():

    if request.method == 'POST':

        votes = [request.form.get("choix"+str(i)) for i in range(1, 6)]

        # Check that the required fields are in the POST'ed data
        #required = ['message']
        #if not all(k in values for k in required):
        #    return 'Missing values', 400

        transaction = Transaction(votes=votes)
        blockchain.add_transaction(transaction)

        # Create a new Transaction
        #index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

        # return redirect('/voter')

    form = TransactionForm()

    return render_template('voter.html', form=form)

@app.route('/avancement', methods=['GET'])
def avancement():
    mempool_data = blockchain.mempool

    resultats = [0, 0, 0, 0, 0]
    voix = {'candidat1':0, 'candidat2':0, 'candidat3':0, 'candidat4':0, 'candidat5':0,}
    for block in blockchain.blocks:

        for transaction in block.transactions:
            for i, candidat in enumerate(transaction.votes):
                voix[candidat] += i

    #vainqueur = blockchain.comptage()

    return render_template('avancement.html', mempool_data=mempool_data, voix=voix, blockchain=blockchain)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)