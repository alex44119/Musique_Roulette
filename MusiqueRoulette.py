# !!! On augmente la probabilité d'apparition de ceux qui ne sont pas choisis
ajoutProba = 0.05 # Cela ne change presque rien

# Gestion des joueurs à part

joueursPath = "joueurs.txt"

try:
    file = open(joueursPath, "r")
    joueursData = file.readlines()
    file.close()
except:
    file = open(joueursPath, "w")
    joueursData = []
    file.close()

joueursData = [j.strip().split("||") for j in joueursData]

import random as rd
import requests
import deezer
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

checkNotAllowed = True

### Deezer Initialization ###

de = deezer.Client()

### Spotify Initialization ###
 
cid = "1bab44b7ca794174a20810e1dc532c61"
secret = "7cf8ad27412e46049db8e94600ff7536"
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

### Chargement des joueurs ###

players = [(j[0], j[1].split(";;;"), j[2]) for j in joueursData]
players4game = []

def choosePlayer():
    demande = "Choose players :"
    for (i, j) in enumerate(players) :
        try:
            index = [p[0] for p in players4game].index(j[0])
        except:
            index = -1
        if index == -1:
            demande += f"\n {i+1} : {j[0]}\n"
        else:
            demande += f"\n➡{i+1} : {j[0]}\n"
    rep = input(demande+"\n 0 : Add a player\nElse, press enter to play\n\n")
    if rep == "" :
        return players4game
    rep = int(rep)
    if rep == 0:
        print("New player\n")
        name = input("Name : ")
        nplaylists = int(input(f"How many playlists for {name} ? "))
        link = [input(f"Playlist{i+1} Link : ") for i in range(nplaylists)]
        if link[0].find("deezer") != -1:
            plaform = "de"
            print("\nPlatform detected : Deezer")
            ID = []
            for (i, li) in enumerate(link):
                a = li.find("link")
                if a == -1:
                    a = li.find("playlist")
                    if a == -1:
                        print("The link{i+1} isn't valid.")
                    else:
                        ID.append(li[a+4:a+4+10])
                        print(f"ID{i+1} detected : {ID[-1]}")
                else:
                    req = requests.get(li).text
                    b = req.find('<meta property="og:url" content="https://www.deezer.com/fr/playlist/')
                    ID.append(req[b+68:b+68+10])
                    print(f"ID{i+1} detected : {ID[-1]}")
            if len(ID) == nplaylists:
                players4game.append((name, ID, "de"))
                players.append((name, ID, "de"))
                print(f"{name} was successfully added !")
                
        elif link[0].find("spotify") != -1:
            plaform = "sp"
            print("\nPlatform detected : Spotify")
            ID = []
            for (i, li) in enumerate(link):
                a = li.find("playlist")
                if a == -1:
                    print("The link{i+1} isn't valid.")
                else:
                    ID.append(li[a+9:a+9+22])
                    print(f"ID{i+1} detected : {ID[-1]}")
            if len(ID) == nplaylists:
                players4game.append((name, ID, "sp"))
                players.append((name, ID, "sp"))
                print(f"{name} was successfully added !\n")
        else:
            print("The link isn't valid.")
    else:
        try:
            index = [p[0] for p in players4game].index(players[rep-1][0])
        except:
            index = -1
        if index == -1:
            players4game.append(players[rep-1])
        else:
            players4game.pop(index)
    choosePlayer()
    
choosePlayer()
N = int(input("How many rounds ?"))

### Enregistrement des joueurs ###

jData = "\n".join([f"{name}||{';;;'.join(ID)}||{platform}" for (name, ID, platform) in players])
players = players4game
file = open(joueursPath, "w")
file.write(jData)
file.close()

### Chargement des playlists ###

n = len(players)
poids = [1 for i in range(n)]
playlists = [[sp.playlist(p)["tracks"]["items"] for p in players[nbA][1]] if players[nbA][2] == "sp" else [de.get_playlist(p).get_tracks() for p in players[nbA][1]] for nbA in range(n)]

### File Path and Number of tracks - Can be changed ###
code = rd.randint(100, 999)
place = f"musiqueRoulette{code}.html"

txtPlay = """<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/></head><body><center>"""

def playlist(nbA):
    """Renvoie le couple (lien, auteur) = (str, str) de la musique à écouter"""
    playlist = rd.choice(playlists[nbA])
    assert (playlist), "La playlist ne contient pas assez de musiques"
    if players[nbA][2] == "sp":
        nb = rd.randint(0, len(playlist)-1)
        track = playlist.pop(nb)["track"]
        return (track["preview_url"], f'{nb}. {track["name"]} - {track["artists"][0]["name"]}')
    
    if players[nbA][2] == "de":
        nb = rd.randint(0, len(playlist)-1)
        track = playlist[nb]
        return (track.preview, f"{nb}. {track.title} - {track.artist.name}")
        
def rdpoids(poids):
    """renvoie un nombre aléatoire entre 0 et len(poids)-1 en prenant en compte le coeff"""
    return rd.choices(list(range(len(poids))), poids)[0]
        


for i in range(N):
    nbA = rdpoids(poids)
    trackAndAuthor = playlist(nbA)
    if checkNotAllowed :
        r = trackAndAuthor[0]
        while (not r):
            nbA = rd.randint(0,n-1)
            trackAndAuthor = playlist(nbA)
            r = trackAndAuthor[0]
    poids = [p+ajoutProba for p in poids]
    poids[nbA] = 1
    
# Attention : Il y aura forcément une erreur pour les titres contennant le signe "
    txtPlay += (f"""{i+1}<audio controls>
    <source src="{trackAndAuthor[0]}">
</audio></br>
<a id = "trackName{i+1}" href = "#/">Track name</a>  -  <a id = "resp{i+1}" href = "#/">Answer</a></br>
<script>
    function scriptTrack{i+1}(v) {{
        if (v){{
            document.getElementById("trackName{i+1}").innerHTML = "{trackAndAuthor[1]}";
        }} else {{
            document.getElementById("trackName{i+1}").innerHTML = "Track name";
        }}
    }};
    let var{i+1} = true;
    document.getElementById("trackName{i+1}").onclick = function () {{
        scriptTrack{i+1}(var{i+1});
        var{i+1} = !(var{i+1});
    }}
    function scriptResp{i+1}(vR) {{
        if (vR){{
            document.getElementById("resp{i+1}").innerHTML = "{players[nbA][0]}";
        }} else {{
            document.getElementById("resp{i+1}").innerHTML = "Answer";
        }}
    }};
    let varR{i+1} = true;
    document.getElementById("resp{i+1}").onclick = function () {{
        scriptResp{i+1}(varR{i+1});
        varR{i+1} = !(varR{i+1});
    }}
</script>""")

txtPlay += "</center></body></html>"

fil = open(place, 'w')

fil.write(txtPlay)

fil.close()

print(f"File was created : \n You can open {place}")
