from os.path import os, exists
from datetime import datetime, timedelta
from functools import *
import subprocess
import sys
import re
import difflib

outputFilename = 'assignment7.txt'
outputFile = open(outputFilename, 'a')
filename = "Deal.py"
dateString = "10-15-2013 23:00:00"

def main():
  out = subprocess.getoutput('ls ./')
  CSIDS = out.split("\n")
  if len(sys.argv) == 3:
    outputFile.write('CSID\tGrade\tComments\n')
    lowerBound = sys.argv[1]
    upperBound = sys.argv[2]
    myList = []
    count = 0
    for item in CSIDS :
      if ord(item[0]) in range(ord(lowerBound), ord(upperBound)+1) :
        if "." not in item :
          myList.append( item )
    for csid in myList :
      count += 1
      os.system('clear')
      print('======================')
      print(csid + " " + str(count) + " out of " + str(len(myList)))
      print('======================')
      assign6( csid , True)
  #singleton mode
  else:
    csid = sys.argv[1]
    os.system('clear')
    print('======================')
    print(csid)
    print('======================')
    assign6( csid , False)
  outputFile.close()

def assign6( csid , writeToFile) :
  fileToGrade = ""
  late = 0
  grade = 70
  style = 30
  wrongFileName = False
  header = True
  comments = " "

  os.chdir(csid)
  if writeToFile: outputFile.write(csid + "\t")
  files = os.listdir('.')

  #filename checking
  for f in files :
    splitted = subprocess.getoutput('ls -l ' + f).split()
    if f == filename :
      fileToGrade = filename
      late = isLate(splitted)
      break
    elif f == filename.lower() :
      fileToGrade = filename.lower()
      late = isLate(splitted)
      wrongFileName = True
      break

  #really odd filename
  if fileToGrade == "" :
    print(subprocess.getoutput('ls -l'))
    fileToGrade = input("Which file should I grade? ")
    if fileToGrade == "" :
      if writeToFile: 
        outputFile.write("0\tno file\n")
      os.chdir("..")
      return
    else :
      splitted = subprocess.getoutput('ls -l ' + fileToGrade.replace(' ','\ ')).split()
      late = isLate(splitted)
      wrongFileName = True

  #grading time!
  if not fileToGrade == "" and late != -1:
    out = "XXInterrputed sprobs will be set to 13X"
    process = subprocess.Popen(['python3', fileToGrade], stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    try:
      out = process.communicate(bytes('50000', 'UTF-8'))[0]
    except KeyboardInterrupt:
      pass
    #yup this next line of code is a little funky but yeah... it works and I'm lazy --Devin
    perfect = True
    wrong = False
    answer = (str(out)[2:-1]).replace('\\n','\n').rstrip().split('\n')
    try:
      switch = int(re.findall("\D+\d+\.(\d+)",answer[-2])[0])
      noSwitch = int(re.findall("\D+\d+\.(\d+)",answer[-1])[0])
    except IndexError:
      wrong = True
      perfect = False
      switch = 1337
      noSwitch = 1337
    #penalize for not rounding
    if switch > 99 or noSwitch > 99:
      perfect = False
      switch = round(int(str(switch)[:3]), -1) // 10
      noSwitch = round(int(str(noSwitch)[:3]), -1) // 10
    if perfect and switch + noSwitch == 100 and ( 66 <= switch <= 68) and (32 <= noSwitch <= 34):
      pass
      print("Perfect (feels nice to be nice =D)")
    elif not wrong and switch + noSwitch == 100 and (( 66 <= switch <= 68) or (32 <= noSwitch <= 34)):
      grade -= 10
      print("Close")
      print(answer[-2:])
      print("Prob when switching: " + str(switch) + " Prob when not switching: " +str(noSwitch))
      comments += "Somewhat wrong output!"
    else:
      grade -= 30
      print("Wrong")
      print(answer[-2:])
      print("Prob when switching: " + str(switch) + " Prob when not switching: " +str(noSwitch))
      comments += "Wrong output!"
  #checking for header and style
  #os.system('vim ' + fileToGrade)
  input("Hit Enter to cat")
  print(subprocess.getoutput('cat ' + fileToGrade))
  headerInput = input("Header( (y or enter)  /  n)? ")
  if headerInput == 'y' or headerInput == '' :
    header = True
  else :
    header = False
  style = input("Style/Comments (Enter a number out of 30 to represent their grade, hit enter for 30): ")
  comments += input ("General Comments?:  ")
  if not style.isdigit() :
    style = 30
  else :
    style = int(style)
  
  #writing grade time!
  if late == -1:
    if writeToFile: outputFile.write('0\t More than 7 days late')
    print('Late more than 7 days!')
  else :
    if late == 3:
      comments = "3 - 7 days late, "
      grade -= 30
    elif late == 2 :
      comments = "2 days late, "
      grade -= 20
    elif late == 1 :
      comments = "1 day late, "
      grade -= 10
    
    if wrongFileName :
      comments += " wrong filename, "
      grade -= 10
    if not header :
      comments += " no/malformed header, "
      grade -= 10

    if writeToFile: outputFile.write(str(grade+style) + "\t"+comments.rstrip(', '))
      
  if writeToFile: outputFile.write('\n')
  os.chdir("..")
      
#returns the number of days late an assignment is
def isLate( splitted ):
  dueDate = datetime.strptime(dateString,"%m-%d-%Y %H:%M:%S")  
  lateOne = dueDate + timedelta(days=1) 
  lateTwo = lateOne + timedelta(days=1)
  lateSev = dueDate + timedelta(days=7)
  turninDate = datetime.strptime(splitted[5] + " " +( ("0" + splitted[6]) if len(splitted[6]) == 1 else splitted[6])+ " " + splitted[7] +" 2013", "%b %d %H:%M %Y")
  if turninDate <= dueDate :
    return 0
  elif turninDate <= lateOne :
    return 1
  elif turninDate <= lateTwo :
    return 2
  elif turninDate <= lateSev:
    return 3
  else :
    return -1

main()
