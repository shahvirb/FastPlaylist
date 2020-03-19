import ezscraper
import find_parsers
import flask
import logging

logging.basicConfig(level=logging.DEBUG)

app = flask.Flask(__name__, template_folder='templates')
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/')
def index():
    parser_paths = find_parsers.find_parsers()
    return flask.render_template('index.html', parsers=parser_paths)


@app.route('/parse_html_file')
def parse_html_file():
    load_file = flask.request.args.get('load_file')
    load_URL = flask.request.args.get('load_URL')
    parsed = None
    source_name = None
    if load_file:
        parsed = ezscraper.parse_html_file(flask.request.args.get('sel_parser'), load_file)
        source_name = load_file
    if load_URL:
        parsed = ezscraper.parse_url(flask.request.args.get('sel_parser'), load_URL)
        source_name = load_URL

    error_text = None
    if not parsed:
        error_text = 'Parse error'

    return flask.render_template('parse_html.html', html_name=source_name,
                                 selected_parser=flask.request.args.get('sel_parser'), parsed_output=parsed,
                                 error_message=error_text)


if __name__ == '__main__':
    app.run()
