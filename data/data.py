import json
#Populate database

data = []
with open("./data/books.csv","r") as f:
  for line in f:
    if '"' in line:
      continue
    try:
      x = line.replace("\n", "").split(",")
      title = str(x[1])+" "+str(x[2])
      obj = {
        "title": title.strip(),
        "authors": [i for i in x[3].split(";")],
        "avail": True,
        "pgs": int(x[4]),
        "isbn": str(x[0]),
      }
      data.append(obj)
    except:
      print(line)
  newfile = open("./data/data.json", "w")
  json.dump(data, newfile)
  newfile.close()