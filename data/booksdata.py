#Populate the database
import json

data = []
with open("./data/books.csv","r") as f:
  count=1
  for line in f:
    if '"' in line:
      continue
    try:
      x = line.replace("\n", "").split(",")
      title = str(x[1])+" "+str(x[2])
      author = x[3].split(";")[0].replace(" ","")
      author = "".join([i for i in author if i not in " ,.;'\/-_"])
      obj = {
        "_id": str(count).zfill(5)+author[:3].upper(),
        "title": title.strip(),
        "authors": [i for i in x[3].split(";")],
        "avail": True,
        "pgs": int(x[4]),
        "isbn": str(x[0]),
      }
      data.append(obj)
      count+=1
    except:
      print(line)
  newfile = open("./data/books.json", "w")
  json.dump(data, newfile)
  newfile.close()