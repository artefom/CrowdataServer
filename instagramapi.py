import requests
import json
import apiBase

def getMediaByCoordinates(lat, lng, token, dist = 5000):
    return requests.get("https://api.instagram.com/v1/media/search?"+\
                        "lat="+str(lat)+\
                        "&lng="+str(lng)+\
                        "&distance="+str(dist)+\
                        "&access_token="+token)

def getLocationByCoordinates(lat,lng, token, dist = 500):
    return requests.get("https://api.instagram.com/v1/locations/search?"+\
                        "lat="+str(lat)+\
                        "&lng="+str(lng)+\
                        "&distance="+str(dist)+\
                        "&access_token="+token)

"""
Представляет информацию, извлечённую из instagramm
"""
class RawInfo_instagram(RawInfo):
    def __init__(self):
        self.data = dict()
        self.data['socialMedia'] = SOCIALMEDIAS.instagram
        
    def __init__(self,json):
        self.data = dict()
        self.data['socialMedia'] = SOCIALMEDIAS.instagram
        self.data['location_id'] = json['location']['id']
        self.data['coordinates'] = [json['location']['latitude'],json['location']['longitude']]
        self.data['id'] = json['id']
        self.data['user_id'] = int(json['user']['id'])
        self.data['created_time'] = int(json['created_time'])
        self.data['likes_count'] = int(json['likes']['count'])
        self.data['comments_count'] = int(json['comments']['count'])
        self.data['tags'] = json['tags']
        self.data['image_url'] = json['images']['standard_resolution']['url']
    
    @staticmethod
    def listFromResponse(response):
        json_data = response.json()['data']
        
        result = []
        
        for pic in json_data:
            result.append(RawInfo_instagram(pic))
        
        return result