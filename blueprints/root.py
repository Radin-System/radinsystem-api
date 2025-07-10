from flask import Blueprint

from __version__ import __version__
from utils import create_response

root_bp = Blueprint('root', 'root', url_prefix='/')

@root_bp.route('/')
def index():
    return create_response(message='Welcome to radin api')

@root_bp.route('/version')
def version():
    return create_response(
        {
            'version': __version__,
        }
    )