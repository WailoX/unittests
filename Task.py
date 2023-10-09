import json
import requests

class DataProcessor:
    def __init__(self):
        self.replacement_mapping = {}

    def load_replacements(self, file_path):
        with open(file_path, 'r') as replacement_file:
            replacements = json.load(replacement_file)
        return replacements

    def load_original_data(self, data_url):
        response = requests.get(data_url)
        original_data = json.loads(response.text)
        return original_data

    def apply_replacements(self, original_data, replacements):
        fixed_data = []
        for message in original_data:
            for replacement_obj in replacements:
                replacement = replacement_obj['replacement']
                source = replacement_obj['source']
                if source is not None:
                    message = message.replace(replacement, source)
                else:
                    message = message.replace(replacement, '')
            if message.strip():
                fixed_data.append(message)
        return fixed_data

    def save_result(self, data, file_path):
        with open(file_path, 'w') as result_file:
            json.dump(data, result_file, indent=4)

if __name__ == '__main__':
    data_processor = DataProcessor()
    replacements = data_processor.load_replacements('replacement.json')
    data_url = 'https://raw.githubusercontent.com/thewhitesoft/student-2023-assignment/main/data.json'
    original_data = data_processor.load_original_data(data_url)

    fixed_data = data_processor.apply_replacements(original_data, replacements)

    data_processor.save_result(fixed_data, 'result.json')
