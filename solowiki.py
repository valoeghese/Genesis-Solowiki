import sys, os

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
  input = INPUT_DIR + i
  with open(input if input.endswith(".md") else (input + ".md")) as source:
    md = source.read().splitlines()
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
      
  post = OUTPUT_DIR + "e/r/c" + (i[:-3] if i.endswith(".md") else i) + ".html"
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
  