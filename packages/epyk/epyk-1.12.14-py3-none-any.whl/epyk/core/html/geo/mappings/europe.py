# Continent mappings
c = {'Albania': 'al',
     'Armenia': 'am',
     'Austria': 'at',
     'Azerbaijan': 'az',
     'Belarus': 'by',
     'Belgium': 'be',
     'Bosnia and Herzegovina': 'ba',
     'Bulgaria': 'bg',
     'Croatia': 'hr',
     'Cyprus': 'cy',
     'Czech Republic': 'cz',
     'Denmark': 'dk',
     'Estonia': 'ee',
     'Finland': 'fi',
     'France': 'fr',
     'Georgia': 'ge',
     'Germany': 'de',
     'Greece': 'gr',
     'Hungary': 'hu',
     'Iceland': 'is',
     'Ireland': 'ie',
     'Italy': 'it',
     'Latvia': 'lv',
     'Lithuania': 'lt',
     'Macedonia': 'mk',
     'Malta': 'mt',
     'Moldova': 'md',
     'Netherlands': 'nl',
     'Norway': 'no',
     'Poland': 'pl',
     'Portugal': 'pt',
     'Romania': 'ro',
     'Serbia': 'rs',
     'Slovakia': 'sk',
     'Slovenia': 'si',
     'Spain': 'es',
     'Sweden': 'se',
     'Switzerland': 'ch',
     'Ukraine': 'ua',
     'United Kingdom': 'gb'}

r = {'Albania': 'al',
     'Algeria': 'dz',
     'Andorra': 'ad',
     'Armenia': 'am',
     'Austria': 'at',
     'Azerbaijan': 'az',
     'Belarus': 'by',
     'Belgium': 'be',
     'Bosnia and Herzegovina': 'ba',
     'Bulgaria': 'bg',
     'Croatia': 'hr',
     'Cyprus': 'cy',
     'Czech Republic': 'cz',
     'Denmark': 'dk',
     'Estonia': 'ee',
     'Finland': 'fi',
     'France': 'fr',
     'Georgia': 'ge',
     'Germany': 'de',
     'Greece': 'gr',
     'Greenland': 'gl',
     'Hungary': 'hu',
     'Iceland': 'is',
     'Iran': 'ir',
     'Iraq': 'iq',
     'Ireland': 'ie',
     'Israel': 'il',
     'Italy': 'it',
     'Jordan': 'jo',
     'Kazakhstan': 'kz',
     'Latvia': 'lv',
     'Lebanon': 'lb',
     'Liechtenstein': 'li',
     'Lithuania': 'lt',
     'Luxembourg': 'lu',
     'Macedonia': 'mk',
     'Malta': 'mt',
     'Moldova': 'md',
     'Monaco': 'mc',
     'Montenegro': 'me',
     'Morocco': 'ma',
     'Netherlands': 'nl',
     'Norway': 'no',
     'Poland': 'pl',
     'Portugal': 'pt',
     'Romania': 'ro',
     'Russian Federation': 'ru',
     'San Marino': 'sm',
     'Saudi Arabia': 'sa',
     'Serbia': 'rs',
     'Slovakia': 'sk',
     'Slovenia': 'si',
     'Spain': 'es',
     'Sweden': 'se',
     'Switzerland': 'ch',
     'Syrian Arab Republic': 'sy',
     'Tunisia': 'tn',
     'Turkey': 'tr',
     'Turkmenistan': 'tm',
     'Ukraine': 'ua',
     'United Kingdom': 'gb'}


if __name__ == "__main__":
    json_data = {}

    import pprint

    r_data = {}
    for k, v in json_data.items():
        r_data[v['name']] = k
    pprint.pprint(r_data)
