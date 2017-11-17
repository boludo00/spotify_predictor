import pandas as pd
import requests
import spotipy
import json
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import pandas as pd
from sklearn.utils import shuffle

# read credentials and set them
"""with open("credentials.json") as f:
    creds = json.loads(f.read())
client_id, client_secret = creds["client_id"], creds["client_secret"]"""

"""token = util.prompt_for_user_token("Giancarlo Perrone",
                                   "user-library-read",
                                   client_id=client_id,
                                   client_secret=client_secret,
                                   redirect_uri='http://127.0.0.1')"""
#print token

sp = spotipy.Spotify(auth="BQBx6H7omP3A04hcT-wxuV20BtkoF1v-Wb5TcT_FM5__zl3H24IZ2u0MjUUOY4RhE2aegA4KU8vlt6NNPw7YrvpkswXqdjlnEx1YyxdEgWYz5Yel7kZClv9avK_nj8yWSqUCOn5InWzLxSU-u2FwNtY")

songs = shuffle(pd.read_csv("songdata.csv")).song[:100]

ids = []
# use this function here to aggregate track ids
# print json.dumps(sp.search("despacito", limit=10, offset=0, type='track', market=None), indent=4)["tracks"]
for s in songs:
    try:
        ids.append(sp.search(s, limit=10, offset=0, type='track', market=None)["tracks"]['items'][0]["id"])
    except:
        print "%s not found" % s

feats = []
for i in ids:
    feats.append(sp.audio_features(tracks=[i]))

with open("features.json", "w") as f:
    json.dump(feats, f)