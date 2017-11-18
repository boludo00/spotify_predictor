import pandas as pd 

def make_csv_from_features(features):
    """
    Take in a pkl'd features object and create a csv, also returns the dataframe.
    """
    df = pd.DataFrame(data=features)
    df.drop(['analysis_url', 'track_href', 'type', 'uri'], axis=1, inplace=True)
    # re-order columns for visibility
    df = df[['artist', 'song', 'artist_followers', 'release_date', 'acousticness', 'danceability', 'duration_ms', 'energy',
        'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence', 'popularity']]
    df.to_csv("spotify_data.csv")
    return df

def add_feature(song_name):
    """
    Given a song name, fetch it from the api and add it to the dataset.
    """
    pass