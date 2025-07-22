from flask import Blueprint, request, abort
from application.utils._json_response import create_response
from .. import agent_packages, load_agent_packages
from ..utils import private_addresses_only

dev_bp = Blueprint('dev', __name__, url_prefix='/dev')

@dev_bp.route('/agent/add-package')
@private_addresses_only(request)
def add_agent_package():
    abort(500)

    load_agent_packages()

@dev_bp.route('/agent/update-versions')
@private_addresses_only(request)
def update_versions():
    """Rescan folder and update version -> hash mapping"""
    load_agent_packages()
    global agent_packages

    return create_response(agent_packages)

@dev_bp.route('/agent/delete-package')
@private_addresses_only(request)
def delete_agent_package():
    abort(500)

    load_agent_packages()