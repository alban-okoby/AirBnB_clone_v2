#!/usr/bin/python3
# Fabric script for deploying an archive to web servers

from fabric.api import env, put, run, sudo, task
from os.path import exists

env.hosts = ['<IP web-01>', '<IP web-02>']

@task
def do_deploy(archive_path):
    """
    Distributes an archive to web servers.

    Args:
        archive_path (str): Path to the archive on the local machine

    Returns:
        True if all operations are done correctly, otherwise False
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
