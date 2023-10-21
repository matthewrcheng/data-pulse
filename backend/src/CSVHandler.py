import csv

class CSVHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_csv(self):
        data = []
        with open(self.file_path, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)
        return data
    
    def write_csv(self, data):
        with open(self.file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            for row in data:
                writer.writerow(row)