import pandas as pd
import numpy as np
import json
import unittest
from logs.data_logs.data_log_generator import dataLog

np.random.seed(99)
df = pd.DataFrame(np.random.rand(4, 3), columns=["cases",
                                            "deaths",
                                            "recoveries"])
df["country"] = ["hk", "hk", "sg", "sg"]
cols = ["cases", "deaths", "recoveries"]

class testDataLogGenerator(unittest.TestCase):

    def test_setters_type_errors(self):
        with self.assertRaises(TypeError):
            dataLog(None, cols, "test")
        with self.assertRaises(TypeError):
            dataLog(df, None, "test")
        with self.assertRaises(TypeError):
            dataLog(df, cols, None)
    
    def test_setters_value_errors(self):
        with self.assertRaises(ValueError):
            dataLog(pd.DataFrame(), cols, "test")
        with self.assertRaises(ValueError):
            dataLog(df, [], "test")
        with self.assertRaises(ValueError):
            dataLog(df, cols, "")
    
    def test_data_aggregation(self):
        test_class = dataLog(df, cols, "test")
        test_class.df_summaries()
        self.assertEquals(pd.DataFrame, type(test_class.data_log))
        self.assertEquals(8, len(test_class.data_log))
        self.assertEquals(0.3519, round(test_class.data_log["cases"][0], 4))
        self.assertEquals(0.6481, round(test_class.data_log["deaths"][0], 4))
        self.assertEquals(0.6956, round(test_class.data_log["recoveries"][0], 4))

    def test_publishing(self):
        test_class = dataLog(df, cols, "test")
        test_class.publish_log()

if __name__ == '__main__':
    unittest.main()
