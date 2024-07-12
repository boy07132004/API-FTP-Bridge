from ftplib import FTP
from functools import wraps
import io


class ZM_FTP():
    def __init__(self, config, logger, backup_folder):
        self.host = config["FTP"]["FTP_SERVER"]
        self.username = config["FTP"]["FTP_USER"]
        self.passwd = config["FTP"]["FTP_PASSWD"]
        self.logger = logger
        self.ftp = None
        self.backup_folder = backup_folder

        self.backup_folder_check()
        self.root_path = self.ftp.pwd()

    def ftp_login(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                self.ftp.pwd()
            except:
                self.ftp = FTP(self.host)
                self.ftp.login(self.username, self.passwd)

            return func(self, *args, **kwargs)
        return wrapper

    @ftp_login
    def backup_folder_check(self):
        try:
            self.ftp.cwd(self.backup_folder)
            self.ftp.cwd("..")

        except:
            self.logger.error("can't find backup folder")
            self.ftp.mkd(self.backup_folder)

    @ftp_login
    def get_file_content(self, filename):
        file_content = []
        self.ftp.retrlines('RETR ' + filename, file_content.append)
        return "\n".join(file_content)

    @ftp_login
    def get_files_content(self, filenames: list, path=""):
        files_content = {}
        self.ftp.cwd(path)

        for filename in filenames:
            files_content[filename] = self.get_file_content(filename)

        self.ftp.cwd(self.root_path)
        return files_content

    @ftp_login
    def write_recipe(self, recipes, path=""):
        ret = []
        self.ftp.cwd(path)

        for _, file_dict in recipes.items():
            for filename, content in file_dict.items():
                content_bytes = content.encode('utf-8')

                response = self.ftp.storbinary(
                    'STOR ' + filename, fp=io.BytesIO(content_bytes))

                if response.startswith('226'):
                    self.logger.info("File uploaded successfully.")
                    ret.append(filename + " OK")
                else:
                    self.logger.error("Error uploading" + filename)
                    ret.append(filename + " failed")

        self.ftp.cwd(self.root_path)

        return ret

    @ftp_login
    def list_recipe_from_path(self, path=""):
        ret = {}
        self.ftp.cwd(path)
        file_list = self.ftp.nlst()

        for filename in file_list:
            if filename.endswith("proc") or filename.endswith("proc1") or filename.endswith("hdr"):
                recipe = filename.split(".")[0]
                ret[recipe] = "OK"

        self.ftp.cwd(self.root_path)

        return ret

    def get_recipes_content_from_path(self, recipes: list, path=""):
        ret = {}
        recipe_list = self.list_recipe_from_path(path)

        for recipe in recipes:
            if recipe not in recipe_list:
                continue

            ret[recipe] = self.get_files_content(
                [recipe+".proc", recipe+".proc1", recipe+".hdr"], path
            )

        return ret
