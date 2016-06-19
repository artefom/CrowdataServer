import pickle


class SOCIALMEDIAS:
    instagram   = 1
    facebook    = 2
    facebook_event = 3


"""
Базовый класс, представляющий общие характеристики даннх, извлечённых их различных соц. сетей
Предположительно общие данные:
    self.socialMedia - #название соц. сети (смотри enum выше)
    self.data = dict()
    self.data['coordinates'] - координаты данных
"""
class base:

    def __init__(self, socialMediaId, coordinates, id):
        self.data = dict()
        self.data['coordinates'] = coordinates
        self.data['socialMedia'] = socialMediaId
        self.data['id'] = id

    def __str__(self):
        return str(self.data)
    def __eq__(self,other):
        return self.data['socialMedia']==other.data['socialMedia'] and self.data['id']==other.data['id']

"""
    Represents responses from instagram api
"""
class instagram(base):
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

class facebook(base):
    
    def __init__(self, id, json):
        super().__init__(SOCIALMEDIAS.facebook, 
            [json['location']['latitude'],json['location']['longitude']], 
            id )

    @staticmethod
    def listFromResponse(response):
        json_data = response.json()['data']
        
        result = []
        
        for pic in json_data:
            result.append(RawInfo_instagram(pic))
        
        return result

    @staticmethod
    def list_from_raw_data(data):
        newborns = []
        
        for id,v in data.items():
            newborns.append(facebook(id,v))

        return newborns

class facebook_event(base):

    def __init__(self, id, json):
        super().__init__(SOCIALMEDIAS.facebook_event, 
            [json['lat'],json['lng']], 
            id )
        self.data['data'] = json

    @staticmethod
    def list_from_raw_data(data):
        newborns = []
        
        for id,v in data.items():
            newborns.append(facebook_event(id,v))

        return newborns

    @staticmethod
    def list_from_file(filename):
        
        with open(filename,'rb') as file_data:
            raw_data = pickle.load(file_data)
    
            fbdata = facebook_event.list_from_raw_data(raw_data)

            return fbdata

        return []

