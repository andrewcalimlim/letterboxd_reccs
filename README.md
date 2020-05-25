# letterboxd_reccs

A reccomendation algorithm for Letterboxd and Criterion Channel users.
http://letterboxd.com/
http://criterion.com/channel

Process:

-Get list of movies on the Criterion Channel
-Get user's ratings of movies on the Criterion Channel from the Letterboxd API
-Get ratings of Criterion Channel movies by other Letterboxd users followed by said user
-Build ratings matrix with user x movie dimensions (possibly in MATLAB)
-Apply iterative SVD matrix decomposition to approximate ratings for movies not seen by user
-Sort approximate ratings by highest to lowest
-Remove movies seen by user (possibly not rated)
-Return sorted list of movies to watch to user


Challenges:
-There is no public Criterion Channel API, VHX tv api might work? includes all the extras though too
-Letterboxd API is closed beta, need to send what I have so far
-Moved program to Python because doing HTTP requests in Java looks like a mess
-Have never done HTTP requests before, thanks Columbia
