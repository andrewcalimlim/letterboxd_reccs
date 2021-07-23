import csv
import os
import numpy as np

###
# Parses csv file into an actual dictionary of ratings with unique film title (year) keys
# returns a dictionary
###
def getRatingsDict(file_name):
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

###
# Given a file path of csv files and specifying which csv file is "you"
# turns the csv files into an alphabetized matrix of ratings
# each user is a row, and each column is a film
# ratings are from 1-10, 0 indicates unseen (unrated viewings don't appear in ratings)
# how are we supposed to know how you feel about a movie without a rating???
#
# returns two matrices, one with all other users' ratings
# the other is "your" ratings
###

def getMatrices(fp, myfile):
    all_films = set()
    others_index = {}
    others_ratings = []
    my_ratings = {}

    i = 0
    directory = fp
    for filename in os.listdir(directory): #iterating per file

        ratings = getRatingsDict(filename) #parsing ratings csv file into ratings dict

        for film in ratings.keys(): #all movies represented in all_films
            all_films.add(film)

        if filename == myfile: #but only ratings get represented in the other data structs
            my_ratings = ratings
            continue

        others_index[i] = filename #this is just for debug, i may remove it for clarity later
        others_ratings.append(ratings)

        i = i + 1

    all_films = sorted(all_films)

    #print(all_films)

    #creating matrices
    others_matrix = np.zeros((len(others_ratings), len(all_films)))
    my_matrix = np.zeros((1, len(all_films)))

    for i in range(len(others_ratings)):
        for j in range(len(all_films)):
            if all_films[j] in others_ratings[i]:
                others_matrix[i,j] = others_ratings[i][all_films[j]]

    for i in range(len(all_films)):
        if all_films[i] in my_ratings:
            my_matrix[0,i] = my_ratings[all_films[i]]

    #print(others_index)

    return my_matrix, others_matrix

"""
test_fp = r'/Users/andrew/Documents/PROJ/dataset/ratings/'
test_myfile = 'me.csv'

mine, theirs = getMatrices(test_fp, test_myfile)
print(theirs)
"""
