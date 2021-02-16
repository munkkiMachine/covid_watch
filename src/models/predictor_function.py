# Adding to sys.path
import sys
import os
from pathlib import Path
sys.path.append(os.path.dirname(Path(__file__).parent.parent))

# importing packages
import numpy as np
import pandas as pd
from fbprophet import Prophet
import pycountry
from collections import namedtuple
import multiprocessing as mp
from src.config.config_module import config
from src import utils


class whats_up_with_covid:

  def __init__(self):
    self.unscored_countries = []

  def confirm_country_states(self, country, confirmed_df, deaths_df, recovered_df):
    # this will need to be called in a for loop for each country
    
    assert(country in confirmed_df['Country'].values)
    print(str(country).upper() + ' is listed')
    country_confirmed_df = confirmed_df[confirmed_df['Country'] == country]
    country_deaths_df = deaths_df[deaths_df['Country'] == country]
    country_recovered_df = recovered_df[recovered_df['Country'] == country]
    country_dfs = [('Confirmed', country_confirmed_df), 
                    ('Deaths', country_deaths_df),
                    ('Recovered', country_recovered_df)]
    states_in_country = country_confirmed_df['State'].unique()
    
    return country_dfs, states_in_country


  def state_level_forecasting(self, country, country_dfs, states_in_country, days_to_forecast):
      
      all_results = pd.DataFrame(columns=['ds', 'trend', 'yhat', 'status', 'country', 'state', 'MAE_per_state_status'])
      params = None

      for state in states_in_country:
        
        # try:
          # separating data for each covid status (Confirmed, Deaths, Recovered)
        for country_df_tup in country_dfs:
          case_type = country_df_tup[0]
          country_df = country_df_tup[1]
          state_df = country_df[(country_df['State'] == state)]
          
          if len(state_df) >= days_to_forecast:

            # data preparation for forecasting at State level
            state_df = state_df[['Date', case_type]]
            state_df.columns = ['ds', 'y']
            state_df['ds'] = pd.to_datetime(state_df['ds'])
            
            forecast, MAE_num, params = self.forecast_w_prophet(state_df, days_to_forecast)
            
            results_df = forecast[['ds', 'trend', 'yhat']]
            results_df['status'] = case_type
            results_df['country'] = country
            results_df['state'] = state
            results_df['MAE_per_state_status'] = MAE_num
            
            all_results = all_results.append(results_df)
        
          else:
            statement = "{}, {} has insufficient data.".format(state, country)
            print(statement)
            self.unscored_countries.append((state, country))
              
      return all_results, params


  def forecast_w_prophet(self, df, days_to_forecast, mode='default', m_fo=10, w_fo=21, y_fo=3, err='yes'):
      
      params = "default parameters"
      
      if mode == 'default':
        m = Prophet()
      elif mode == 'custom':
        m = Prophet(daily_seasonality=False, weekly_seasonality=False, yearly_seasonality=False)
        m.add_seasonality(name='monthly', period=30.5, fourier_order=m_fo)
        m.add_seasonality(name='weekly', period=7, fourier_order=w_fo)
        m.add_seasonality(name='daily', period=1, fourier_order=y_fo)
        params = "fourier orders: " + "monthly: " + str(m_fo) + " weekly: " + str(w_fo) + " daily: " + str(y_fo)
      
      m.fit(df)
      future = m.make_future_dataframe(periods=days_to_forecast)
      forecast = m.predict(future)

      if err=='yes':
        MAE_num = self.mean_sqr_error(df, days_to_forecast, mode, m_fo, w_fo, y_fo)
        return forecast, MAE_num, params
      else:
        return forecast
      

  def mean_sqr_error(self, df, days_to_forecast, mode, m_fo, w_fo, y_fo):
      
      test_forecast_date = sorted(list(set(df['ds'].values)))[-days_to_forecast]
      
      val_df = df[(df['ds'] >= test_forecast_date)]
      train_df = df[(df['ds'] < test_forecast_date)]
      
      forecast = self.forecast_w_prophet(train_df, days_to_forecast, mode, m_fo, w_fo, y_fo, err='no')
      
      slim_forecast = forecast[['ds', 'yhat']][forecast['ds'] >= test_forecast_date]
      MAE_df = val_df.merge(slim_forecast, on=['ds'])
      MAE_df['abs_diff'] = (MAE_df['y'] - MAE_df['yhat']).abs()
      MAE_list = list(MAE_df['abs_diff'].values)
      MAE_num = sum(MAE_list)/len(MAE_list)

      return MAE_num

  def country_wide_prediction(self, country, confirmed_df, deaths_df, recovered_df, days_to_forecast):
    
    worldwide_forecast = pd.DataFrame()

    params = []

    country_dfs, states_in_country = self.confirm_country_states(country, confirmed_df, deaths_df, recovered_df)
    all_results, params = self.state_level_forecasting(country, country_dfs, states_in_country, days_to_forecast)
    all_results["parameters"] = params

    if worldwide_forecast.empty:
      worldwide_forecast = all_results
    else:
      worldwide_forecast = worldwide_forecast.append(all_results)
            
    return worldwide_forecast

  def parallel_scoring(self, cpu_count = int(mp.cpu_count() - 2)):
    confirmed_df = pd.read_csv(config.get('score_dataset', 'confirmed_data'))
    deaths_df = pd.read_csv(config.get('score_dataset', 'deaths_data'))
    recovered_df = pd.read_csv(config.get('score_dataset', 'recovered_data'))
    countries = confirmed_df['Country'].unique()
    # countries = ["Canada", "Australia"]
    
    # for testing/debugging
    # for country in countries:
    #   results = self.country_wide_prediction(country, confirmed_df, deaths_df, recovered_df, 7)

    pool = mp.Pool(cpu_count)
    results = [pool.apply(self.country_wide_prediction, args=(country, confirmed_df, deaths_df, recovered_df, 7)) for country in countries]
    pool.close()
    results_df = pd.concat(results)
    results_df.to_csv(config.get('score_dataset', 'final_data'))

if __name__ == "__main__":

  take_a_guess = whats_up_with_covid()
  take_a_guess.parallel_scoring()
