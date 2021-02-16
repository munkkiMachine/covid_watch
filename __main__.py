if __name__ == "__main__":
    from src.config.config_module import config
    from src import utils
    from src.data.make_dataset import makeDataset
    from src.data.process_dataset import processDataset
    from src.models.predictor_function import whats_up_with_covid
    #TODO: figure out how to run predictor_function.py from here

    # read in raw data
    makeDataset(config.get("make_dataset", "url"), 
                    config.get("make_dataset", "git_site_raw"), 
                    config.get("make_dataset", "ext"),
                    config.get("make_dataset", "ingestion_range"), 
                    config.get("make_dataset", "output_file_name")).saveFileToRaw()

    # process data for scoring
    processDataset(input_file = "{}_{}.csv".format(config.get("process_dataset", "input_file_name"), utils.current_date()),
    output_file = config.get("process_dataset", "output_file_location")).process_dataset_to_processed()

    take_a_guess = whats_up_with_covid()
    take_a_guess.parallel_scoring()