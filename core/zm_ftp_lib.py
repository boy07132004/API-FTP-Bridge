from ftplib import FTP
import io
import logging


class ZM_FTP(FTP):
    def __init__(self, config):
        host = config["FTP"]["FTP_SERVER"]
        username = config["FTP"]["FTP_USER"]
        passwd = config["FTP"]["FTP_PASSWD"]
        self.path = config["FTP"]["FOLDER_PATH"]

        super().__init__(host)
        self.login(user=username, passwd=passwd)

    def write_recipe(self, recipe, filename="default_name"):
        _filename = self.path + '\\' + filename
        content_bytes = recipe.encode('utf-8')

        response = self.storbinary(
            'STOR ' + _filename, fp=io.BytesIO(content_bytes))

        if response.startswith('226'):
            logging.info("File uploaded successfully.")
        else:
            logging.error("Error uploading file.")
