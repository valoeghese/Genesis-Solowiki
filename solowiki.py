import sys

if len(sys.argv) < 2:
  print("Please specify the files to rebuild.")
  exit()

for i in list(sys.argv)[1:]:
  print("Transpiling " + i)
  with source as open(i if i.endswith(".md") else (i + ".md")):
    md = f.readlines()
  html = []
  
  for line in md:
    sline = line.strip()
    
    # basic stuff will be done better with tokens later
    if (sline.startswith("###")):
      html.append("<h3>" + sline[3:] + "</h3>")
    elif (sline.startswith("##")):
      html.append("<h2>" + sline[2:] + "</h3>")
    elif (sline.startswith("#"):
      html.append("<h1>" + sline[1:] + "</h1>")
    else:
      html.append("<p>" + sline+ "</p>")
      
    git commit -m "loop thingy arguments brr"
    