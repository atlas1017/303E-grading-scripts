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

outputFilename = 'assignment14.txt'
outputFile = open(outputFilename, 'a')
filename = "GuessingGame.py"
dateString = "11-20-2013 23:59:59"

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
      assign14( csid , True)
  #singleton mode
  else:
    csid = sys.argv[1]
    os.system('clear')
    print('======================')
    print(csid)
    print('======================')
    assign14( csid , False)
  outputFile.close()
  inputFile.close()

def assign14(csid , writeToFile) :
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
  5 total test cases
  2 normal test each 5 points
    all 1's
    alternating 1 -1
  3 others
  test that it handles n correctly, 5 points
  test if inputting weird guesses is handled correctly, 5 points
  test that it handles 7 no's correctly, 5 points

  general formatting 5 points
  total of 30 points
  '''
  initialPrompt = "Guessing Game\n\nThink of a number between 1 and 100 inclusive.\nAnd I will guess what it is in 7 tries or less.\n\nAre you ready? (y/n): "
  prompt = "Enter 1 if my guess was high, -1 if low, and 0 if correct: "
  goodResponse = "Thank you for playing the Guessing Game."
  badResponse = "Either you guessed a number out of range or you had an incorrect entry."

  testCases = [
    'y\n1\n1\n1\n1\n1\n0',
    'y\n1\n-1\n1\n-1\n1\n-1\n0',
    'n\n',
    'y\nBAD INPUT\nBAD INPUT\n0\n',
    'y\n1\n-1\n1\n-1\n1\n-1\n1'
  ]
  correctOutput = [
    initialPrompt + '\nGuess  1 :  The number you thought was 50\nEnter 1 if my guess was high, -1 if low, and 0 if correct: \nGuess  2 :  The number you thought was 25\nEnter 1 if my guess was high, -1 if low, and 0 if correct: \nGuess  3 :  The number you thought was 12\nEnter 1 if my guess was high, -1 if low, and 0 if correct: \nGuess  4 :  The number you thought was 6\nEnter 1 if my guess was high, -1 if low, and 0 if correct: \nGuess  5 :  The number you thought was 3\nEnter 1 if my guess was high, -1 if low, and 0 if correct: \nGuess  6 :  The number you thought was 1\nEnter 1 if my guess was high, -1 if low, and 0 if correct: \n'+ goodResponse,
    initialPrompt + '\nGuess  1 :  The number you thought was 50\nEnter 1 if my guess was high, -1 if low, and 0 if correct: \nGuess  2 :  The number you thought was 25\nEnter 1 if my guess was high, -1 if low, and 0 if correct: \nGuess  3 :  The number you thought was 37\nEnter 1 if my guess was high, -1 if low, and 0 if correct: \nGuess  4 :  The number you thought was 31\nEnter 1 if my guess was high, -1 if low, and 0 if correct: \nGuess  5 :  The number you thought was 34\nEnter 1 if my guess was high, -1 if low, and 0 if correct: \nGuess  6 :  The number you thought was 32\nEnter 1 if my guess was high, -1 if low, and 0 if correct: \nGuess  7 :  The number you thought was 33\nEnter 1 if my guess was high, -1 if low, and 0 if correct: \n'+goodResponse,
    initialPrompt + '\nBye',
    initialPrompt + '\nGuess  1 :  The number you thought was 50\nEnter 1 if my guess was high, -1 if low, and 0 if correct: \nEnter 1 if my guess was high, -1 if low, and 0 if correct: \nEnter 1 if my guess was high, -1 if low, and 0 if correct: \n' + goodResponse,
    initialPrompt + '\nGuess  1 :  The number you thought was 50\nEnter 1 if my guess was high, -1 if low, and 0 if correct: \nGuess  2 :  The number you thought was 25\nEnter 1 if my guess was high, -1 if low, and 0 if correct: \nGuess  3 :  The number you thought was 37\nEnter 1 if my guess was high, -1 if low, and 0 if correct: \nGuess  4 :  The number you thought was 31\nEnter 1 if my guess was high, -1 if low, and 0 if correct: \nGuess  5 :  The number you thought was 34\nEnter 1 if my guess was high, -1 if low, and 0 if correct: \nGuess  6 :  The number you thought was 32\nEnter 1 if my guess was high, -1 if low, and 0 if correct: \nGuess  7 :  The number you thought was 33\nEnter 1 if my guess was high, -1 if low, and 0 if correct: \n'+badResponse
  ]
  if late != -1:
    answers = []
    count = 0
    for test in testCases:
      count += 1
      try:
        process = subprocess.Popen(['python3', fileToGrade], **pipes)
        out = process.communicate(bytes(test, 'UTF-8'))[0]
        answers.append(str(out)[2:-1].replace('\\n','\n').strip())
      except KeyboardInterrupt:
        print(" on test" +str(count))

    correct_formatting = True

    # gradin' normal tests 
    correct = ""
    count = 0
    numFailed = 0
    for correct,out in zip(correctOutput,answers):
      printed = False
      count += 1
      print("=====Test "+str(count)+"=====")
      #check formatting
      if out != correct and correct_formatting:
        print("\tIncorrect Formatting -5")
        print("\t=====Correct=====\n\t"+'\n\t'.join(correct.split('\n'))+"\n\t=====Output=====\n\t"+'\n\t'.join(out.split('\n')))
        printed = True
        correct_formatting = False

      #check correctness
      #if there's a perfect match no need to fuzzy match
      if not correct_formatting:
        failed = False
        theirNums = [int(s) for s in out.split() if s.isdigit()]
        ourNums = [int(s) for s in correct.split() if s.isdigit()]

        if count == 3:
          if "bye" not in out.lower(): 
            failed = True
        elif count == 5:
          if badResponse.lower()[:-1] not in out.lower(): 
            failed = True
        elif set(theirNums) != set(ourNums):
          failed = True

        if failed:
          comments.append("Failed test " + str(count) + " (-5)")
          numFailed += 1
          if not printed:
            print("\tFailed test "+str(count) + ": -5")
            print("\t=====Correct=====\n\t"+'\n\t'.join(correct.split('\n'))+"\n\t=====Output=====\n\t"+'\n\t'.join(out.split('\n')))
        else:
          print("\tPassed")
      else:
        print("\tPassed")

    #take off for test that we had to ^C
    if len(answers) < 5:
      numFailed += 5 - len(answers)

    #calculating grade time
    total_off = (numFailed * -5)
    print()
    print("Failed " + str(numFailed))

    if not correct_formatting:
      total_off -= 5
      feedback = "Incorrect formatting: -5"
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
