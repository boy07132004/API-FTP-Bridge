from ftplib import FTP
import io


class ZM_FTP(FTP):
    def __init__(self, config, logger):
        host = config["FTP"]["FTP_SERVER"]
        username = config["FTP"]["FTP_USER"]
        passwd = config["FTP"]["FTP_PASSWD"]
        self.path = config["FTP"]["FOLDER_PATH"]
        self.logger = logger

        # remove the end slash
        if len(self.path) > 0 and self.path[-1] == "/":
            self.path = self.path[:-1]

        super().__init__(host)
        self.login(user=username, passwd=passwd)
        self.rootPath = self.pwd()

    def ftp_path_chk(self, remotePath=None):
        self.cwd(self.rootPath)

        if remotePath:
            for i in range(1, len(remotePath.split("/"))):
                path = remotePath.split("/")[i]
                try:
                    self.cwd(path)
                except:
                    self.mkd(path)
                    self.cwd(path)

        else:
            self.logger.warning("Please input remote path.")

    def write_recipe(self, recipe, filename="default_name.txt"):
        _path = self.rootPath + self.path
        self.ftp_path_chk(_path)

        _filename = _path + '/' + filename
        content_bytes = recipe.encode('utf-8')

        response = self.storbinary(
            'STOR ' + _filename, fp=io.BytesIO(content_bytes))

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
