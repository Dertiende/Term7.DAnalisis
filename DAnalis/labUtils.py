# температура, влажность, ветер
# дисперсия, среднее, среднее квадратич. отклонение
import matplotlib
from scipy import ndimage
import numpy as np
import seaborn
import pandas as pd

import matplotlib.pyplot as plt

# plt.plot([1,2,3,4,5],[1,2,3,4,5])
# plt.show()
pd.options.mode.chained_assignment = None


def numbToMonth(month):
	name = ["January", "February", "March", "April", "May", "June",
	        "July", "August", "September", "October", "November", "December"]
	return name[month - 1]


def gistTemp(day, night, month):
	day["time"] = "day"
	day = day[day["Time"].dt.month == month]
	varDay = day.var()["T"]
	moDay = day["T"].mean()

	night = night[night["Time"].dt.month == month]
	moNight = night["T"].mean()
	varNight = night.var()["T"]
	temp = pd.concat([day["T"], night["T"], day["time"]], axis=1, keys=["all", "night", "time"])
	temp["all"] = temp["all"].fillna(temp["night"])
	temp["time"] = temp["time"].fillna("night")
	temp = temp.drop(columns="night")
	temp["all"] = temp["all"].replace(to_replace="None", value=np.nan)
	plt.title("Temperature " + numbToMonth(month))
	# print(temp)
	seaborn.histplot(data=temp, x="all", hue="time", multiple="layer", bins=30)
	plt.show()
	print("Мат. ожидание дневное: ", moDay)
	print("Мат. ожидание ночное: ", moNight)
	print("Дисперсия дневная: ", varDay)
	print("Дисперсия ночная: ", varNight)


def gistHum(day, night, month):
	day["time"] = "day"
	day = day[day["Time"].dt.month == month]
	varDay = day.var()["U"]
	moDay = day["U"].mean()

	night = night[night["Time"].dt.month == month]
	moNight = night["U"].mean()
	varNight = night.var()["U"]
	temp = pd.concat([day["U"], night["U"], day["time"]], axis=1, keys=["all", "night", "time"])
	temp["all"] = temp["all"].fillna(temp["night"])
	temp["time"] = temp["time"].fillna("night")
	temp = temp.drop(columns="night")
	temp["all"] = temp["all"].replace(to_replace="None", value=np.nan)
	plt.title("Humidity " + numbToMonth(month))
	# print(temp)
	seaborn.histplot(data=temp, x="all", hue="time", multiple="layer", bins=30)
	plt.show()



def gistWind(data, month):
	N = 16
	theta = np.arange(0.,2 * np.pi, 2 * np.pi / N)
	radii = np.array([4,7,5,3,1,5,6,7,4,3,5,6,2,4,4,6])
	ax = plt.axes([0.025, 0.025, 0.95, 0.95], polar=True)
	colors = np.array(['#4bb2c5','#c5b47f','#EAA228','#579575','#839557','#958c12','#953579','#4b5de4'])
	bars = plt.bar(theta, radii, width=(2*np.pi/N), bottom=0.0, color=colors)
	ax.set_theta_zero_location("N")

	plt.show()


def gistCloud(data, month):
	pass


def gistPres(data, month):
	pass


def windCode(data):
	data = data.replace(to_replace="Ветер, дующий с северо-северо-востока", value="22.5")
	data = data.replace(to_replace="Ветер, дующий с северо-востока", value="45")
	data = data.replace(to_replace="Ветер, дующий с востоко-северо-востока", value="67.5")
	data = data.replace(to_replace="Ветер, дующий с востока", value="90")
	data = data.replace(to_replace="Ветер, дующий с востоко-юго-востока", value="112.5")
	data = data.replace(to_replace="Ветер, дующий с юго-востока", value="135")
	data = data.replace(to_replace="Ветер, дующий с юго-юго-востока", value="157.5")
	data = data.replace(to_replace="Ветер, дующий с юга", value="180")
	data = data.replace(to_replace="Ветер, дующий с юго-юго-запада", value="202.5")
	data = data.replace(to_replace="Ветер, дующий с юго-запада", value="225")
	data = data.replace(to_replace="Ветер, дующий с западо-юго-запада", value="247.5")
	data = data.replace(to_replace="Ветер, дующий с запада", value="270")
	data = data.replace(to_replace="Ветер, дующий с западо-северо-запада", value="292.5")
	data = data.replace(to_replace="Ветер, дующий с северо-запада", value="315")
	data = data.replace(to_replace="Ветер, дующий с северо-северо-запада", value="337.5")
	data = data.replace(to_replace="Ветер, дующий с севера", value="360")
	data = data.replace(to_replace="Штиль, безветрие", value="None")
	data["DD"] = data["DD"].fillna("None")

	return data


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

data = pd.read_csv("27532.01.01.2020.01.01.2021.1.0.0.ru.utf8.00000000.csv", index_col=False, skiprows=6,
                   encoding="utf-8", sep=";")
data.rename(columns={"Местное время во Владимире": "Time"}, inplace=True)
data["Time"] = pd.to_datetime(data["Time"])
data = data.drop(
	columns=["Cl", "Ch", "Cm", "E", "Tg", "E'", "sss", "VV", "H", "Nh", "WW", "W1", "H",
	         "W2", "tR", "ff10", "ff3", "RRR", "Tx", "Td", "Tn", "P"])
data = data.sort_values(by="Time")
data = windCode(data)
dfDay = data[(data["Time"].dt.hour >= 9) & (data["Time"].dt.hour < 21)]
dfNight = data[(data["Time"].dt.hour >= 0) & (data["Time"].dt.hour < 9) | (data["Time"].dt.hour >= 21) & (
		data["Time"].dt.hour < 24)]
print("======================================================")
print(dfDay)
dfDay["T"] = pd.to_numeric(dfDay["T"], errors="coerce")
print("======================================================")

for month in range(1, 12):
	gistTemp(dfDay, dfNight, month)
	gistHum(dfDay,dfNight,month)
# print(dfDay[dfDay["Time"].dt.month == 2])