import requests

relevant_keys = ['name', 'currencies', 'capital', 'region', 'subregion', 'languages', 'flag', 'population',
                 'continents', 'flags', 'coatOfArms', 'maps']


def connect_to_api():
    # Get Data from API
    url = f'https://restcountries.com/v3.1/all'
    countries_response = requests.get(url).json()

    # Removing Antarctica from the response because it is missing too many keys
    countries_to_remove = ['Antarctica', 'Bouvet Island']
    countries_response = [element for element in countries_response if element['name']['common'] not in countries_to_remove]
    return countries_response


def get_native_name(input_country_data):
    return dict(list(input_country_data['name']['nativeName'].values())[0])['common']


def get_currency_name(input_country_data):
    return dict(list(input_country_data['currencies'].values())[0])['name']


def get_currency_symbol(input_country_data):
    """ Some countries' currency do not have a symbol in the API (Sudan, for example) """
    try:
        return (list(input_country_data['currencies'].values())[0])['symbol']
    except KeyError:
        return 'N/A'


def get_all_languages(input_country_data):
    all_languages_list = list(input_country_data['languages'].values())
    all_languages_string = "; ".join(all_languages_list)
    return all_languages_string


def get_population(input_country_data):
    population = int(input_country_data['population'])

    if population < 100000:
        return population
    if population < 1000000:
        return f'{round(population / 1000, 2)}K'
    if population < 1000000000:
        return f'{round(population / 1000000, 2)}M'

    return f'{round(population / 1000000000, 2)}B'


def get_capital(input_country_data):
    """ Some countries in the API do not have a capital (Macau, for example) """
    try:
        return input_country_data['capital'][0]
    except KeyError:
        return 'N/A'
