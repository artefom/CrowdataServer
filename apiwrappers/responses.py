
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
        return self.socialMedia + ":" + self.data['id']
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
