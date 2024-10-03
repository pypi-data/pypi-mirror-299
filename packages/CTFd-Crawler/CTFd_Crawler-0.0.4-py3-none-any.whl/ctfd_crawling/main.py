import json
import logging
import os
from dataclasses import asdict

from .dataclass import Challenge, Important
from .util import ApiManagement, DownloadCrawler

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(asctime)s - %(message)s",
    filename="ctf_crawling.log",
)


class CTFCrawler:
    def __init__(self, work_directory="."):
        self.work_directory = work_directory.strip("/")
        self.api = None

    def save(self):
        with open(f"{self.work_directory}/{self.important.name}.json", "w") as f:
            json.dump(
                {
                    "important": {
                        "name": self.important.name,
                        "url": self.important.url,
                        "token": self.important.token,
                        "location": self.important.location,
                    },
                    "data": [asdict(i) for i in self.data],
                },
                f,
                indent=4,
            )
        logging.info(
            f"Save the data to {self.work_directory}/{self.important.name}.json"
        )

    def important_check(self, important):
        if not important.get("name"):
            logging.error("No name key in the important")
            raise Exception("No name key in the important")
        if not important.get("url"):
            logging.error("No url key in the important")
            raise Exception("No url key in the important")
        if not important.get("token"):
            logging.error("No token key in the important")
            raise Exception("No token key in the important")
        if not important.get("location"):
            logging.error("No location key in the important")
            raise Exception("No location key in the important")
        self.important: Important = Important(**important)
        return True

    def load(self, json_file):
        """
        Load the data from the file.
        """
        with open(f"{self.work_directory}/{json_file}", "r") as f:
            data = json.load(f)
            if data.get("important") and self.important_check(data["important"]):
                logging.info(f"Load the data from {self.work_directory}/{json_file}")
                if data.get("data"):
                    self.data = [Challenge(**i) for i in data["data"]]
                else:
                    self.data = []
                self.important.location = self.important.location.strip("/")
                self.important.url = self.important.url.strip("/")
                self.api = ApiManagement(
                    self.important.url,
                    self.important.token,
                )
            else:
                raise Exception("No important key in the file. Please check the file")

    def self_load(self, name, url, token, location):
        """
        Load the data from the user input.
        It save the data to file.
        """
        if os.path.exists(f"{self.work_directory}/{name}.json"):
            logging.info(f"{self.work_directory}/{name}.json is already exists")
            raise Exception(f"{self.work_directory}/{name}.json is already exists")
        else:
            location = location.strip("/")
            url = url.strip("/")
            self.api = ApiManagement(url, token, location)
            self.important = Important(
                name=name, url=url, token=token, location=location
            )
            self.data = []

    def get_challenges(self):
        if not self.api:
            logging.error("Please load the data")
            raise Exception("Please load the data")
        result = self.api.challenges(self.data)
        if type(result) == Exception:
            logging.error(result)
            raise result
        self.data = result
        self.save()
        return result

    def download_challenges(self, flag=1):
        """
        flag 0: download challenges and save the files as is
        flag 1: download challenges and save the files as zip format
        """
        self.download_crawler = DownloadCrawler(self.important)
        logging.info("Set download crawler")
        result = self.download_crawler.download_all(self.data)
        logging.info("Download the challenges")
        for i in result:
            logging.info(f"{i} downloaded")
        self.important.location = self.download_crawler.get_output()
        self.save()
