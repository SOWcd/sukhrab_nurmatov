import re
txt = "The rain in Almaty"
x = re.search("^The.*Almaty$", txt)
if x:
  print("YES! We have a match!")
else:
  print("No match")