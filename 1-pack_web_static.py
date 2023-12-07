from fabric.api import local
from datetime import datetime
import os

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder

    Returns:
        Archive path if successfully generated, None otherwise
    """
    try:
        local("mkdir -p versions")

        # Generate the archive
        now = datetime.utcnow()
        archive_name = "web_static_{}{}{}{}{}{}.tgz".format(
            now.year, now.month, now.day, now.hour, now.minute, now.second
        )
        local("tar -cvzf versions/{} web_static".format(archive_name))

        return os.path.join("versions", archive_name)

    except Exception as e:
        # Print the exception and return None
        print("Error during archive creation: {}".format(e))
        return None
