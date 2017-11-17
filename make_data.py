import pandas as pd
import requests
import spotipy
import json
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import pandas as pd
from sklearn.utils import shuffle

# read credentials and set them
with open("credentials.json") as f:
    creds = json.loads(f.read())
client_id, client_secret = creds["client_id"], creds["client_secret"]

token = util.prompt_for_user_token("Giancarlo Perrone",
                                   "user-library-read",
                                   client_id=client_id,
                                   client_secret=client_secret,
                                   redirect_uri='http://127.0.0.1')
print token

sp = spotipy.Spotify(auth="BQAXqXOsfTwFIc8YDcRMN33cH5v0ZFKLH7uYMtGMlP0eZUYZB8jojC-bo5OA929qBUBS6WxJ6-4AZwgMDslzuIa-NA0GhmUfbKxltP4ls-49kh21O5Sy9nBfw8pdHV7QRFeqaIN62cgcNGTYud0kYLA")
songs = shuffle(pd.read_csv("songdata.csv"))[['song', 'artist']][:10]

ids = []
# use this function here to aggregate track ids
# print json.dumps(sp.search("despacito", limit=10, offset=0, type='track', market=None), indent=4)["tracks"]
for s in songs.iterrows():
    try:
        track_id = sp.search(s[1].song, limit=10, offset=0, type='track', market=None)["tracks"]['items'][0]["id"]
        ids.append((track_id, s[1].artist))
        print "%s : %s added to data with track id %s" % (s[1].artist, s[1].song, track_id)
    except:
        print "%s not found" % s[1].song

feats = []
for i, d in enumerate(ids):
    feats.append(sp.audio_features(tracks=[d[0]]))
    feats[i][0].update({"artist": d[1]})

with open("features.json", "w") as f:
    json.dump(feats, f)

objs = map(lambda x: x[0], feats)
df = pd.DataFrame(data=objs)
df.set_index('id', inplace=True)
df.drop(['analysis_url', 'track_href', 'type', 'uri'], axis=1, inplace=True)
df.to_csv("data1.csv")