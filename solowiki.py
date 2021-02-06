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

class Token:
  def __init__(self, dat, istext):
    self.data = data
    self.text = istext

HEADER = Token("/H1", False)
SUBHEADER = Token("/H2", False)
SUBHEADER_2 = Token("/H3", False)
SUBHEADER_3 = Token("/H4", False)
BOLD = Token("/B", False)
ITALIC = Token("/I", False)
QUOTE = Token("/BQ", False)
LINK_START = Token("/LS", False)
LINK_MID = Token("/LM", False)
LINK_END = Token("/LE", False)
BREAK = Token("/NL", False)
HTML_NEWLINE = Token("/HNL", False)

tokenmap = {"# ": HEADER, "## ": SUBHEADER, "### ": SUBHEADER_2, "#### ": SUBHEADER_3, "**": BOLD, "''": ITALIC, "> ": QUOTE, "!{": LINK_START, "|": LINK_MID, "}": LINK_END}

def processToken(currentRun, tokenList):
  global tokenmap
  if currentRun in tokenmap:
    tokenList.append(tokenmap[currentRun]
    return True
  else:
    return False

for i in list(sys.argv)[1:]: # for each provided file
  print("Resolving " + i)
  inpt = INPUT_DIR + i
  try:
    mdFile = inpt.endswith(".md")
    if "." in inpt and not mdFile: # if an asset
      print("- File discovered to likely be an asset.")
      # asset nonsense
      if (os.path.exists(inpt)):
        print("--- Copying resource into bin.")
        outputpath = OUTPUT_DIR + i
        missingDirs(outputpath)
        shutil.copyfile(inpt, outputpath)
      else:
        print("--- Asset not present Skipping file.")
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
      print("--- Deleted file.")
    else:
      print("--- Bin does not exist, cannot act on the given file.")
    continue
  
  print("- Transpiling " + i)
  loadBase()

  metadata = md[0].split("|")
  base0Split = base0.split("<!--WIKINAMEHERE-->")
  
  if len(metadata) == 1:
    metadata.append("Unnamed Solowiki")
  
  html = base0Split[0] + metadata[1].strip() + base0Split[1] + "<h1 id=\"title\">" + metadata[0].strip() + "</h1>" + "\n"
  
  newLines = False
  tokens = []
  
  # Tokenise
  print("--- Tokenising")
  for line in md[1:]:
    sline = line.strip()
    
    if line == "":
      if newLines:
        tokens.append(BREAK)
      newLines = True
      continue # yes I am abusing continue statement deal with it
    else:
      newLines = False
    
    run = ""
    for char in line:
      run += char
      if run != "":
        if processToken(run, tokens):
          run = ""
    
    if run != "":
      processToken(run, tokens)
    
    tokens.append(HTML_NEWLINE)

  # Parse Tokens into HTML
  print("--- Parsing to HTML")
  
  # Finalise
  html += baseF
      
  post = OUTPUT_DIR + (i[:-3] if i.endswith(".md") else i) + ".html"
  missingDirs(post)
  
  bin = open(post, "w+")
  bin.write(html)
  bin.close()
  