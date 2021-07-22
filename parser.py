#import numpy as np
import csv

def csv_to_dict(file_name):
    ratings = {}

    file_path = 'dataset/ratings/' + file_name
    with open(file_path, newline='\n') as csvfile:
        boxd_reader = csv.reader(csvfile, delimiter=',', quotechar='|')

        #iterate per line (comma separated)
        for entry in boxd_reader:
            
            #skip the header    
            if entry[0] == 'Date':
                continue
            
            #handling commas in title
            if len(entry) > 5:
                name = ','.join(entry[1:-3])
                name = name[1:-1] #stripping quotation marks?
                year = entry[3]
                stars = entry[-1] #ratings is taken
        
            #no commas in title
            else:
                name = entry[1]
                year = entry[2]
                stars = entry[4]

            key = name + ' (' + year + ')'

            ratings[key] = float(stars) * 2 #not a string, also /10
    
    return ratings

test = csv_to_dict('mal tose.csv')
print(test)