from os.path import os, exists
from datetime import datetime, timedelta
from functools import *
import math
import subprocess
import sys
import re
import difflib

outputFilename = 'assignment8.txt'
outputFile = open(outputFilename, 'a')
averageNumRuns = 5
filename = "CalculatePI.py"
dateString = "10-18-2013 23:00:00"

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
      assign8( csid , True)
  #singleton mode
  else:
    csid = sys.argv[1]
    os.system('clear')
    print('======================')
    print(csid)
    print('======================')
    assign8( csid , False)
  outputFile.close()

def assign8( csid , writeToFile) :
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
    correct_format_left = True
    correct_format_mid = True
    correct_format_right = True
    correct_format_other = True
    valid_output = True
    calculated_values = []

    # perfect match
    first_line = "Computation of PI using Random Numbers"
    last_line = "Difference = Calculated PI - math.pi"
    regex_perfect = "^num = 100[0 ]{5}   Calculated PI = \d\.\d{6}   Difference = [+-]\d\.\d{6}$"
    regex_left = "100[\d\s]{5}"
    regex_mid = "=\s*(\d\.\d{6})\D+"
    regex_right = "[+-]\d\.\d{6}$"


    # grab pi and difference
    regex_grab = "[+-]?\d+(?:\.\d+(?:e[+-]?\d*)?)?"

    for run_num in range(averageNumRuns):
      process = subprocess.Popen(['python3', fileToGrade], stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
      try:
        out = process.communicate(bytes('50000', 'UTF-8'))[0]
      except KeyboardInterrupt:
        pass
      answer = list(filter(lambda line: len(line.rstrip()) is not 0, str(out)[2:-1].replace('\\n', '\n').rstrip().lstrip().split('\n')))
      print('\n'.join(answer))

      # grab the difference
      raw_grabbed = list(filter(lambda match: len(match) > 0, [re.findall(regex_grab, line) for line in answer]))
      grabbed_pi = [float(pi) for (_, pi, _) in raw_grabbed]
      grabbed_diff = [float(diff) for (_, _, diff) in raw_grabbed]
      calculated_values.append(grabbed_diff)

      # perfect matching
      correct_format_other = correct_format_other and first_line in answer and last_line in answer and len(answer) is 8
      try:
        perfect_matches = list(filter(lambda match: match is not None, [re.search(regex_perfect, line) for line in answer]))
        correct_format_other = correct_format_other and len(perfect_matches) is 6
      except:
        correct_format_other = False
      try:
        left_matches = list(filter(lambda match: match is not None, [re.search(regex_left, line) for line in answer]))
        correct_format_left = correct_format_left and len(left_matches) is 6
      except:
        correct_format_left = False
      try:
        mid_matches = list(filter(lambda match: match is not None, [re.search(regex_mid, line) for line in answer]))
        correct_format_mid = correct_format_mid and len(mid_matches) is 6
      except:
        correct_format_mid = False
      try:
        right_matches = list(filter(lambda match: match is not None, [re.search(regex_right, line) for line in answer]))
        correct_format_right = correct_format_right and len(right_matches) is 6
      except:
        correct_format_right = False

      # 0. verify decreasing error as n increases
      # 1. verify avg_diff + avg_pi is very close to math.pi
      # stops if either the current run or the average runs pass condition 0
      # and if condition 1 passes
      averages = list(map(lambda tup: sum(tup) / len(tup), zip(*[[math.fabs(x) for x in run] for run in calculated_values])))
      print("This Run: %s" % ', '.join(['%.6f' % math.fabs(x) for x in grabbed_diff]))
      print("All Runs: %s\n" % ', '.join(map(lambda i: '%.6f' % i, averages)))
      valid_output = valid_output and all([(math.fabs(calc - math.pi - diff) < 0.0001) for calc, diff in zip(grabbed_pi, grabbed_diff)])
      if all(x >= y for x,y in zip(averages, averages[1:])) or all(math.fabs(x) >= math.fabs(y) for x,y in zip(grabbed_diff, grabbed_diff[1:])):
        break

    if correct_format_left and correct_format_mid and correct_format_right and correct_format_other and valid_output:
      print("Perfect! ^_^")
    else:
      if not correct_format_left:
        print("num not left justified")
        comments += ", num not left justified"
        grade -= 6
      if not correct_format_mid:
        print("pi not expressed to six decimals")
        comments += ", pi not expressed to six decimals"
        grade -= 6
      if not correct_format_right:
        print("diff not expressed to six decimals or without sign")
        comments += ", diff not expressed to six decimals or without sign"
        grade -= 8
      if not correct_format_other:
        print("spacing or other general misformatting output")
        comments += ", spacing or other general misformatting output"
        grade -= 5
      if not valid_output:
        print("outputs do not add up")
        comments += ", outputs do not add up"
        grade -= 5

  #checking for header and style
  #os.system('vim ' + fileToGrade)
  input("Hit Enter to cat")
  print(subprocess.getoutput('cat ' + fileToGrade))
  headerInput = input("Header( (y or enter)  /  n)? ")
  if headerInput == 'y' or headerInput == '' :
    header = True
  else :
    header = False
  style = input("Style/Other (Out of 30, hit enter for 30): ")
  comments += ", %s" % input("General Comments?: ")
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
