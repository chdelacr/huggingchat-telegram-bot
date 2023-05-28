import logging
import os
import pysftp

logger = logging.getLogger("__main__.sftp_handler")

def sftpLoadCookies():
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    SFTP_SERVER = os.getenv("SFTP_SERVER")
    SFTP_USERNAME = os.getenv("SFTP_USERNAME")
    SFTP_PASSWORD = os.getenv("SFTP_PASSWORD")
    SFTP_PATH = os.getenv("SFTP_PATH")

    with pysftp.Connection(SFTP_SERVER, username=SFTP_USERNAME, password=SFTP_PASSWORD, cnopts=cnopts) as sftp:
        with sftp.cd(SFTP_PATH):
            logger.info("Loading HuggingChat cookies from SFTP")
            sftp.get("remote_cookies.json", "local_cookies.json")
        sftp.close()