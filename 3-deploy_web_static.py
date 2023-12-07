#!/usr/bin/python3
# Fabric script for creating and distributing an archive to web servers.

from fabric.api import env, task
from os.path import exists
from fabric.operations import local
from datetime import datetime
from fabric.state import output

# Set my env
env.hosts = ['<IP web-01>', '<IP web-02>']
output['running'] = False
output['stdout'] = False

@task
def do_pack():
    """
    Generates a .tgz archive from the contents of web_static

    Returns:
        Archive path if successfully generated, None otherwise
    """
    try:
        local("mkdir -p versions")
        now = datetime.utcnow()
        archive_name = "web_static_{}{}{}{}{}{}.tgz".format(
            now.year, now.month, now.day, now.hour, now.minute, now.second
        )
        local("tar -cvzf versions/{} web_static".format(archive_name))
        return "versions/{}".format(archive_name)

    except Exception as e:
        print("Error during archive creation: {}".format(e))
        return None

@task
def do_deploy(archive_path):
    """
    Distributes an archive to web servers.

    Args:
        archive_path (str): Path to the archive on the local machine.

    Returns:
        True if all operations are done correctly, otherwise False.
    """
    if not exists(archive_path):
        return False

    try:
        put(archive_path, '/tmp/')
        archive_filename = archive_path.split('/')[-1]
        release_path = '/data/web_static/releases/{}'.format(
            archive_filename.split('.')[0]
        )
        run('mkdir -p {}'.format(release_path))
        sudo('tar -xzf /tmp/{} -C {}'.format(archive_filename, release_path))
        run('rm /tmp/{}'.format(archive_filename))
        run('rm -f /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(release_path))

        return True

    except Exception as e:
        print("Error during deployment: {}".format(e))
        return False

@task
def deploy():
    """
    Creates and distributes an archive to web servers.

    Returns:
        True if all operations are done correctly, otherwise False.
    """
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)
