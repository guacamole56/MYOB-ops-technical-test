from flask import Flask, jsonify

from .config import VERSION, DESCRIPTION
from .helper import get_last_commit_sha


# Main web app entry point.
app = Flask(__name__)


# Endpoints.
@app.route('/')
def hello():
    return 'Hello World!\n'


@app.route('/health')
def healthcheck():
    return 'OK\n'


@app.route('/metadata')
def metadata():
    return jsonify(
            app_name=__name__,
            description=DESCRIPTION,
            last_commit_sha=get_last_commit_sha(),
            version=VERSION
            )
