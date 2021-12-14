import math
from scipy.stats import t

def cloudCode(data):
	data = data.replace(to_replace="10%  или менее, но не 0", value=10)
	data = data.replace(to_replace="90  или более, но не 100%", value=90)
	data = data.replace(to_replace="Облаков нет.", value=0)
	data = data.replace(to_replace="Небо не видно из-за тумана и/или других метеорологических явлений.", value=0)
	data = data.replace(to_replace="20–30%.", value=20)
	data = data.replace(to_replace="40%.", value=40)
	data = data.replace(to_replace="50%.", value=50)
	data = data.replace(to_replace="60%.", value=60)
	data = data.replace(to_replace="70 – 80%.", value=70)
	data = data.replace(to_replace="100%.", value=100)

	return data


def windCode(data):
	data = data.replace(to_replace="Ветер, дующий с северо-северо-востока", value="ССВ")
	data = data.replace(to_replace="Ветер, дующий с северо-востока", value="СВ")
	data = data.replace(to_replace="Ветер, дующий с востоко-северо-востока", value="ВСВ")
	data = data.replace(to_replace="Ветер, дующий с востока", value="В")
	data = data.replace(to_replace="Ветер, дующий с востоко-юго-востока", value="ВЮВ")
	data = data.replace(to_replace="Ветер, дующий с юго-востока", value="ЮВ")
	data = data.replace(to_replace="Ветер, дующий с юго-юго-востока", value="ЮЮВ")
	data = data.replace(to_replace="Ветер, дующий с юга", value="Ю")
	data = data.replace(to_replace="Ветер, дующий с юго-юго-запада", value="ЮЮЗ")
	data = data.replace(to_replace="Ветер, дующий с юго-запада", value="ЮЗ")
	data = data.replace(to_replace="Ветер, дующий с западо-юго-запада", value="ЗЮЗ")
	data = data.replace(to_replace="Ветер, дующий с запада", value="З")
	data = data.replace(to_replace="Ветер, дующий с западо-северо-запада", value="ЗСЗ")
	data = data.replace(to_replace="Ветер, дующий с северо-запада", value="СЗ")
	data = data.replace(to_replace="Ветер, дующий с северо-северо-запада", value="ССЗ")
	data = data.replace(to_replace="Ветер, дующий с севера", value="С")
	data = data.replace(to_replace="Штиль, безветрие", value="None")
	data["DD"] = data["DD"].fillna("None")

	return data


def windRadians(wdata):
	wdata = wdata.replace(to_replace="ССВ", value="22.5")
	wdata = wdata.replace(to_replace="СВ", value="45")
	wdata = wdata.replace(to_replace="ВСВ", value="67.5")
	wdata = wdata.replace(to_replace="В", value="90")
	wdata = wdata.replace(to_replace="ВЮВ", value="112.5")
	wdata = wdata.replace(to_replace="ЮВ", value="135")
	wdata = wdata.replace(to_replace="ЮЮВ", value="157.5")
	wdata = wdata.replace(to_replace="Ю", value="180")
	wdata = wdata.replace(to_replace="ЮЮЗ", value="202.5")
	wdata = wdata.replace(to_replace="ЮЗ", value="225")
	wdata = wdata.replace(to_replace="ЗЮЗ", value="247.5")
	wdata = wdata.replace(to_replace="З", value="270")
	wdata = wdata.replace(to_replace="ЗСЗ", value="292.5")
	wdata = wdata.replace(to_replace="СЗ", value="315")
	wdata = wdata.replace(to_replace="ССЗ", value="337.5")
	wdata = wdata.replace(to_replace="С", value="360")

	return wdata


def numbToMonth(month):
	name = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
	        "November", "December"]
	return name[month - 1]


def avgGeometryDirections(directions, speeds):
	sinSum = 0.0
	cosSum = 0.0
	for value, speed in zip(directions, speeds):
		sinSum += speed * math.sin(math.radians(value))
		cosSum += speed * math.cos(math.radians(value))
	sinSum = sinSum / len(directions)
	cosSum = cosSum / len(directions)
	return ((math.degrees(math.atan2(sinSum, cosSum)) + 360) % 360), math.sqrt(cosSum * cosSum + sinSum * sinSum)

d, sp = avgGeometryDirections([90, 90, 270, 180], [1, 1, 4, 5])

def tValue (len):
	tVal = t.ppf(.95, len-1)
	return tVal

def coInt (mo,tVal, sko, len):
	left = mo - tVal*(sko / math.sqrt(len))
	right = mo + tVal*(sko / math.sqrt(len))
	return left, right

print (d, sp)