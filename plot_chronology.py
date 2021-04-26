import json
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime
from labella.scale import LinearScale
from labella.scale import TimeScale
from labella.timeline import TimelineTex
import re
from datetime import date

def test_labella(struct, name):
  #tl = TimelineTex(struct, options={'scale': LinearScale()})
  tl = TimelineTex(struct, options={'scale': TimeScale()})
  tl.export(f"{name}.tex")


def test_chrono(names, dates, numb):
  levels = np.tile([-5, 5, -3,3, -1, 1],int(np.ceil(len(dates)/6)))[:len(dates)]
  fig, ax = plt.subplots(figsize=(8.8, 4), constrained_layout=True)
  ax.set(title="Chronologie MOreau")
  markerline, stemline, baseline = ax.stem(dates, levels,
                                         linefmt="C3-", basefmt="k-",
                                         use_line_collection=True)
  plt.setp(markerline, mec="k", mfc="w", zorder=3)
  markerline.set_ydata(np.zeros(len(dates)))
  vert = np.array(['top', 'bottom'])[(levels > 0).astype(int)]
  for d, l, r, va in zip(dates, levels, names, vert):
    ax.annotate(r, xy=(d, l), xytext=(-3, np.sign(l)*3),
                textcoords="offset points", va=va, ha="right")

  #ax.get_xaxis().set_major_locator(mdates.MonthLocator(interval=4))
  #ax.get_xaxis().set_major_formatter(mdates.DateFormatter("%b %Y"))
  plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
  ax.get_yaxis().set_visible(False)
  for spine in ["left", "top", "right"]:
    ax.spines[spine].set_visible(False)

  ax.margins(y=0.1)
  plt.show()

def open_json(path):
  f = open(path, encoding="utf-8")
  s = json.load(f)
  f.close()
  return s


path = "data/chronologie_moreau.json"
data = open_json(path)

base_graph_X = []
base_graph_Y = []

for year in range(1649, 1661):
  print(year)
  year = str(year)
  if year not in data:
#    base_graph_Y.append(0)
    continue
  names = []
  dates = []
  numb  = []
  liste_events = data[year]
  NB_textes = 0
  struct = []
  cpt = 0
  for event in liste_events:
    cpt+=1
    nb = len(event["liste"])
    NB_textes += nb 
    if event["date"]=="N/A":
      continue
    date_str  = event["date"]
    try:
      y = int(date_str[6:])
    except:
      continue
    m = int(date_str[3:5])
    d = int(date_str[:2])
    if d==0: d=1
    date_format = date(y, m, d)
    dates.append(date_format)
    name = event["Etiquette Moreau"]
    name = re.sub("’", "'", name)
    names.append(name[:20])
    numb.append(len(event["liste"]))
    struct.append({"time": date_format, "text": f"{date_str}: {name} ({nb})"})
  test_labella(struct, year)
  base_graph_X.append(year)
  base_graph_Y.append(NB_textes)
#  plt.title("Nombre de Mazarinades par évènement selon Moreau")
#  plt.plot(names, numb)
#  plt.savefig("figures/by_event_%s.png"%year)
#  plt.show()
#  test_chrono(names, dates, numb)
#  break
plt.clf()
plt.title("Nombre de Mazarinades par année selon Moreau")
plt.yscale("log")
plt.plot(base_graph_X, base_graph_Y)
plt.savefig("figures/base_graph.png")

#fig, ax = plt.subplots(figsize=(8.8, 4), constrained_layout=True)
#ax.set(title="Chronologie Moreau")
print(len(dates))
