# Un système de vote en ligne plus sûr

## Brève description

On travaille sur un système de vote se basant sur la blockchain. Le vote ne sera pas binaire mais on attribuera une note entre 1 (peu d'accord) et 5 (très d'accord) à chaque proposition. 

Nous allons donc construire une blockchain où les votes auront le rôle des transactions. Il faudra ensuite récupérer ces votes pour obtenir le résultat de l'élection. 

Une fois que nous aurons fabriqué cette blockchain, le but est de créer une interface graphique afin que les utilisateurs puissent voter facilement.

## Implémentation du scrutin de Condorcet


## Création du serveur

Pour la création du serveur nous allons nous baser sur le TP "Learn Blockchains by Building One" de HackerNoon. Nous créerons notre serveur avec la bibliothèque *flask*.

## Création de la blockchain

Pour fabriquer la blockchain, on utilise le système de classe de Python. 

On crée les blocs dans le fichier _block.py_. 
Les blocs sont les instances de la class **Block()** ayant pour attributs : l'index du bloc (.index), le timestamp de la création (.timestamp), les transactions contenues dans le bloc (.transactions), la preuve de travail (.proof) ainsi que le hash du précédent bloc (.previous_hash).
On mine les blocs avec la fonction **mine()** qui nous permet d'avoir une preuve de travail et on hash les blocs avec la fonction **hash()**
On vérifie ensuite la validité des blocs qui sont construits : si la preuve de travail a été correctement effectuée (**valid_proof()**), si les transactions sont bien correctes et si le nombre de transactions contenues dans le bloc ne dépasse pas la taille du bloc.

On va ensuite lier les blocs entre eux dans le fichier _blockchain.py_.
La blockchain va être un objet ayant pour attribut le mempool (.mempool) et les blocs formant la blockchain (.blocks).
On s'occupe ensuite du mempool : la fonction **add_transaction()** permet de rajouter une transaction au mempool. Une fois qu'il y a un assez grand nombre de transactions dans le mempool, on crée un bloc avec **new_block()**. Enfin on ajoute le bloc à la blockchain avec **extend_chain()**.

## Interface web


## Modules nécessaire au fonctionnement

Pour faire tourner correctement notre programme, nous aurons besoins des bibliothèques suivantes : rich, ecdsa, cryptography, Flask, requests. 
La bibliothèque *rich* sera utilisé pour l'affichage, *ecdsa* permet de créer des clés, *cryptography* sera utilisé pour tous les encryptages, *Flask* et *requests* permettront de créer le serveur et d'interagir avec lui.

## Auteurs et remerciements
Merci à Marc-Antoine Weisser pour ses explications et son aide.

GARREAU Corentin, MACHABERT Guillaume, REMOUÉ Arthur.

