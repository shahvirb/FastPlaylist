import jellyfish

TESTS = [('Chronicle: 20 Greatest Hits', 'chronicle'),
         ('Guns N\' Roses', 'GUNS N Roses')]

ALGOS = {'levenshtein_distance': jellyfish.levenshtein_distance,
         'damerau_levenshtein_distance': jellyfish.damerau_levenshtein_distance,
         'hamming_distance': jellyfish.hamming_distance,
         'jaro_distance': jellyfish.jaro_distance,
         'jaro_winkler': jellyfish.jaro_winkler,
         'match_rating_comparison': jellyfish.match_rating_comparison}


def test(case, ALGOS):
    print(case[0], case[1])
    for key in ALGOS:
        score = ALGOS[key](case[0], case[1])
        print(key, score)

if __name__ == '__main__':
    for case in TESTS:
        test(case, ALGOS)
        #test((case[1], case[0]), ALGOS)