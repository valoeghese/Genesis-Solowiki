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
  print("Resolving " + i)
  input = INPUT_DIR + i
  try:
    with open(input if input.endswith(".md") else (input + ".md")) as source:
      md = source.read().splitlines()
  except FileNotFoundError:
    print("Markdown Source not found.")

    post = OUTPUT_DIR + (i[:-3] if i.endswith(".md") else i) + ".html"
    if os.path.exists(post):
      a = input("Bin HTML file found. Permanently Delete file? [Y/N] ")
      if (a.upper() == "Y"):
        os.remove(post)
      print("Deleted file.")
    else:
      print("Bin does not exist, cannot act on the given file.")
    continue
  
  print("Transpiling " + i)

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
  