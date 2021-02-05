import sys, os

if sys.version_info[0] < 3:
    raise Exception("Outdated Python Version! Must be using Python 3")

# CONSTANTS. Change these for input output dirs
# =========================================
INPUT_DIR = "wiki/"
OUTPUT_DIR = "bin/"
# =========================================

if len(sys.argv) < 2:
  print("Please specify the files to rebuild.")
  exit()

loadedBase = False
base0 = None
baseF = None
baseI = "      "
nextI = "  "

def loadBase():
  global loadedBase, base0, baseF
  
  if loadedBase:
    pass
  else:
    print("Loading template base.html")
    with open("base.html") as baseSource:
      data = baseSource.read().split("<!--INJHERE-->")
      #data.split(

for i in list(sys.argv)[1:]:
  print("Resolving " + i)
  inpt = INPUT_DIR + i
  try:
    with open(inpt if inpt.endswith(".md") else (inpt + ".md")) as source:
      md = source.read().splitlines()
  except FileNotFoundError:
    print("- Markdown Source not found.")

    post = OUTPUT_DIR + (i[:-3] if i.endswith(".md") else i) + ".html"
    if os.path.exists(post):
      a = input("- Bin HTML file found. Permanently Delete file? [Y/N] ")
      if (a.upper() == "Y"):
        os.remove(post)
      print("- Deleted file.")
    else:
      print("- Bin does not exist, cannot act on the given file.")
    continue
  
  print("- Transpiling " + i)

  html = ""
  
  for line in md:
    sline = line.strip()
    
    # basic stuff will be done better with tokens later
    if (sline.startswith("###")):
      html += ("<h3>" + sline[3:].strip() + "</h3>")
    elif (sline.startswith("##")):
      html += ("<h2>" + sline[2:].strip() + "</h3>")
    elif (sline.startswith("#")):
      html += ("<h1>" + sline[1:].strip() + "</h1>")
    else:
      html += ("<p>" + sline+ "</p>")
      
  post = OUTPUT_DIR + (i[:-3] if i.endswith(".md") else i) + ".html"
  postc = ""
  for j in post.split("/")[:-1]:
    postc += "/" + j
  postc = postc[1:]
  
  try:
    os.makedirs(postc)
  except FileExistsError:
    pass
  
  bin = open(post, "w+")
  bin.write(html)
  bin.close()
  