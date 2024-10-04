import os

version_folder = os.path.dirname(os.path.join(os.path.abspath(__file__)))

with open(os.path.join(version_folder, 'version/version')) as f:
    __version__ = f.read().strip()

with open(os.path.join(version_folder, 'version/scm_version')) as f:
    scm_version = 'local'
