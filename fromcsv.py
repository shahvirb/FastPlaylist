import gmusic
import logging
import click
import csv

logging.basicConfig(level=logging.DEBUG)


def read_csv(filename):
    data = []
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            data.append({key: row[key] for key in reader.fieldnames if row[key] != ''})
        headers = reader.fieldnames
    return (data, headers)


@click.command()
@click.argument('filename')
@click.option('--create/--no-create', default=False, help='Creates a playlist')
@click.option('--name', default=None, help='Playlist name')
@click.option('--add', default='song', help='Which results to add. Defaults to \'song\'. Values = [\'song\', \'album\']' )
def main(filename, create, name, add):
    logging.info('Reading CSV File: {}'.format(filename))
    rows, headers = read_csv(filename)
    logging.info('{} data rows found with header: '.format(len(rows), headers))
    
    gmclient = gmusic.get_authenticated_client()
    tracks = []
    for row in rows:
        search = row[headers[0]]
        logging.info('Searching: \"{}\" - {}'.format(search, row))
        raw = gmusic.search(gmclient, search)
        hits = []
        if add == 'song':
            hits = gmusic.find_songs(gmclient, raw, row)
            hits = hits[0:1]
        if add == 'album':
            hits = gmusic.find_albums(gmclient, raw, row)
        if hits:
            for hit in hits:
                logging.info('Found: {} - {} - {}'.format(hit['title'], hit['artist'], hit['album']))
                tracks.append(hit)
        else:
            logging.warning('No results found for {}'.format(search))
    logging.info('Searched for {} rows and found {} tracks'.format(len(rows), len(tracks)))
    
    if create:
        if not name:
            name = filename
        plid = gmclient.create_playlist(name)
        logging.info('Created playlist {} as ID {}'.format(name, plid))
        song_ids = [track['storeId'] for track in tracks]
        gmclient.add_songs_to_playlist(plid, song_ids)
        logging.info('Added {} tracks to playlist'.format(len(song_ids)))


if __name__ == '__main__':
    main()