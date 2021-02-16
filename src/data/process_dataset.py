import pandas as pd
from pathlib import Path
import sys
import os
sys.path.append(os.path.dirname(Path(__file__).parent.parent))
from src.config.config_module import config
from src import utils


class processDataset:

    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.raw_df = None
        self.ready_to_split_df = None
        self.confirmed = None
        self.deaths = None
        self.recovered = None

    def read_data(self):
        base_path = Path(__file__).parents[2]
        raw_data_path = (base_path / 'data//raw').resolve()

        self.raw_df = pd.read_csv(str(raw_data_path) + '/' + self.input_file)

    def rename_data(self):
        # renaming columns
        df = self.raw_df.rename(columns={'Unnamed: 0':'SNo', 'Country_Region':'Country', 'Province_State':'State', 'Last_Update':'Date'})
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        cols_to_keep = ['Confirmed', 'Deaths', 'Recovered']
        df = df.groupby(["Date", "Country", "State"])[cols_to_keep].sum().reset_index()
        self.ready_to_split_df = df

    def split_data(self):
        # setting up data for Prophet
        self.confirmed = self.ready_to_split_df[['Date', 'State', 'Country', 'Confirmed']]
        self.deaths = self.ready_to_split_df[['Date', 'State', 'Country', 'Deaths']]
        self.recovered = self.ready_to_split_df[['Date', 'State', 'Country', 'Recovered']]
    
    def write_data(self):
        # writing data into processed data folder
        self.confirmed.to_csv(os.path.join(self.output_file, ('confirmed_{}{}'.format(utils.current_date(), '.csv'))))
        self.deaths.to_csv(os.path.join(self.output_file, ('deaths_{}{}'.format(utils.current_date(), '.csv'))))
        self.recovered.to_csv(os.path.join(self.output_file, ('recovered_{}{}'.format(utils.current_date(), '.csv'))))
    
    def process_dataset_to_processed(self):
        self.read_data()
        self.rename_data()
        self.split_data()
        self.write_data()


if __name__ == "__main__":
    
    processDataset(input_file = "{}_{}.csv".format(config.get("process_dataset", "input_file_name"), utils.current_date()),
    output_file = config.get("process_dataset", "output_file_location")).process_dataset_to_processed()
