import jellyfish

TESTS = [('Chronicle: 20 Greatest Hits', 'chronicle'),
         ('Guns N\' Roses', 'GUNS N Roses'),
         ('Santana', 'Carlos Santana'),
         ('Run The Jewels 2', 'Run The Jewels'),
         ('Run The Jewels 2', 'Run The Jewels 2'),
         ('Run The Jewels 2', 'Run The Jewels 3'),]

s2 = 'a thousand kisses deep'
s1 = ['Sailing to Byzantium', 'Pelt', 'Romance and Revolution', 'House of Women', 'A Thousand Kisses Deep', 'Yell of the Gazelle', 'You Draw The Line', 'You Draw the Line', 'Secret Life Of A Girl', 'Tapestry Unravelled', 'Aililiu', 'Songs Of Leonard Cohen', 'Lovers And Strangers']

s1 = ['The Antisocial Club', 'The Imagined Savior Is Far Easier To Paint', 'When The Heart Emerges Glistening']
#TESTS = [(string.lower(), s2.lower()) for string in s1]

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
        print()
        #test((case[1], case[0]), ALGOS)