import sys

if len(sys.argv) < 2:
  print("Please specify the files to rebuild.")
  exit()

for i in list(sys.argv)[1:]:
  print("Transpiling " + i)
  