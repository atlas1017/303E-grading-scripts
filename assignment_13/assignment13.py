from os.path import os, exists
from datetime import datetime, timedelta
from functools import *
import math
import subprocess
import sys
import re
import difflib

pipes = {'stdout':subprocess.PIPE, 'stdin':subprocess.PIPE, 'stderr':subprocess.PIPE}

outputFilename = 'assignment13.txt'
outputFile = open(outputFilename, 'a')
filename = 'WordSearch.py'

# Each test worth 6 points
file_names = ('horizontal', 'vertical', 'backwards', 'non_square', 'not_found')
# Worth 10 bonus points
bonus_name = 'diagonal'

dateString = "11-15-2013 23:59:59"
dateString = "12-7-2013 23:59:59"

def main():
  out = subprocess.getoutput('ls ./')
  CSIDS = out.split("\n")
  if len(sys.argv) == 3:
    outputFile.write('CSID\tGrade\tComments\n')
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
      assign13( csid , True)
  #singleton mode
  else:
    csid = sys.argv[1]
    os.system('clear')
    print('======================')
    print(csid)
    print('======================')
    assign13( csid , False)
  outputFile.close()

def assign13(csid , writeToFile) :
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


  # copies ../FILE_TO_COPY.txt to ./hidden.txt and runs the program in ./
  # diffs ./found.txt with ../FILE_TO_COPY_found.txt
  perfect_formatting = True
  def cp_run_and_diff (file_to_copy):
    nonlocal perfect_formatting
    os.chdir ('..')
    subprocess.getoutput('rm %s/hidden.txt' % csid)
    subprocess.getoutput('rm %s/found.txt' % csid)
    os.system('cp %s.txt %s/hidden.txt' % (file_to_copy, csid))
    os.chdir(csid)
    subprocess.getoutput('python3 %s' % fileToGrade)
    if file_to_copy != bonus_name:
      print ("Testing %s:" % file_to_copy)
    success = True
    try:
      with open ('found.txt', 'r') as actual, open ('../%s_found.txt' % file_to_copy, 'r') as expected:
        actual_lines = [x.strip() for x in list(actual) if len(x.strip()) != 0]
        actual_lines.sort()
        expected_lines = [x.strip() for x in list(expected) if len(x.strip()) != 0]
        expected_lines.sort()
        if (len(actual_lines) != len(expected_lines)):
          success = False
          if (file_to_copy == file_names[0]):
            perfect_formatting = False
        else:
          last_line = None
          for expected_line, actual_line in zip(expected_lines, actual_lines):
            if not success:
              break
            if file_to_copy == file_names[0] and last_line is not None:
              perfect_formatting = perfect_formatting and len(last_line) == len(actual_line)
            last_line = actual_line
            success = expected_line.split() == actual_line.split()
        if True or not success and file_to_copy != bonus_name:
          print ('  Expected:')
          for line in expected_lines:
            print ('    |%s' % line)
          print ('  Actual:')
          for line in actual_lines:
            print ('    |%s' % line)
          print()
        elif success:
          if file_to_copy == bonus_name:
            print ("Testing '%s':" % file_to_copy)
          print ('Program output matches exactly!\n')
    except:
      if file_to_copy != bonus_name:
        print ("Program did not output to file.\n")
      if (file_to_copy == file_names[0]):
        perfect_formatting = False
      return False

    subprocess.getoutput('rm hidden.txt')
    subprocess.getoutput('rm found.txt')
    return success

  if late != -1:
    test_results = []
    for test in file_names:
      test_results.append (cp_run_and_diff (test))
    test_results.append (cp_run_and_diff (bonus_name))
    
    if test_results[-1]:
      print("Bonus: Diagonal searching implemented correctly! (+10)\n")
      comments.append("passed diagonal bonus (+10)")
      grade += 10
    if perfect_formatting:
      print("Bonus: formatting is perfect! (+5)\n")
      comments.append("passed formatting bonus (+5)")
      grade += 5
    if all(test_results[:-1]):
      print("Perfect! ^_^")
      comments.append("passed all tests")
    elif not any(test_results[:-1]):
      print("Failed every test... ='(")
      comments.append("failed all tests (-30)")
      grade -= 30
    else:
      first_fail = True
      def print_fail (string):
        nonlocal first_fail
        if first_fail:
          first_fail = False
          print(string)

      functionality_fail = "Tests failed (6 points each):"
      num_off = 0
      for i in range (len(test_results) - 1):
        if not test_results[i]:
          print_fail (functionality_fail)
          print("\t%s" % file_names[i])
          comments.append("failed %s (-6)" % file_names[i])
          num_off += 6
      grade -= num_off
      print("Total off: (-%d)" % num_off)

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
