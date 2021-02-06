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
baseI = "        "
nextI = "  "

def loadBase():
  global loadedBase, base0, baseF
  
  if loadedBase:
    pass
  else:
    print("--- Loading template base.html")
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
  def __init__(self, dat, istext, opener, closer):
    self.data = dat
    self.text = istext
    if closer == None:
      self.tag = opener
    else:
      self.opener = opener
      self.closer = closer

HEADER = Token("/H1", False, "<h1>", "</h1>")
SUBHEADER = Token("/H2", False, "<h2>", "</h2>")
SUBHEADER_2 = Token("/H3", False, "<b>", "</b><br/>")
PARAHEADER = Token("/P", False, "<p>", "</p>")
BOLD = Token("/B", False, "<b>", "</b>")
ITALIC = Token("/I", False, "<i>", "</i>")
UNDERLINE = Token("/U", False, "<u>", "</u>")
QUOTE = Token("/BQ", False, "<div class=\"quote\">&nbsp;<q>", "</q></div>")
INLINE_QUOTE = Token("/IQ", False, "<q>", "</q>")
LINK_START = Token("/LS", False, "<a href=\"", None)
LINK_MID = Token("/LM", False, "\">", None)
LINK_END = Token("/LE", False, "</a>", None)
BREAK = Token("/NL", False, "<br/>", None)
RESET = Token("/R", False, None, None)

headers = [HEADER, SUBHEADER, SUBHEADER_2, QUOTE, PARAHEADER]
wrappers = [BOLD, ITALIC, UNDERLINE, INLINE_QUOTE]
simple = [BREAK, LINK_START, LINK_MID, LINK_END]
tokenmap = {"**": BOLD, "''": ITALIC, "__": UNDERLINE, "\"": INLINE_QUOTE, "{": LINK_START, "|": LINK_MID, "}": LINK_END}

def processToken(currentRun, tokenList, forceToken):
  global tokenmap
  if currentRun in tokenmap:
    tokenList.append(tokenmap[currentRun])
    return True
  else:
    for tokenkey in tokenmap:
      if currentRun.endswith(tokenkey):
        cutoffsize = len(tokenkey)
        tokenList.append(Token(currentRun[:-cutoffsize], True, None, None)) # add preceding text
        tokenList.append(tokenmap[tokenkey]) # add token
        return True
    if forceToken: # if force token make a text token
      tokenList.append(Token(currentRun, True, None, None))
      return True
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
  
  html = base0Split[0] + metadata[1].strip() + base0Split[1] + "<span id=\"title\"><h1>" + metadata[0].strip() + "</h1></span>" + "\n"
  
  newLines = False
  tokens = []
  
  # Tokenise
  print("--- Tokenising")
  for line in md[1:]:
    line = line.strip()
    
    if line == "":
      if newLines:
        tokens.append(BREAK)
      newLines = True
      continue # yes I am abusing continue statement deal with it
    else:
      newLines = False
    
    if line.startswith("###"):
      tokens.append(SUBHEADER_2)
      line = line[3:].strip()
    elif line.startswith("##"):
      tokens.append(SUBHEADER)
      line = line[2:].strip()
    elif line.startswith("#"):
      tokens.append(HEADER)
      line = line[1:].strip()
    elif line.startswith(">"):
      tokens.append(QUOTE)
      line = line[1:].strip()
    else:
      tokens.append(PARAHEADER)
    
    run = ""
    for char in line:
      run += char
      if run != "":
        if processToken(run, tokens, False):
          run = ""
    
    if run != "":
      processToken(run, tokens, True)
    
    tokens.append(RESET)

  # Parse Tokens into HTML
  print("--- Parsing to HTML")
  
  effects = {}
  
  html += baseI
  
  for token in tokens:
    if token.text:
      html += token.data
    elif token in headers:
      html += token.opener
      effects[token] = True
    elif token == RESET:
      for hd in headers:
        if effects.get(hd, False):
          html += hd.closer
          effects[hd] = False
      html += "\n" + baseI
    elif token in wrappers:
      if effects.get(token, False):
        html += token.closer
        effects[token] = False
      else:
        html += token.opener
        effects[token] = True
    elif token in simple:
      html += token.tag
    
  
  # Finalise
  html += baseF
      
  post = OUTPUT_DIR + (i[:-3] if i.endswith(".md") else i) + ".html"
  missingDirs(post)
  
  bin = open(post, "w+")
  bin.write(html)
  bin.close()
  