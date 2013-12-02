from os.path import os, exists
from datetime import datetime, timedelta
from functools import *
import math
import subprocess
import sys
import re
import difflib

pipes = {'stdout':subprocess.PIPE, 'stdin':subprocess.PIPE, 'stderr':subprocess.PIPE}

outputFilename = 'assignment12.txt'
outputFile = open(outputFilename, 'a')
filename = "ISBN.py"
input_file = 'isbn.txt' 
output_file = 'isbnOut.txt'
testCases = 10
dateString = "11-11-2013 23:59:59"

def main():
  out = subprocess.getoutput('ls ./')
  CSIDS = out.split("\n")
  if len(sys.argv) == 3:
    outputFile.write('\nCSID\tGrade\tComments\n')
    lowerBound = sys.argv[1]
    upperBound = sys.argv[2] + '~';
    myList = []
    count = 0
    for item in CSIDS:
      if lowerBound <= item <= upperBound:
        if "." not in item :
          myList.append( item )
    for csid in myList :
      count += 1
      os.system('clear')
      print('======================')
      print(csid + " " + str(count) + " out of " + str(len(myList)))
      print('======================')
      assign12( csid , True)
  #singleton mode
  else:
    csid = sys.argv[1]
    os.system('clear')
    print('======================')
    print(csid)
    print('======================')
    assign12( csid , False)
  outputFile.close()

def assign12(csid , writeToFile) :
  fileToGrade = ""
  late = 0
  grade = 70
  style = 30
  wrongFileName = False
  header = True
  comments = []

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

  # run student's isbn.py and compare their output with standard output
  def run_program_compare():
    os.chdir('..')
    os.system('cp %s %s/isbn.txt' % (input_file, csid))
    os.chdir(csid)
    command = 'python3 ' + fileToGrade
    os.system( command )
    wrongCases = testCases
    count = 1
    try:
      user_file = open(output_file, 'r')
      user_line = user_file.readline()
      std_file = open('../%s' % output_file, 'r')
      std_line = std_file.readline()
      
      while (std_line and user_line ):
        print ("test case", count)
        print ("Expected: ", std_line, end='')
        print ("Actual:   ", user_line)
        count += 1
        if std_line.lower().split() == user_line.lower().split():
          wrongCases -= 1
        elif std_line.lower().split()[1] in user_line.lower().split():
          wrongCases -= 0.5
        user_line = user_file.readline()
        std_line = std_file.readline()

      while(std_line):
          print ("test case", count)
          print ("Expected: ", std_line, end='')
          print ("Actual:   ")
          user_line = user_line.readline()
          count += 1
      while(user_line):
          wrongCases += 1
          print ("Expected: ", end='')
          print ("Actual:   ", user_line)
          user_line = user_line.readline()
    except:
      pass
    if wrongCases <= testCases: return wrongCases
    else: return testCases

  if late != -1:
    wrongTests = run_program_compare()
    print ("correct: ", testCases - wrongTests)
    print ("wrong:   ", wrongTests)
    if wrongTests == 0:
      print("Excellent! passed all tests")
      comments.append("passed all tests")
    else:
      grade = grade - (30/testCases) * wrongTests
      c = str(wrongTests) + " are wrong"
      comments.append(c)

  #checking for header and style
  #os.system('vim ' + fileToGrade)
  input("Hit Enter to cat")
  print(subprocess.getoutput('cat ' + fileToGrade))
  headerInput = input("Header and comments? (y/n, hit enter for y): ")
  if headerInput == 'y' or headerInput == '' :
    header = True
  else :
    header = False
  style = input("Style/Other (Out of 30, hit enter for 30): ")
  gen_comments = input("General Comments?: ").rstrip().lstrip()
  gen_comments = gen_comments if len(gen_comments) is not 0 else "style"
  if not style.isdigit():
    style = 30
  else :
    style = int(style)
  if (gen_comments != "style" or style != 30):
    gen_comments += " (%+d)" % (style - 30)
    comments.append("%s" % gen_comments)
  
  #writing grade time!
  if late == -1:
    if writeToFile: outputFile.write('0\t More than 7 days late')
    print('Late more than 7 days!')
  else :
    if late == 3:
      comments.append("3 - 7 days late (-30)")
      grade -= 30
    elif late == 2 :
      comments.append("2 days late (-20)")
      grade -= 20
    elif late == 1 :
      comments.append("1 day late (-10)")
      grade -= 10
    
    if wrongFileName :
      comments.append("wrong filename (-10)")
      grade -= 10
    if not header :
      comments.append("missing comments or malformed header (-10)")
      grade -= 10

    if writeToFile: outputFile.write(str(grade+style) + "\t" + ', '.join(comments))
      
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
