#!/usr/bin/python3
# Delete out-of-date archives
import os
from fabric.api import env, local, run, cd, lcd

env.hosts = ["104.196.168.90", "35.196.46.172"]

def do_clean(number=0):
    """Delete out-of-date archives.

    Args:
        number (int): The number of archives to keep.

    If number is 0 or 1, keeps only the most recent archive. If
    number is 2, keeps the most and second-most recent archives,
    etc.
    """
    number = max(1, int(number))

    with lcd("versions"):
        local("ls -t | tail -n +{} | xargs -I {{}} rm {{}}".format(number + 1))

    with cd("/data/web_static/releases"):
        archives = run("ls -tr | grep 'web_static_'").split()
        archives = archives[:-number] if len(archives) > number else []
        run("rm -rf {}".format(" ".join(archives)))
