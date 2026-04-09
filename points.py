import matplotlib.pyplot as plt
import math
import colorsys
import weatherapi as wx

class fix:
    def __init__(self, code, latitude, longitude):
        self.code = code
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.neighbors = []
        self.isAirport = False

    def isNeighbor(self, neighbor):
        return neighbor in self.neighbors;

    def addNeighbor(self, neighbor):
        if not self.isNeighbor(neighbor):
            self.neighbors.append(neighbor)
        if not neighbor.isNeighbor(self):
            neighbor.addNeighbor(self)

    def distanceTo(self, nav):
        latdiff = self.latitude - nav.latitude
        longdiff = self.longitude - nav.longitude
        return math.sqrt(latdiff*latdiff + longdiff*longdiff)

def getPictureCoords(fix):
    latcorner=31.307700
    latbottom=24.626464
    latsize=latcorner-latbottom
    longcorner=-87.947433
    longbottom=-79.565430
    longsize=longbottom-longcorner
    height=818
    width=713
    lat=fix.latitude
    long=fix.longitude
    latcoord = width*(latcorner-lat)/latsize
    longcoord= height * (long-longcorner)/longsize
    return (longcoord, latcoord)

def findFixByCode(fixes, code):
    for i in range(len(fixes)):
        if fixes[i].code == code:
            return fixes[i]

def readFixesFromFile(filename):
    file = open(filename, "r")
    content = file.read()
    file.close()

    fixes = contentToBasicFixes(content, False)
    
    for line in content.splitlines():
        values = line.split(",")
        cur = findFixByCode(fixes, values[0])
        for i in range(3,len(values)):
            newNeighbor = findFixByCode(fixes, values[i])
            if (newNeighbor != None):
                cur.addNeighbor(newNeighbor)
            else:
                print("[WARN] Could not find",values[i])
    return fixes

def contentToBasicFixes(content, isAirport):
    fixes = []
    for line in content.splitlines():
        values = line.split(",")
        if (len(values) >= 3):
            code = values[0]
            latitude = values[1]
            longitude = values[2]
            f = fix(code, latitude, longitude)
            f.isAirport = isAirport
            fixes.append(f)
    return fixes

def readAirportsFromFile(filename, fixes):
    file = open(filename, "r")
    content = file.read()
    file.close()

    fixes += contentToBasicFixes(content, True)
    for airport in fixes:
        if (airport.isAirport):
            for nav in fixes:
                if airport.distanceTo(nav) <= 0.25:
                    airport.addNeighbor(nav)

def plotFixesToGraph(fixes, ax):
    for i in fixes:
        coords = getPictureCoords(i)
        for j in i.neighbors:
            ncoords = getPictureCoords(j)
            ax.plot([coords[0], ncoords[0]], [coords[1], ncoords[1]], 'r-')
        if i.isAirport:
            ax.plot(coords[0], coords[1], marker='o', color='blue', markersize=10)
            ax.text(coords[0],coords[1], i.code)
        else:
            ax.plot(coords[0], coords[1], marker='o', color=windAsColor(i.latitude,i.longitude), markersize=5)

def windAsComplex(direction, speed):
    rDir = math.radians(90-direction)
    # 1 GPS degree = 60 knots
    windX = speed * math.cos(rDir) / 60
    windY = speed * math.sin(rDir) / 60
    return complex(windX, windY)

# For pretty map
def windAsColor(latitude, longitude, altitude=3000):
    direction, speed, temp = wx.getWindData(latitude, longitude, altitude)
    hue = direction / 360
    r,g,b = colorsys.hsv_to_rgb(hue, 1, 1)
    return r,g,b

def heuristic(fix1, fix2, altitude):
    # Begin with the direct distance between the points
    baseValue = fix1.distanceTo(fix2)
    # Find our intended vector
    intendedX = fix2.longitude - fix1.longitude
    intendedY = fix2.latitude - fix1.latitude
    intended = complex(intendedX, intendedY)

    print(intended)
    # Find the midpoint for the weather
    wxLat = (fix2.latitude + fix1.latitude) / 2
    wxLong = (fix2.longitude + fix2.longitude) / 2
    direction, speed, temp = wx.getWindData(wxLat, wxLong, altitude)
    wind = windAsComplex(direction, speed)
    print(wind)
    result = intended - wind
    print(result)

# Main Program
print("Fetching weather info from AviationWeather.gov...")
wx.populateWindData()
print("Fetched.")
fixes = readFixesFromFile("fixes.txt")
readAirportsFromFile("airports.txt", fixes)
fig, ax = plt.subplots()

# Plot the Florida map
img = plt.imread("florida.png")
ax.imshow(img)
# Plot all the fixes
plotFixesToGraph(fixes,ax)

# Get weather info

heuristic(findFixByCode(fixes, "KDAB"), findFixByCode(fixes, "KMLB"), 3000)

# Tada
plt.show()

