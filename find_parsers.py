import glob


def find_parsers(prefix='parser_', suffix='.py'):
    paths = glob.glob(prefix + '*' + suffix)
    return [p.split('.')[0] for p in paths]


if __name__ == '__main__':
    print(find_parsers())
