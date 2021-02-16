# covid_watch 
covid_watch predicts the week's COVID-19 cases, deaths and recoveries across the world.
These predictions are done at the state(province) granularity in each country the World Health Organization (WHO) has data available for.

## Usage
Everything is triggered from the main file.
Just run python -m (your_directory)/covid_watch

## Table of Contents
- covid_watch
  - data                          #^ all data for the pipeline rests here.
    - external                    #^ any secondary data can be stored here.
    - final                       #^ final scores stored here.
    - processed                   #^ raw data engineered for scoring stored here.
    - raw                         #^ raw data read in from WHO stored here.
  - logs                          #^ logs to track data quality stored here.
  - models                        #^ model artifacts can be stored here. Currently unused.
  - notebooks                     #^ notebooks to visualize the results
  - reports                       #^ more complete reports wil be stored here
  - src
    - config                      #^ config generator that provides inputs across the pipeline
    - data                        #^ all data read/cleaning/transformation scripts
    - models                      #^ script to conduct the scoring
  - utils.py                      #^ occasionally used for universal functions across pipeline
  - tests                         #^ unit tests can be found here

## Rough Explanation of the Process
There's three major modules used in this pipeline: make_dataset, process_dataset, and predictor_function.
make_dataset (src/data) reads the data from WHO website, appends it, then stores it in data/raw.
process_dataset (src/data) takes the make_dataset output, splits the dataset into confirmed, deaths, and recovered; then cleans/formats the datatypes,
storing them in data/processed.
predictor_function (src/models) takes each dataset for the current day and runs the Generative Additive Model across all countries in parallel.
Final results are the posted in data/final.

## License
[MIT](https://choosealicense.com/licenses/mit/)
