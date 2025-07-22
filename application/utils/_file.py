import os, hashlib

AGENT_FOLDER = 'agent_packages'

def create_agent_file_path(version: str) -> str:
    os.makedirs(AGENT_FOLDER, exist_ok=True)
    return os.path.join(AGENT_FOLDER, version, f'agent-{version}.exe')

def calculate_file_sha256(filepath: str) -> str:
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)

    return sha256.hexdigest()
