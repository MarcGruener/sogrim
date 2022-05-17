
from pathlib import Path
import pandas as pd
data = Path('Haltestellen.txt').read_text()
filename = 'Haltestellen.txt'
#data = np.array2string(data)

data = data.replace('<COORD>', '')
data = data.replace('</COORD>', '')
data = data.replace("      ", '')

data = data.split("\n<C1>")

Haltestellendaten = pd.DataFrame(columns = ['Gemeinde',"Long", 'Lat', 'Haltestelle'])


for i in data:
    if i == '    ':
        i = 1
    else:
        i = i.split("</C1>")
        i[1] = i[1].replace("</C2>\n    \n", '')
        i[1] = i[1].replace("\n<C2>", '')
        i[1] = i[1].replace("    ", '')
        Haltestellendaten = Haltestellendaten.append({'Gemeinde' : "","Long": i[0], 'Lat': i[1], "Haltestelle": 1},ignore_index = True)

print(Haltestellendaten)