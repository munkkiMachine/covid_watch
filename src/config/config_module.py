from pathlib import Path
from src import utils
import os
from configparser import ConfigParser
from datetime import datetime
parser = ConfigParser()

def create_config():

    parser.add_section('make_dataset')
    parser.set('make_dataset', 'url', 'https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports')
    parser.set('make_dataset', 'git_site_raw', 'https://raw.githubusercontent.com')
    parser.set('make_dataset', 'ext', 'csv')
    parser.set('make_dataset', 'training_range', '7')
    parser.set('make_dataset', 'ingestion_range', '30') #This needs to be at least 4 times greater than the training range.
    parser.set('make_dataset', 'output_file_name', 'who_covid_data')

    parser.add_section('process_dataset')
    parser.set('process_dataset', 'input_file_name', 'who_covid_data')
    parser.set('process_dataset', 'output_file_location', os.path.join(utils.get_project_root(), 'data', 'processed'))

    parser.add_section('score_dataset')
    parser.set('score_dataset', 'confirmed_data', os.path.join(utils.get_project_root(), 'data', 'processed', 'confirmed_{}.csv'.format(utils.current_date())))
    parser.set('score_dataset', 'deaths_data', os.path.join(utils.get_project_root(), 'data', 'processed', 'deaths_{}.csv'.format(utils.current_date())))
    parser.set('score_dataset', 'recovered_data', os.path.join(utils.get_project_root(), 'data', 'processed', 'recovered_{}.csv'.format(utils.current_date())))
    parser.set('score_dataset', 'final_data', os.path.join(utils.get_project_root(), 'data', 'final', 'results_{}.csv'.format(utils.current_date())))

    config_file = 'src/config/config.ini'
    with open(config_file, 'w') as f:
        parser.write(f)
    
    parser.read(config_file)
    return parser

config = create_config()
