import json
import pandas as pd
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import pandas as pd
from sklearn.utils import shuffle
import coloredlogs, logging
import time


logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)


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
songs = shuffle(pd.read_csv("songdata.csv"))[['song', 'artist']][:5000]

ids = []
feats = []
song_count = 1
pkl_ids = pd.read_pickle("ids.pkl")
pkl_feats = pd.read_pickle("features.pkl")
# use this function here to aggregate track ids
for i, s in enumerate(songs.iterrows()):
    # skip duplicates
    if s[1].song in map(lambda s: s[2], pkl_ids):
        logger.warning("Duplicate [%s] found!" % s[1].song)
        continue
    try:
        result = sp.search(s[1].song, limit=1, offset=0, type='track', market=None)
        logger.debug(result["tracks"]["items"])
        track_id = result["tracks"]['items'][0]["id"]
        artist_id = result["tracks"]['items'][0]["artists"][0]["id"]
        album_id = result["tracks"]['items'][0]["album"]["id"]

        logger.info("[%d] Processing %s : %s --- track_id: %s artist_id: %s album_id: %s" % (song_count, s[1].artist, s[1].song, track_id, artist_id, album_id))

        # append 4-element tuple (653FhwnB8YXSwqbuPn8eB4, Mac Miller, BDE Bonus, 4LLpKhyESsyAXpc4laK94U, 0ETFjACtuP2ADo6LFhL6HN)
        ids.append((track_id, s[1].artist, s[1].song, artist_id, album_id))
        ft = sp.audio_features(tracks=[track_id])
        logger.debug("\n%s Feature: %s" % (s[1].song, ft))
        feats.append(ft[0])
        popl = sp.track(track_id)["popularity"]
        art_followers = sp.artist(artist_id)
        song_date = sp.album(album_id)["release_date"]
        logger.debug(feats[song_count - 1])
        feats[song_count - 1].update({"artist": s[1].artist, "song": s[1].song, "popularity": popl, "artist_followers": art_followers["followers"]["total"], "release_date": song_date})        
        
        # create pkl here, just in case 
        pd.to_pickle(ids + pkl_ids, "ids.pkl")
        pd.to_pickle(feats + pkl_feats, "features.pkl")
        song_count += 1
    except Exception as e:
        logger.error("%s, %s --- on %s" % (type(e), e, s[1].song))
        # time.sleep(3)


with open("features.json", "w") as f:
    json.dump(pd.read_pickle("features.pkl") + feats, f, indent=4)


logger.info("Successfully added features for %d track ids (see features.json or .pkl file)" % (song_count - 1))


# feats = []
# feat_count = 0
# for i, d in enumerate(ids):
#     try:
#         feats.append(sp.audio_features(tracks=[d[0]]))
#         popl = sp.track(d[0])["popularity"]
#         art_followers = sp.artist(d[3])
#         song_date = sp.album(d[4])["release_date"]
#         feats[i][0].update({"artist": d[1], "song": d[2], "popularity": popl, "artist_followers": art_followers["followers"]["total"], "release_date": song_date})
#         logger.info("[%d] Added features for %s " % (feat_count, d[2]))
#         feat_count += 1
#     except:
#         logger.warning("%s did not yield audio features!!!" % d[2])
# with open("features.json") as f:
#     real_data = json.loads(f.read())



