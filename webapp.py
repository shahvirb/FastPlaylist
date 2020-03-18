import flask
import logging
import find_parsers

logging.basicConfig(level=logging.DEBUG)

app = flask.Flask(__name__, template_folder='templates',
                  static_folder=r'C:\Users\fusiv\Documents\Progr_Proj\Python\FastPlaylist\static')
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/parse_html_file')
def parse_html_file():
    parser_paths = find_parsers.find_parsers()
    return flask.render_template('parse_html.html', html_name=flask.request.args.get('load_file'), parsers=parser_paths,
                                 selected_parser=flask.request.args.get('sel_parser'))


if __name__ == '__main__':
    app.run()
