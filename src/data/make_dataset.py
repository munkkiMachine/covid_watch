from pathlib import Path
import sys
import os
sys.path.append(os.path.dirname(Path(__file__).parent.parent))

import requests
from datetime import datetime
import time
from bs4 import BeautifulSoup
import pandas as pd
from src.config.config_module import config
from src import utils
from logs.data_logs.data_log_generator import dataLog

class makeDataset:

    def __init__(self, url, git_link_raw, ext, range, output_name):
        self.url = url
        self.git_link_raw = git_link_raw
        self.ext = ext
        self.range = int(range)
        self.output_name = output_name

    def listDirs(self):
        page = requests.get(self.url).text
        soup = BeautifulSoup(page, 'html.parser')
        return [self.git_link_raw + node.get('href').replace("blob/", "") for node in soup.find_all('a') if node.get('href').endswith(self.ext)]

    def selectDataInRange(self):
        dirList = self.listDirs()
        return dirList[-self.range:]

    def generateMasterDataframe(self):
        master_df = pd.DataFrame()
        directories = self.selectDataInRange()
        for link in directories:
            x = pd.read_csv(link)
            master_df = master_df.append(x)
        # TODO: Probably best to refer to the datecol here from a predefined schema
        return self.dateFilter(master_df, "Last_Update")
    
    def dateFilter(self, df, date_col):
        """
        WHO's data isn't perfect and outdated data makes it in.
        This is an extra layer to keep only relevant dates.
        """
        available_dates = df[date_col].unique()
        available_dates.sort()
        in_range_dates = available_dates[-self.range:]
        
        mask = df[date_col].isin(in_range_dates)
        return df[mask]

    def saveFileToRaw(self):
        root_dir = utils.get_project_root()
        file_dir = os.path.join(root_dir, "data", "raw", self.output_name + "_" + utils.current_date() + ".csv")

        if os.path.isfile(file_dir):
            print("Raw data was already updated today")
        else:
            data_file = self.generateMasterDataframe()

            data_file.to_csv(file_dir)


if __name__ == "__main__":

    makeDataset(config.get("make_dataset", "url"), 
                config.get("make_dataset", "git_site_raw"), 
                config.get("make_dataset", "ext"),
                config.get("make_dataset", "ingestion_range"), 
                config.get("make_dataset", "output_file_name")).saveFileToRaw()
