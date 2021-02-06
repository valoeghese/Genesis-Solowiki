import sys, os, shutil

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
baseI = "          "
nextI = "  "

def loadBase():
  global loadedBase, base0, baseF
  
  if loadedBase:
    pass
  else:
    print("- Loading template base.html")
    loadedBase = True
    with open("base.html") as baseSource:
      data = baseSource.read().split("<!--INJHERE-->")
      base0 = data[0]
      baseF = data[1]

def missingDirs(post): # create missing directories
  postc = ""
  for j in post.split("/")[:-1]:
    postc += "/" + j
  postc = postc[1:]
  
  try:
    os.makedirs(postc)
  except FileExistsError:
    pass

for i in list(sys.argv)[1:]: # for each provided file
  print("Resolving " + i)
  inpt = INPUT_DIR + i
  try:
    mdFile = inpt.endswith(".md")
    if "." in inpt and not mdFile: # if an asset
      print("- File discovered to likely be an asset.")
      # asset nonsense
      if (os.path.exists(inpt)):
        print("- Copying resource into bin.")
        outputpath = OUTPUT_DIR + i
        missingDirs(outputpath)
        shutil.copyfile(inpt, outputpath)
      else:
        print("- Asset not present Skipping file.")
      continue #abuse the continue statement again
    with open(inpt if mdFile else (inpt + ".md")) as source:
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
  loadBase()

  html = base0 + "<h1 id=\"title\">" + md[0] + "</h1>" + "\n"
  
  for line in md[1:]:
    sline = line.strip()
    
    if line == "":
      html += baseI + "<br/>\n"
      continue # yes I am abusing continue statement deal with it
    
    # basic stuff will be done better with tokens later
    if (sline.startswith("###")):
      html += baseI + ("<h3>" + sline[3:].strip() + "</h3>")
    elif (sline.startswith("##")):
      html += baseI + ("<h2>" + sline[2:].strip() + "</h3>")
    elif (sline.startswith("#")):
      html += baseI + ("<h1>" + sline[1:].strip() + "</h1>")
    else:
      html += baseI + ("<p>" + sline+ "</p>")
    html += "\n"
  html += baseF
      
  post = OUTPUT_DIR + (i[:-3] if i.endswith(".md") else i) + ".html"
  missingDirs(post)
  
  bin = open(post, "w+")
  bin.write(html)
  bin.close()
  