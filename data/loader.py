import os

link_file = open("data/salary_links.txt", "r")

line = "TEMP"
while line:
  name = link_file.readline().strip()
  link = link_file.readline().strip()

  print("Running script for {}...".format(name))
  os.system("python data/data_to_db.py {} {}".format(name, link))
  print("Done.")
