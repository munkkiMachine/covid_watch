import pandas as pd
import numpy as np
import json


class dataLog:

    def __init__(self, df, cols, title):
        self.df = self._set_df(df)
        self.cols = self._set_cols(cols)
        self.title = self._set_title(title)
        self.data_log = None
    
    def df_summaries(self):

        df_agg_collected = None

        for i in ["mean", "min", "max", np.std]:
            df_agg = self.df.groupby('country', as_index=False)[self.cols].agg(i)
            if i == np.std:
                i = "std"
            df_agg.insert(0, "country_agg", [x + "_" + i for x in df_agg['country']])

            if df_agg_collected is None:
                df_agg_collected = df_agg
            else:
                df_agg_collected = df_agg_collected.append(df_agg)

        self.data_log = df_agg_collected.reset_index(drop=True)
    
    def publish_log(self):
        self.df_summaries()
        path = "logs/data_logs/%s%s" % (self.title, ".json")
        data_log_json = self.data_log.to_json(orient="index")
        parsed = json.loads(data_log_json)
        with open(path, "w") as outfile:
            json.dump(parsed, outfile)
    
    def _set_df(self, df_input):
        if not isinstance(df_input, pd.DataFrame):
            raise TypeError("df needs to be pandas DataFrame")
        if df_input.empty:
            raise ValueError("this dataframe is empty")
        return df_input
    
    def _set_cols(self, cols_input):
        if not isinstance(cols_input, list):
            raise TypeError("cols need to be a list type")
        if not cols_input:
            raise ValueError("cols is empty")
        return cols_input
    
    def _set_title(self, title_input):
        if not isinstance(title_input, str):
            raise TypeError("title needs to be a string")
        if not title_input:
            raise ValueError("title is an empty string")
        return title_input


if __name__ == "__main__":
    #TODO: convert this to a test

    np.random.seed(99)
    df = pd.DataFrame(np.random.rand(4, 3), columns=["cases",
                                                    "deaths",
                                                    "recoveries"])
    df["country"] = ["hk", "hk", "sg", "sg"]

    x = dataLog(df, ["cases", "deaths", "recoveries"], "test")
    x.df_summaries()
    print(x.data_log)
    x.publish_log()

    with open('logs/data_logs/test.json') as f:
        data = json.load(f)
