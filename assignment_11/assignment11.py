from os.path import os, exists
from datetime import datetime, timedelta
from functools import *
import math
import subprocess
import sys
import re
import difflib
import time

pipes = {'stdout':subprocess.PIPE, 'stdin':subprocess.PIPE, 'stderr':subprocess.PIPE}

outputFilename = 'assignment11.txt'
outputFile = open(outputFilename, 'a')
inputFile = open('input.txt','r')
inputLines = inputFile.read().splitlines()
correctFile = open('correct.txt','r')
correctLines = correctFile.read().splitlines()
filename = "DNA.py"
dateString = "03-28-2014 23:59:59"

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
      assign11( csid , True)
  #singleton mode
  else:
    csid = sys.argv[1]
    os.system('clear')
    print('======================')
    print(csid)
    print('======================')
    assign11( csid , False)
  outputFile.close()
  inputFile.close()

def assign11(csid , writeToFile) :
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

  #grading time!
  '''
  tests 1-6 are 3 points
  7 and 8 are for multiple subsequences and are 4 points
  test 9 is to make sure they don't output singleton matches and is 3 points
  '''
  if late != -1:
    answers = []
    count = 0
    for strand1,strand2 in zip(inputLines[0::2],inputLines[1::2]):
      count += 1
      try:
        process = subprocess.Popen(['python3', fileToGrade], **pipes)
        out = process.communicate(bytes(strand1+'\n'+strand2+'\n', 'UTF-8'))[0]
        answers.append(str(out)[2:-1].replace('\\n','\n').strip())
      except KeyboardInterrupt:
        print(" on test" +str(count))

    correct_formatting = True
    extra_credit = True
    num_3_points_tests_failed = 0
    num_4_points_tests_failed = 0

    # gradin' normal tests 
    correct = ""
    count = 0
    for normal_out,extra_credit_out,out in zip(correctLines[0::2],correctLines[1::2],answers[:10]):
      printed = False
      correct_formatting = True
      count += 1
      normal_out = normal_out.replace('\\n','\n')
      print("\n=====Test "+str(count)+"=====")
      extra_credit_out = extra_credit_out.replace('\\n','\n')
      # there was some ambiguity on if the no sequence found text had a period or not
      out = out.replace('.','')
      if extra_credit and out != extra_credit_out:
        extra_credit = False
      if not extra_credit and correct_formatting and out != normal_out :
        print("\tIncorrect Formatting -5")
        print("\t=====Correct=====\n"+normal_out+"\n\t=====Output=====\n"+out)
        if input("Hit enter to accept deduction, or type n: ") == "":
          printed = True
          correct_formatting = False

      #check correctness
      #if there's a perfect match no need to fuzzy match
      if not correct_formatting:
        failed = False
        splitted = set(out.split(':')[-1].split('\n')[1:])
        correct_splitted = normal_out.split('\n')
        if count <= 6:
          if splitted != set(correct_splitted[-1:]):
            num_3_points_tests_failed += 1
            failed = True
            points = "3"
        elif count == 7:
          if splitted != set(correct_splitted[-2:]):
            num_4_points_tests_failed += 1
            failed = True
            points = "4"
        elif count == 8:
          if splitted != set(correct_splitted[-3:]):
            num_4_points_tests_failed += 1
            failed = True
            points = "4"
        elif count == 9:
          if splitted != set(correct_splitted[-1:]):
            num_3_points_tests_failed += 1
            failed = True
            points = "3"
        if failed:
          if not printed:
            print("\t=====Correct=====\n"+normal_out+"\n\t=====Output=====\n"+out)
          print("\tFailed Test -"+points)
        else:
          print("\tPassed")
      else:
        print("\tPassed")

    #calculating grade time
    total_off = 0
    total_off -= num_3_points_tests_failed * 3
    total_off -= num_4_points_tests_failed * 4
    print()
    feedback = "3 point tests passed: "+str(7-num_3_points_tests_failed)+"/7 so " + str(num_3_points_tests_failed*-3)
    comments.append(feedback)
    print(feedback)
    feedback = "4 point tests passed: "+str(2-num_4_points_tests_failed)+"/2 so " + str(num_4_points_tests_failed*-4)
    comments.append(feedback)
    print(feedback)

    if not correct_formatting:
      total_off -= 5
      feedback = "Incorrect formatting: -5"
      comments.append(feedback)
      print(feedback)
    if extra_credit:
      total_off +=3
      feedback = "Extra credit formatting: +3"
      comments.append(feedback)
      print(feedback)
    grade += total_off
    print("Grade: "+str(grade)+"/70")
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
  turninDate = datetime.strptime(splitted[5] + " " +( ("0" + splitted[6]) if len(splitted[6]) == 1 else splitted[6])+ " " + splitted[7] +" 2014", "%b %d %H:%M %Y")
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
