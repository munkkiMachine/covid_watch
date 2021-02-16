import unittest
import requests
import pandas as pd
from src.config.config_module import config
from src.data.make_dataset import makeDataset

make_dataset_class = makeDataset(config.get("make_dataset", "url"), 
                                 config.get("make_dataset", "git_site_raw"), 
                                 config.get("make_dataset", "ext"),
                                 config.get("make_dataset", "ingestion_range"),
                                 "who_covid_data")


class testMakeDataset(unittest.TestCase):

    def test_config(self):
        # small check that the config file is reading
        self.assertEqual("csv", config.get("make_dataset", "ext"))

    def test_url_status(self):
        # pinging the url for a 200 HTTP code
        url_status = requests.get(config.get("make_dataset", "url")).status_code
        all_good_status = requests.codes.all_good #pylint: disable=no-member
        self.assertEqual(url_status, all_good_status)

    def test_data_append(self):
        # testing that the data is appending properly
        df = make_dataset_class.generateMasterDataframe()
        self.assertEqual(type(df), pd.DataFrame)
        self.assertTrue(len(df) > 0)

    def test_data_range(self):
        # check that the amounto data pulled is what's expected
        df = make_dataset_class.generateMasterDataframe()
        self.assertEqual(len(df.Last_Update.unique()), int(config.get("make_dataset", "ingestion_range")))
 
if __name__ == '__main__':
    unittest.main()
