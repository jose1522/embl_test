import logging
import requests
from task import Server
from pathlib import Path
from os import path, fsync

logger = logging.getLogger("ftp_client")


class DownloaderException(Exception):
    pass


class Downloader:

    def __init__(self, server: Server):
        self.server = server

    @property
    def path(self) -> path:
        return path.join(Path(__file__).parent.parent, "files", self.filename)

    @property
    def filename(self) -> str:
        return self.server.url.split('/')[-1].replace(" ", "_")

    def run(self):
        try:
            response = requests.get(self.server.url, stream=True)
            if response.ok:
                logger.info(f"Downloaded file {self.filename} to path: {self.path}")
                with open(self.path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024 * 8):
                        if chunk:
                            f.write(chunk)
                            f.flush()
                            fsync(f.fileno())
            else:
                raise DownloaderException(f"Download failed: status code {response.status_code}:\t{response.text}")
        except Exception as e:
            raise DownloaderException(f"Download failed: {str(e)}")


if __name__ == '__main__':
    s = Server("https://ftp.ebi.ac.uk/pub/databases/chembl/other/activities.csv")
    d = Downloader(s)
    d.run()