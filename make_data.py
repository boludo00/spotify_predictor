import json
import pandas as pd
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import pandas as pd
from sklearn.utils import shuffle
import coloredlogs, logging

logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO', logger=logger)


# read credentials and set them
with open("credentials.json") as f:
    creds = json.loads(f.read())
client_id, client_secret = creds["client_id"], creds["client_secret"]

token = util.prompt_for_user_token("Giancarlo Perrone",
                                   "user-library-read",
                                   client_id=client_id,
                                   client_secret=client_secret,
                                   redirect_uri='http://127.0.0.1')
# print token

sp = spotipy.Spotify(auth=token)

# do 1000 at a time
songs = shuffle(pd.read_csv("songdata.csv"))[['song', 'artist']][:1000]

ids = []
song_count = 0
# use this function here to aggregate track ids
for s in songs.iterrows():
    try:
        track_id = sp.search(s[1].song, limit=1, offset=0, type='track', market=None)["tracks"]['items'][0]["id"]
        artist_id = sp.search(s[1].song, limit=1, offset=0, type='track', market=None)["tracks"]['items'][0]["artists"][0]["id"]
        album_id = sp.search(s[1].song, limit=1, offset=0, type='track', market=None)["tracks"]['items'][0]["album"]["id"]
        # append 4-element tuple (653FhwnB8YXSwqbuPn8eB4, Mac Miller, BDE Bonus, 4LLpKhyESsyAXpc4laK94U, 0ETFjACtuP2ADo6LFhL6HN)
        ids.append((track_id, s[1].artist, s[1].song, artist_id, album_id))
        logger.debug("Processing %s : %s with track id %s artist id %s album id %s" % (s[1].artist, s[1].song, track_id, artist_id, album_id))
        logger.info("[%d] Processing %s : %s" % (song_count, s[1].artist, s[1].song))
        song_count += 1
        # create pkl here, just in case 
        pd.to_pickle(ids, "ids.pkl")
    except Exception as e:
        logger.warning("%s --- on %s" % (type(e), s[1].song))

# create pkl here, just in case 
# pd.to_pickle(ids, "ids.pkl")
logger.info("Successfully gathered info for %d tracks" % song_count)

feats = []
feat_count = 0
for i, d in enumerate(ids):
    try:
        feats.append(sp.audio_features(tracks=[d[0]]))
        popl = sp.track(d[0])["popularity"]
        art_followers = sp.artist(d[3])
        song_date = sp.album(d[4])["release_date"]
        feats[i][0].update({"artist": d[1], "song": d[2], "popularity": popl, "artist_followers": art_followers["followers"]["total"], "release_date": song_date})
        logger.info("[%d] Added features for %s " % (feat_count, d[2]))
        feat_count += 1
    except:
        logger.warning("%s did not yield audio features!!!" % d[2])

logger.info("Successfully added features for %d track ids" % feat_count)

# flatten the inner list in the object
feats = map(lambda x: x[0], feats)

with open("features.json", "w") as f:
    json.dump(feats, f, indent=4)

df = pd.DataFrame(data=feats)
df.drop(['analysis_url', 'track_href', 'type', 'uri'], axis=1, inplace=True)

# re-order columns for visibility
df = df[['artist', 'song', 'artist_followers', 'release_date', 'acousticness', 'danceability', 'duration_ms', 'energy',
        'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence', 'popularity']]
df.to_csv("data1.csv")