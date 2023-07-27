import csv
import os

dir_path = r'api_yamdb\static\data'
print(os.listdir(dir_path))

with open('api_yamdb\static\data\category.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        
        print(row)