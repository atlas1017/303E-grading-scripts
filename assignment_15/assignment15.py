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

outputFilename = 'assignment15.txt'
outputFile = open(outputFilename, 'a')
filename = "Benford.py"
dateString = "12-02-2013 23:59:59"

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
      assign15( csid , True)
  #singleton mode
  else:
    csid = sys.argv[1]
    os.system('clear')
    print('======================')
    print(csid)
    print('======================')
    assign15( csid , False)
  outputFile.close()
  inputFile.close()

def assign15(csid , writeToFile) :
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
  20 points for correctness
  -5 if there's not 1 number past the decimal point
  '''
  if late != -1:
    #copy over input file
    os.system('cp ../Census_2009.txt .')
    try:
      process = subprocess.Popen(['python3', fileToGrade], **pipes)
      out = process.communicate(bytes('', 'UTF-8'))[0]
      answerList = str(out)[2:-1].replace('\\t',' ').strip().split('\\n')
    except KeyboardInterrupt:
      print(" on test" +str(count))

    correct_formatting = True
    correct_output = True

    f = open('../correct.txt', 'r')
    correctList = f.read()
    f.close()

    correct = []
    for x in correctList.split('\n'):
      correct.append(x.split(' '))
    answer = []
    for x in answerList:
      if x.strip(): #empty string is false
        answer.append(x.split())

    #check correctness
    if len(correct) == len(answer):
      count = 0
      for right,theirs in zip(correct,answer):
        count+=1
        if count == 1:
          continue
        for rightElem, theirsElem in zip(right,theirs):
          if rightElem != theirsElem and (rightElem not in theirsElem and theirsElem not in rightElem):
            try:
              rightFloat = eval(rightElem)
              theirsFloat = eval(theirsElem)
            except Exception:
              rightFloat = ""
              theirsFloat = ""
            #SOOOOO MUCH COPY PASTA!!!! DON'T EVEN CAR IT WORKS!!!
            #YES CAR!!!!
            if type(rightFloat) == type(0.0) and type(theirsFloat) == type(0.0):
              if rightFloat == round(theirsFloat,1):
                correct_formatting = False
                print('Mismatch!')
                print('===Correct===')
                print(rightElem)
                print('===Theirs===')
                print(theirsElem)
              else:                
                print('Mismatch!')
                print('===Correct===')
                print(rightElem)
                print('===Theirs===')
                print(theirsElem)
                correct_output = False
            else:                
              print('Mismatch!')
              print('===Correct===')
              print(rightElem)
              print('===Theirs===')
              print(theirsElem)
              correct_output = False
    else:
      correct_output = False
      print("Lengths didn't match up?!?")
      print('===Correct===')
      for x in correct:
        print(x)
      print('===Theirs===')
      for x in answer:
        print(x)

    if not correct_output:
      print('===Correct===')
      for x in correct:
        print(x)
      print('===Theirs===')
      for x in answer:
        print(x)


    #calculating grade time
    total_off = 0
    if not correct_output:
      total_off -=20
      #Yup, kc.
      feedbakc = "Failed: -20 =("
      comments.append(feedbakc)
      print(feedbakc)
    if not correct_formatting:
      total_off -= 5
      feedback = "Incorrect formatting: -5"
      comments.append(feedback)
      print(feedback)
    grade += total_off
    if total_off == 0:
      print("<('.')^ Perfect ^('.')>")
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