import sys

# CONSTANTS. Change these for input output dirs
# =========================================
INPUT_DIR = "wiki/"
OUTPUT_DIR = "bin/"
# =========================================

if len(sys.argv) < 2:
  print("Please specify the files to rebuild.")
  exit()

for i in list(sys.argv)[1:]:
  print("Transpiling " + i)
  i = INPUT_DIR + i
  with open(i if i.endswith(".md") else (i + ".md")) as source:
    md = source.read().splitlines()
  html = []
  
  for line in md:
    sline = line.strip()
    
    # basic stuff will be done better with tokens later
    if (sline.startswith("###")):
      html.append("<h3>" + sline[3:] + "</h3>")
    elif (sline.startswith("##")):
      html.append("<h2>" + sline[2:] + "</h3>")
    elif (sline.startswith("#")):
      html.append("<h1>" + sline[1:] + "</h1>")
    else:
      html.append("<p>" + sline+ "</p>")
      
    print(html[0])