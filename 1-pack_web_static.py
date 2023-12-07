#!/usr/bin/python3
# Fabfile to generate a .tgz archive
import os.path
from datetime import datetime
from fabric.api import local, task

@task
def do_pack():
    """Create a tar gzipped archive of the directory web_static"""
    dt = datetime.utcnow()
    archive_name = "web_static_{}{}{}{}{}{}.tgz".format(
        dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second
    )
    archive_path = os.path.join("versions", archive_name)

    # Create the 'versions'
    local("mkdir -p versions")
    result = local("tar -cvzf {} web_static".format(archive_path), capture=True)

    if result.failed:
        return None

    return archive_path
