<h1 align="center">Musique Roulette</h1>

Création d’un jeu alliant musique et stratégie. Le programme python génère automatiquement une page html permettant de jouer les musiques des di fférents joueurs sur un navigateur quelconque. Idéal pour jouer en famille ou entre amis.
</br></br>
<h3 align="center">Mise en place</h3>
Le programme necessite les bibliothèques suivantes :
<ul>
<li>deezer_python</li>
<li>spotipy</li>
<li>requests</li>
</ul>
</br>
Executez le programme python avec un shell car il faut pouvoir intéragir à travers le shell. </br>
Si c'est la première fois que vous le lancez, vous n'avez qu'une seule possibilié : tapez "0" pour ajouter un nouveau joueur.
</br></br>
Pour chaque joueur ajouté, il faut : 
<ul>
<li>Renseigner son nom (unique)</li>
<li>Renseigner les playlists que le joueur écoute le plus souvent avec un lien Deezer ou Spotify (La playlist doit être publique !!!)</li>
</ul>
</br>
Une fois que tous les joueurs ont été créés et selectionnés, appuyez sur la touche Entrée, et renseignez le nombre de musiques que vous voulez générer. 
</br></br>
Une fichier html sera créé, il sufira ensuite de l'executer avec votre navigateur préféré. La page est alors plutôt intuitive à utiliser.
</br></br>
<h3 align="center">Règles du jeu</h3>

Si vous voulez ajouter de la compétitivité au jeu, voici des possibles règles.
</br></br>
On suppose qu'il y a n joueurs. À chaque tour, au bout des 30 secondes de reproduction de la musique, et après une discussion entre les joueurs, ceux-ci votent pour la personne dont ils croient que la musique appartient. Si quelqu'un pense qu'une musique est à lui, il doit essayer de mentir pour faire croire qu'elle ne lui appartient pas.
</br></br>
Après les votes, les joueurs se voient attribuer les points suivants :
<ul>
<li>La partie entière de n/2 points si le joueur a réussi à trouver la bonne personne (excepté lui-même)</li>
<li>(-1) points si le joueur ne s'est pas voté lui-même alors qu'il s'agissait de sa propre musique</li>
<li>À l'inverse, si le joueur dont la musique appartient s'est voté lui-même, alors il gagne 1 point par joueur qui ne l'a pas voté</li>
</ul>
</br>
À la fin du jeu, le joueur avec le plus de points gagne.
