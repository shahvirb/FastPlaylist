import gmusicapi
import logging
import getpass
import gcredentials
import jellyfish

logging.basicConfig(level=logging.DEBUG)

def get_authenticated_client():
    gmapi = gmusicapi.Mobileclient()
    email = gcredentials.EMAIL_HARDCODE
    logging.info("Attempting login as {} with android ID {}".format(email, gcredentials.AID_HARDCODE))
    success = gmapi.login(email, getpass.getpass(), gcredentials.AID_HARDCODE)
    logging.info('Logged in: {}'.format(success))
    return gmapi


def find_songs(results, filter):
    tracks = []
    for hit in results['song_hits']:
        track = hit['track']
        keys = set(filter.keys()).intersection(track.keys())
        matches = [jellyfish.match_rating_comparison(track[key], filter[key]) for key in keys]
        if not False in matches:
            tracks.append(track)
    return tracks