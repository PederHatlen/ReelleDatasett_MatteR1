import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from json import loads

# Laste data fra JSON fil (Har tidligere gode erfaringer med json)
# "data" blir et objekt/Dictionary
data = loads(open("data/egneObservasjoner.json", "r").read())

# Deklarere Arrayer som brukes til lagring av punktdata
# Numpy fprdi det er lettere å konvertere typer
xArr = np.array([])
avgArr = np.array([])
fmargArr = np.array([])

# For alle målinger, regn ut gjennomsnitt, standardavvik, standardfeil og feilmargin
for i in data:
    print("\n"+i,"cm fra start:", data[i])
    tmpArr = np.array(data[i]).astype(float)

    arrLen = len(tmpArr)
    arrSum = sum(tmpArr)
    
    # Kalkulering av verdier
    avgVal = arrSum / arrLen
    STDavvik = np.sqrt(sum((tmpArr - avgVal)**2) / (len(tmpArr) - 1))
    STDFeil = STDavvik / np.sqrt(arrLen)
    fMarg = 2*STDFeil

    # Kalkulerte verdier blir lagt inn i arrayer
    xArr = np.append(xArr, i)
    avgArr = np.append(avgArr, avgVal)
    fmargArr = np.append(fmargArr, fMarg)

    print("Gjennomsnittet er:", round(avgVal, 5))
    print("Standardavvik er:", round(STDavvik, 5))
    print("Standardfeil er:", round(STDFeil, 5))
    print("Feilmargin er:",round(fMarg, 5))

# Konvertere til lister, bedre med en liste for mye en feil typer.
x = xArr.astype(int).tolist()
y = avgArr.astype(float).tolist()

# Kalkulerings funksjon
def objective(x, a, b): 
    return a*b**x

# finne objective sine tilnermede konstantledd
fit = curve_fit(objective, x, y, [41, 0.8])

a = fit[0][0]
b = fit[0][1]

print(f"\na={a}\nb={b}")

x_values = np.linspace(0, 130)
y_values = objective(x_values, a, b)

# Tegne Punkt, Variasjon og Regresejonsgraf
plt.plot(x_values, y_values, "--", color="Green")
plt.vlines(x, y - 2*fmargArr, y + 2*fmargArr, "r")
plt.scatter(x, y)

plt.xlabel("Lengde (CM)")
plt.ylabel("Tid (Sekunder)")
plt.title("Egne observasjoner (bane vogn)")
plt.grid(True)
plt.show()