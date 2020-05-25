import requests

#head request to user's portifolio

username = "hemaglox"
headUrlRequest = "https://letterboxd.com/" + username + "/"

r1 = requests.head(headUrlRequest)

# X-Letterboxd-Identifier': gives the LID of the member
LID = r1.headers['X-Letterboxd-Identifier']

#401 error: not authenticated yet
#TODO: do Authentication step from letterboxd api
# good hint https://oauthlib.readthedocs.io/en/latest/oauth2/endpoints/token.html
# http://api-docs.letterboxd.com/#path--member--id- reference too

"""
r2 = requests.get("https://api.letterboxd.com/api/v0/member/{id}", \
    params = {"id" : LID})
"""
"""
r2 =  requests.get("https://api.letterboxd.com/api/v0/member/" + LID, \
    auth=('hemaglox', 'st4ycl4ssy'))
print(r2.status_code)
"""

