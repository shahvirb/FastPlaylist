import gmusic
import logging
import click
import csv

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

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
@click.option('--add', default='song', help='Which results to add. Defaults to "song". Values = ["song, "album"]' )
@click.option('--step/--no-step', default=False, help='Step through each row in the csv')
@click.option('--query', default='all', help='Which headers to use when forming search queries. Defaults to "all". Values = ["all", "first"]' )
def main(filename, create, name, add, step, query):
    import coloredlogs
    coloredlogs.install()
    handler = logging.StreamHandler()
    #handler.setFormatter(logging.Formatter(fmt=logging.BASIC_FORMAT))
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.WARNING)

    logger.info('Reading CSV File: {}'.format(filename))
    rows, headers = read_csv(filename)
    logger.info('{} data rows found with header: '.format(len(rows), headers))

    gmclient = gmusic.get_authenticated_client()
    tracks = []
    no_results = []
    for row in rows:
        search = None
        if query == 'first':
            search = row[headers[0]]
        if query == 'all':
            search = ' '.join([row[headers[n]] for n in range(len(headers))])
        logger.info('Searching: \"{}\" - {}'.format(search, row))
        raw = gmusic.search(gmclient, search)

        hits = []
        if add == 'song':
            hits = gmusic.find_songs(gmclient, raw, row)
            hits = hits[0:1]
        if add == 'album':
            hits = gmusic.find_albums(gmclient, raw, row)
        if hits:
            for hit in hits:
                logger.info('Found: {} - {} - {}'.format(hit['title'], hit['artist'], hit['album']))
                tracks.append(hit)
        else:
            no_results.append(search)
            logger.warning('No results: {}'.format(search))
        if step:
            input('Press enter to continue')
    logger.info('Searched for {} rows and found {} tracks'.format(len(rows), len(tracks)))
    logger.warning('No results:')
    for r in no_results:
        logger.warning(f'\t{r}')

    if create:
        if not name:
            name = filename
        plid = gmclient.create_playlist(name)
        logger.info('Created playlist {} as ID {}'.format(name, plid))
        song_ids = [track['storeId'] for track in tracks]
        gmclient.add_songs_to_playlist(plid, song_ids)
        logger.info('Added {} tracks to playlist'.format(len(song_ids)))


if __name__ == '__main__':
    main()