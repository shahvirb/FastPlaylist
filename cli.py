import gmusic
import logging

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    gmapi = gmusic.get_authenticated_client()
    #search = input('Search: ')
    filter = {'title': 'Sweet Child O\' Mine',
              'artist':'guns n\ roses',
              'album': 'Appetite for Destruction'}
    search = filter['title']
    results = gmapi.search(search)
    tracks = gmusic.find_songs(results, filter)
    import pprint
    pprint.pprint(tracks[0:2])