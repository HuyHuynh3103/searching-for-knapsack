DATASET_SIZE = 'dataset_size'
NUMBER_OF_CLASS = 'number_of_class'
INPUT_FILE = 'input_file'
OUTPUT_FILE = 'output_file'
class Config: 
    def __init__(self) -> None:
        self.settings = {
            DATASET_SIZE: 10,
            NUMBER_OF_CLASS: 7,
            INPUT_FILE: 'INPUT_10.txt',
            OUTPUT_FILE: 'OUTPUT_10.txt',
        }
    def get_setting(self, key):
        return self.settings.get(key)
    
    def set_setting(self, key, value):
        self.settings[key] = value
