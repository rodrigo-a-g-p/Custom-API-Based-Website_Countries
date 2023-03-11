from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
import random
from titlecase import titlecase
from helperFunctions import connect_to_api, get_native_name, get_currency_name, get_currency_symbol, get_capital, get_all_languages, get_population, relevant_keys


app = Flask(__name__)
Bootstrap(app)

countries_response = connect_to_api()


@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        country = request.form['country_input']
        return redirect(url_for('show_country', country_name=country))

    featured_countries_list = [{element['name']['common']: element['flags']['png']} for element in random.sample(countries_response, 3)]
    return render_template('index.html', countries_to_display=featured_countries_list)


@app.route('/<country_name>')
def show_country(country_name):
    try:
        # Used titlecase() function from imported package because it does not titlecase words such as "and"
        # Unlike .title() method, which does not skip any word
        found_country = [element for element in countries_response if element['name']['common'] == titlecase(country_name)][0]
        country_data = {key: value for key, value in found_country.items() if key in relevant_keys}

        # Jinja cannot process the function list() (among other errors that may occur), hence special functions were created to retrieve some parts of the data
        variables_processed_outside_jinja = {'native_name': get_native_name(country_data),
                                             'currency_name': get_currency_name(country_data),
                                             'currency_symbol': get_currency_symbol(country_data),
                                             'all_languages': get_all_languages(country_data),
                                             'population': get_population(country_data),
                                             'capital': get_capital(country_data)}

        return render_template('country.html', country=country_data, send_variables=variables_processed_outside_jinja)

    except IndexError:
        # Triggered in case country specified by the user does not exist in the API
        return redirect(url_for('display_error'))


@app.route('/error')
def display_error():
    return render_template('error.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
