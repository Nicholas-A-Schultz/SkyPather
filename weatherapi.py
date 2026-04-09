import requests
import re
import numpy as np
import math

windStations = {
        "EYW" : (24.556, -81.76),
        "JAX" : (30.494, -81.688),
        "MIA" : (25.795, -81.29),
        "MLB" : (28.103, -80.645),
        "PFN" : (30.358, -85.796),
        "PIE" : (27.909, -82.687),
        "TLH" : (30.397, -84.351),
        "ATL" : (33.637, -84.428),
        "CSG" : (32.516, -84.939),
        "SAV" : (32.128, -81.202),
        "HAT" : (35.233, -75.618),
        "ILM" : (34.271, -77.903),
        "RDU" : (35.878, -78.787),
        "CAE" : (33.939, -81.12),
        "CHS" : (32.899, -80.041),
        "FLO" : (34.185, -79.724),
        "GSP" : (34.896, -82.219),
        "2XG" : (29.600, -86.500)
        }

class windPoint:
    def __init__(self, code, latitude, longitude):
        self.code = code
        self.latitude = latitude
        self.longitude = longitude
        self.windsAloft = {
                3000 : (0,0,0),
                6000 : (0,0,0),
                9000 : (0,0,0),
                12000 : (0,0,0)
                }
    def setWind(self, altitude, windString):
        match = re.fullmatch(r"(\d{2})(\d{2})([+-]\d{2})?", windString)
        direction, speed, temp = match.groups()
        direction = int(direction) * 10
        speed = int(speed)
        # If temperature is none, that means no risk of icing
        temp = int(temp) if temp else None
        if direction == 990:
            direction = 0
        self.windsAloft[altitude] = (direction,speed,temp)

windPoints = []
def populateWindData():
    raw = requests.get("https://aviationweather.gov/api/data/windtemp?region=mia&level=low&fcst=06")
    requestText = raw.text
    # Finding the FT line
    index = 0
    found = False
    data = requestText.splitlines()
    while not found:
        if ("FT" in data[index]):
            found=True
        index +=1

    for i in range(index, len(data)):
        values = data[i].split(" ")
        code = values[0]
        coords = windStations[code]
        wp = windPoint(code, coords[0], coords[1])
        for j in range(1,5):
            altitude = j*3000
            wp.setWind(altitude,values[j])
            windPoints.append(wp)
    

def getWindData(lat, lon, alt, power=2):

    def interp_angle(a1, a2, t):
        a1 = math.radians(a1)
        a2 = math.radians(a2)

        x = math.cos(a1) * (1 - t) + math.cos(a2) * t
        y = math.sin(a1) * (1 - t) + math.sin(a2) * t

        return (math.degrees(math.atan2(y, x)) + 360) % 360

    def angle_to_vec(a, w):
        r = math.radians(a)
        return np.array([math.cos(r) * w, math.sin(r) * w])

    def vec_to_angle(vx, vy):
        return (math.degrees(math.atan2(vy, vx)) + 360) % 360

    def dist(lat1, lon1, lat2, lon2):
        R = 6371 # Radius of the Earth
        p1, p2 = math.radians(lat1), math.radians(lat2)
        dp = math.radians(lat2 - lat1)
        dl = math.radians(lon2 - lon1)

        a = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
        return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    def vertical(winds):
        levels = sorted(winds.keys())

        if alt <= levels[0]:
            return winds[levels[0]]
        if alt >= levels[-1]:
            return winds[levels[-1]]

        for i in range(len(levels) - 1):
            z0, z1 = levels[i], levels[i + 1]
            if z0 <= alt <= z1:
                t = (alt - z0) / (z1 - z0)

                d0, s0, t0 = winds[z0]
                d1, s1, t1 = winds[z1]
                
                d = interp_angle(d0, d1, t)
                s = s0 + (s1 - s0) * t
                if (t0 == None or t1 == None):
                    tmp = None
                else:
                    tmp = t0 + (t1 - t0) * t

                return d, s, tmp

    wind_vec = np.array([0.0, 0.0])
    speed_sum = 0.0
    temp_sum = 0.0
    wsum = 0.0

    for pt in windPoints:
        d, s, tmp = vertical(pt.windsAloft)

        d_km = dist(lat, lon, pt.latitude, pt.longitude)
        if d_km == 0:
            return d, s, tmp

        w = 1.0 / (d_km ** power)

        # direction as vector for correct averaging
        wind_vec += angle_to_vec(d, w)

        speed_sum += s * w
        if (tmp != None):
            temp_sum += tmp * w
        wsum += w

    direction = vec_to_angle(wind_vec[0], wind_vec[1])
    if (wsum == 0):
        wsum = 0.01
    speed = speed_sum / wsum
    temp = temp_sum / wsum

    return direction, speed, temp

