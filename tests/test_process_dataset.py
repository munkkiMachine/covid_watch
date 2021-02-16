import unittest
from src import utils
from src.config.config_module import config
from src.data.process_dataset import processDataset

test_processDataset_class = processDataset(input_file = "{}_{}.csv".format(config.get("process_dataset", "input_file_name"), utils.current_date()),
output_file = config.get("process_dataset", "output_file_location"))

class testProcessDataset(unittest.TestCase):

    def test_config(self):
        # check to see process_dataset section of config loads
        self.assertEqual(config.get('process_dataset', 'input_file_name'), 'who_covid_data')

    def test_raw_data_read(self):
        # ensure that raw data is being read in
        test_processDataset_class.read_data()
        self.assertTrue(len(test_processDataset_class.raw_df) > 1)

    def test_data_splitting(self):
        # Ensure data is being split equally
        test_processDataset_class.split_data()
        self.assertTrue(len(test_processDataset_class.confirmed) == len(test_processDataset_class.deaths))
        self.assertTrue(len(test_processDataset_class.deaths) == len(test_processDataset_class.recovered))

if __name__ == "__main__":
    unittest.main()
