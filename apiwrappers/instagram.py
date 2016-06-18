import requests
import json
import responses.instagram

"""
    get all media by coordinates and radius
"""
def getMediaByCoordinates(lat, lng, token, dist = 5000):
    return requests.get("https://api.instagram.com/v1/media/search?"+\
                        "lat="+str(lat)+\
                        "&lng="+str(lng)+\
                        "&distance="+str(dist)+\
                        "&access_token="+token)


"""
    get all locations by coordinates and radius
"""
def getLocationByCoordinates(lat,lng, token, dist = 500):
    return requests.get("https://api.instagram.com/v1/locations/search?"+\
                        "lat="+str(lat)+\
                        "&lng="+str(lng)+\
                        "&distance="+str(dist)+\
                        "&access_token="+token)