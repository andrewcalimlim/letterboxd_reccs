#####
#
# Name: Andrew Calimlim
# UNI: amc2391
# Class: COMS 4901
# Date: 2 Aug 2021
#
#####

import csv
import os
import numpy as np
import copy
import feedparser

#####
#
# Input:
# A Letterboxd username
# 
# Function: 
# Gets RSS Feed for a Lbxd user and iterates over the last ~50 entries, ignoring lists and unrated entries
# 
# Output:
# Dictionary of ratings from that user
#
#####

def getRatingsDict(username):
    ratings = {}

    URL = 'https://letterboxd.com/' + username + '/rss/'

    NewsFeed = feedparser.parse(URL)

    for entry in NewsFeed.entries: #parse all existing entries

        # this key dne for list entries or unrated entries, which we ignore
        if 'letterboxd_memberrating' not in entry.keys():
            continue

        title = entry['letterboxd_filmtitle']
        year = entry['letterboxd_filmyear']
        stars = entry['letterboxd_memberrating']

        key = title + ' (' + year + ')'

        ratings[key] = float(stars) * 2 #not a string, also /10
    
    return ratings

######
#
# Input:
# A list of usernames (string format)

#
# Function:
# turns the list of strings into an alphabetized matrix of ratings
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

def getMatrices(users):

    all_films = set()
    indexes_dict = {}
    ratings_list = []

    i = 0
    for username in users:

        ratings = getRatingsDict(username) #parsing ratings csv file into ratings dict

        for film in ratings.keys(): #all movies represented in all_films
            all_films.add(film)

        indexes_dict[i] = username
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


######
#
# Input:
# - A matrix to do a rank1 approximation of
# - The original matrix (to reinstate existing values from)
#
# Function:
# Does a single rank 1 approximation of and then reinstates 
# existing values from the original
#
#
# Output:
# - A rank 1 approximation (1 iteration)
#
######

def rank1ApproximateOnce(A, original):
    U,S,V_T = np.linalg.svd(A)

    s_1 = S[0]
    u_1 = U[:,0]
    v_1 = V_T[0,:]

    #need to be 2-dimensional to do matrix multiplication
    u_1 = np.reshape(u_1,(u_1.size, 1))
    v_1 = np.reshape(v_1,(1, v_1.size))

    #rank 1 approximation (according to my linear algebra notes)
    A_r = np.matmul(s_1 * u_1, v_1)

    row,col = np.shape(A_r)
    for i in range(row):
        for j in range(col):
            if original[i,j] != 0:
                A_r[i,j] = original[i,j]
    return A_r

######
#
# Input:
# A convergence on rank 1 approximations of a matrix
#
#
# Function:
# 
# Iteratively rank 1 approximates a matrix until 
# a total 1e-5 difference in iteration outputs is reached
#
#
#
# Output:
# - An approximation of all possible ratings (via SVD)
#
######

def rank1Approximate(A):
    old = A
    new = copy.deepcopy(old)
    diff = float('inf')
    while diff > (1 * 10 ** -5):
        new = rank1ApproximateOnce(old, A)
        diff = np.sum(np.absolute(new - old))
        old = new
    return new

##### Tests

test_users = ['hemaglox', 'samuelio', 'jasonc8106', 'm3hr', 'hhodaie']

the_matrix, who, films = getMatrices(test_users)

recc = rank1Approximate(the_matrix)
my_ratings = the_matrix[0,:]
my_recc = recc[0,:]

print("Here's your recommendations, Andrew: ")

total = 0
while total < 5:
    index = np.argmax(my_recc)
    if my_ratings[index] == 0:
        line = '\t' + str(total + 1) + ') ' + films[index] 
        line = line + '\t| Expected Rating: ' + str(round(my_recc[index],2))
        print(line)
        total = total + 1
    my_recc[index] = float('-inf')


"""
Here's your recommendations, Andrew: 
        Rank) Title (Year)              | Expected Rating

        1) Fantastic Planet (1973)      | 9.57
        2) Schindler's List (1993)      | 9.57
        3) Angel (1937)                 | 9.02
        4) Autumn Sonata (1978)         | 9.02
        5) Jaws (1975)                  | 9.02
"""