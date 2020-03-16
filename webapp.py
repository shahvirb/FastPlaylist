import flask
import logging
logging.basicConfig(level=logging.DEBUG)

app = flask.Flask(__name__, template_folder='templates', static_folder=r'C:\Users\fusiv\Documents\Progr_Proj\Python\FastPlaylist\static')


@app.route('/')
def index():
   return flask.render_template('index.html')

if __name__ == '__main__':
   app.run()