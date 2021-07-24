#####
#
# Name: Andrew Calimlim
# UNI: amc2391
# Class: COMS 4901
# Date: 23 Jul 2021
#
#####

import csv
import os
import numpy as np

#####
#
# Input:
# A csv file name 
# 
# Function: 
# Parses file by commas
# into an actual dictionary of ratings with unique film title (year) keys
# Overwrites key values with most recent ratings since csv file is ordered by date
# 
# Output:
# Dictionary of ratings
#
#####

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

######
#
# Input:
# A file path of csv files
#
#
# Function:
# turns the csv files into an alphabetized matrix of ratings
# each user is a row, and each column is a film
# ratings are from 1-10, 0 indicates unseen (unrated viewings don't appear in ratings)
# how are we supposed to know how you feel about a movie without a rating???
#
#
# Output:
# - An (incomplete) matrix of all ratings per person
# - A dictionary indicate row, user correspondence
# - An alphabetized list of all films (column, film title correspondence)
#
######

def getMatrices(fp):

    all_films = set()
    indexes_dict = {}
    ratings_list = []

    i = 0
    directory = fp
    for filename in os.listdir(directory): #iterating per file

        ratings = getRatingsDict(filename) #parsing ratings csv file into ratings dict

        for film in ratings.keys(): #all movies represented in all_films
            all_films.add(film)

        indexes_dict[i] = filename
        ratings_list.append(ratings)

        i = i + 1

    all_films = sorted(all_films)

    #creating matrices
    ratings_matrix = np.zeros((len(ratings_list), len(all_films)))

    for i in range(len(ratings_list)):
        for j in range(len(all_films)):
            if all_films[j] in ratings_list[i]:
                ratings_matrix[i,j] = ratings_list[i][all_films[j]]

    return ratings_matrix, indexes_dict, all_films

##### Tests

test_fp = r'/Users/andrew/Documents/PROJ/dataset/ratings/'

A, who, films = getMatrices(test_fp)

U,S,V_T = np.linalg.svd(A)

s_1 = S[0]
u_1 = U[:,0]
v_1 = V_T[0,:]

#verify reshapes too
u_1 = np.reshape(u_1,(u_1.size, 1))
v_1 = np.reshape(v_1,(1, v_1.size))

A_r = np.matmul(s_1 * u_1, v_1)
print(A_r)

#aight cool now iterate a bunch and then we can approximate cool