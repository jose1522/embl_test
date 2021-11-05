import ftplib
from os import path
from uuid import uuid4
from pathlib import Path
from dataclasses import dataclass


@dataclass
class FTPCredentials:
    user: str
    password: str


@dataclass
class FTPServer:
    url: str
    uri: str
    filename: str


class Downloader:

    def __init__(self, server: FTPServer, credentials: FTPCredentials = None):
        self.name = str(uuid4())
        self.server = server
        self.__credentials = credentials

    @property
    def path(self) -> path:
        return path.join(Path(__file__).parent.parent, "files", self.filename)

    @property
    def filename(self):
        return f"{self.name}.{self.server.filename}"

    def run(self):
        with ftplib.FTP(self.server.url) as ftp:
            if self.__credentials:
                ftp.login(user=self.__credentials.user, passwd=self.__credentials.password)
            ftp.cwd(self.server.uri)
            with open(self.path, "wb") as file:
                ftp.retrbinary("RETR " + self.server.filename, file.write)


if __name__ == '__main__':
    url = "ftp.ebi.ac.uk"
    uri = "pub/databases/chembl/other/"
    name = "activities.csv"
    s = FTPServer(url, uri, name)
    downloader = Downloader(s)
    downloader.run()
