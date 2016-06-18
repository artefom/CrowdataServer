import dataCells
from math import sin, cos, sqrt, atan2, radians

mat = None

def SetGlobalParameters():
    global mat
    if (mat == None):
        print('setting up mat')
        mat = dataCells.DataMatrix(5)

def geoDistance(coord1,coord2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(coord1[0])
    lon1 = radians(coord1[1])
    lat2 = radians(coord2[0])
    lon2 = radians(coord2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance;

def getCircles(lat1,lng1,lat2,lng2):
    global mat
    circles = mat.dataCell.getCircles(
                                        ((lat1,lng1),
                                        (lat2,lng2))
                                    )
    return circles