import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from json import loads
from requests import post
from string import ascii_letters as alphabet

pDegree = 3
newData = False

if(newData):
	post_url = "https://data.ssb.no/api/v0/no/table/03772/" # Skogsvei
	# post_url = "https://data.ssb.no/api/v0/no/table/11419/" # Månedslønn
	query = loads(open("query/skogsvei.json", "r").read())
	rawdata = post(post_url, json = query)
	data = rawdata.text
	open("data/cache.json", "w", encoding="utf_8").write(data)

# Laste data fra JSON fil (Har tidligere gode erfaringer med json)
# "data" blir et objekt/Dictionary
data = loads(open("data/cache.json", "r", encoding="utf_8").read())

# Deklarere Arrayer som brukes til lagring av punktdata
xArr = list(data["dimension"]["Tid"]["category"]["index"].values())
yArr = list(data["value"])

# Gjennomsnitt
avg = sum(data["value"])/len(data["value"])

# Numpy regresjonsanalyse (polynom) med pDegree som polynomgrad
model = np.poly1d(np.polyfit(xArr, yArr, pDegree))

# Printe alle konstantledd (skaleres rundt polynomgrad)
for i in range(len(model.coefficients)):
	print(alphabet[i],"=", model.coefficients[i])

plt.plot(xArr, model(xArr), "--", color="red")

plt.plot([0, max(xArr)], [avg, avg], "--", color="purple")
plt.scatter(xArr, yArr)

plt.title(data["label"])
plt.xlabel(data["dimension"]["Tid"]["label"])
plt.ylabel(list(data["dimension"]["ContentsCode"]["category"]["label"].keys())[0])
plt.grid(True)
plt.show()