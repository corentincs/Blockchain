### A More Secure Online Voting System
##Brief Overview
We are developing a voting system based on blockchain technology. Instead of traditional binary voting, voters will assign a score ranging from 1 (strongly disagree) to 5 (strongly agree) for each proposal.

In this project, we will construct a blockchain where votes function as transactions. These votes will later be retrieved to determine the election results.

Once the blockchain is built, our goal is to design a user-friendly graphical interface, allowing users to cast their votes seamlessly.

##Implementation of the Condorcet Method
We will integrate a counting function within the blockchain class that will first aggregate the votes to populate a matrix representing pairwise preferences. If no clear winner emerges from this initial stage, we will use the ranked pairs method to determine the final outcome.

##Blockchain Creation
For the blockchain creation, we will use Python’s class system.

Blocks will be created in the block.py file. Each block will be an instance of the Block() class, with attributes including: the block index (.index), timestamp of creation (.timestamp), the transactions contained within the block (.transactions), proof of work (.proof), and the hash of the previous block (.previous_hash). The blocks will be mined using the mine() function to generate proof of work, and the blocks will be hashed using the hash() function. Once created, the validity of each block is verified—ensuring proof of work is completed correctly (valid_proof()), that the transactions are valid, and that the block does not exceed the transaction limit.

Next, the blocks are linked in the blockchain.py file. The blockchain will be an object with attributes for the mempool (.mempool) and the blocks that form the chain (.blocks). The mempool will manage transactions via the add_transaction() function, which adds transactions to the mempool. Once enough transactions are gathered, a new block is created with new_block() and added to the chain using extend_chain().

##Web Interface
The web interface will be managed in the web.py file. We will start by creating a Flask app and assigning a unique address for each node. Next, we will create a blockchain object (using the previously defined Block class) and apply several methods. Users can vote through the POST /vote endpoint, which submits their candidate choice into the mempool. When the mempool reaches the set size (3 transactions per block), the blocks can be mined via the GET /mine endpoint. Election progress can be tracked using the GET /progress endpoint, which returns the number of votes for each candidate. Finally, the GET /nodes/resolve method ensures blockchain consensus.

The forms.py file allows users to select candidates during voting.

##Required Modules
The following Python libraries are required for the program to run properly: rich, ecdsa, cryptography, Flask, and requests. The rich library is used for display formatting, ecdsa handles key creation, cryptography manages encryption, and Flask and requests allow server creation and interaction.

##Authors and Acknowledgements
Special thanks to Marc-Antoine Weisser for his guidance and support.

GARREAU Corentin
