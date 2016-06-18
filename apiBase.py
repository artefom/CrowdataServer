#Social media ENUMERATE:
class SOCIALMEDIAS:
    instagram = 1

"""
Базовый класс, представляющий общие характеристики даннх, извлечённых их различных соц. сетей
Предположительно общие данные:
    self.socialMedia - #название соц. сети (смотри enum выше)
    self.data = dict()
    self.data['coordinates'] - координаты данных
"""
class RawInfo:

    def __init__(self, socialMediaId, coordinates, id):
        self.data = dict()
        self.data['coordinates'] = coordinates
        self.data['socialMedia'] = socialMediaId
        self.data['id'] = id

    def __str__(self):
        return self.socialMedia + ":" + self.data['id']
    def __eq__(self,other):
        return self.data['socialMedia']==other.data['socialMedia'] and self.data['id']==other.data['id']
