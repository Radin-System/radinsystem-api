import os
from flask import Blueprint, request, abort, send_file
from .. import agent_packages
from ..utils import create_response, create_agent_file_path

agent_bp = Blueprint('agent', __name__, url_prefix='/agent')

@agent_bp.route('/update-details')
def update_details():
    version = request.args.get('version')
    if not version:
        abort(400, 'Missing version parameter')

    version_hash = agent_packages.get(version, '')

    if not hash:
        abort(404, f'version not found: {version}')

    return create_response({'version': version, 'sha256': version_hash})

@agent_bp.route('/latest-update-details')
def latest_update_details():
    global agent_packages
    if not agent_packages:
        abort(404, 'No versions available')

    latest_version = sorted(agent_packages.keys(), reverse=True)[0]
    return create_response({'latest': latest_version, 'sha256': agent_packages[latest_version]})

@agent_bp.route('/download-application')
def download_application():
    version = request.args.get('version')
    if not version:
        abort(400, 'Missing version parameter')

    file_path = create_agent_file_path(version)
    if not os.path.exists(file_path):
        abort(404, f'Agent version {version} not found')

    return send_file(file_path, as_attachment=True)
