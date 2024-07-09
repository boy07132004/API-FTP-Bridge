from ftplib import FTP
import io


class ZM_FTP(FTP):
    def __init__(self, config, logger):
        host = config["FTP"]["FTP_SERVER"]
        username = config["FTP"]["FTP_USER"]
        passwd = config["FTP"]["FTP_PASSWD"]
        self.logger = logger

        super().__init__(host)
        self.login(user=username, passwd=passwd)

    def write_recipe(self, recipe, filename="default_name.txt"):

        content_bytes = recipe.encode('utf-8')

        response = self.storbinary(
            'STOR ' + filename, fp=io.BytesIO(content_bytes))

        if response.startswith('226'):
            self.logger.info("File uploaded successfully.")
        else:
            self.logger.error("Error uploading file.")

    def list_all_recipe(self):
        ret = set()
        file_list = self.nlst()

        for filename in file_list:
            recipe = filename.split(".")[0]
            ret.add(recipe)

        return list(ret)
