import gmusicapi
import logging
import getpass
import gcredentials
import jellyfish

logging.basicConfig(level=logging.INFO)

def get_authenticated_client():
    gmapi = gmusicapi.Mobileclient()
    email = gcredentials.EMAIL_HARDCODE
    logging.info("Attempting login as {} with android ID {}".format(email, gcredentials.AID_HARDCODE))
    success = gmapi.login(email, getpass.getpass(), gcredentials.AID_HARDCODE)
    logging.info('Logged in: {}'.format(success))
    return gmapi


def search(client, phrase):
    return client.search(phrase)


def string_score(s1, s2):
    s1 = s1.lower()
    s2 = s2.lower()
    return jellyfish.jaro_distance(s1, s2)


def string_similar(s1, s2):
    similar = string_score(s1, s2) >= 0.8
    assert similar != None
    #print(s1, s2, jellyfish.match_rating_comparison(s1, s2), jellyfish.jaro_distance(s1, s2))
    return similar


def find_songs(client, results, filter):
    tracks = []
    for hit in results['song_hits']:
        track = hit['track']
        keys = set(filter.keys()).intersection(track.keys())
        matches = [string_similar(track[key], filter[key]) for key in keys]
        if not False in matches:
            tracks.append(track)
    return tracks


def find_albums(client, results, filter):
    albums = []
    for hit in results['album_hits']:
        hit = hit['album']
        keys = set(filter.keys()).intersection(hit.keys())
        matches = [string_similar(hit[key], filter[key]) for key in keys]
        assert len(matches) == len(keys)
        if not False in matches:
            album = client.get_album_info(hit['albumId'], include_tracks=True)
            score = string_score(hit['name'], filter['name'])
            albums.append((album, score))
    
    tracks = []
    for sorted_albums in sorted(albums, reverse=True, key=lambda x: x[1]):
        tracks += sorted_albums[0]['tracks']
        break # Only add the first album. Assumption: first result is the best result
    
    return tracks