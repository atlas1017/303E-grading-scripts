from os.path import os, exists
from datetime import datetime, timedelta
import subprocess
import sys
import re
import difflib

correct = open('correct.txt', 'r').read()
outputFilename = 'assignment4.txt'
outputFile = open(outputFilename, 'w+')
outputFile.write('CSID\tGrade\tComments\n')
filename = "Day.py"
dateString = "02-17-2014 23:00:00"
inputArray = open('input.txt','r').read().split()

def main():
  out = subprocess.getoutput('ls ./')
  CSIDS = out.split("\n")
  if len(sys.argv) == 3:
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
      assign4( csid , True)
  #singleton mode
  else:
    csid = sys.argv[1]
    os.system('clear')
    print('======================')
    print(csid)
    print('======================')
    assign4( csid , False)
  outputFile.close()

def assign4( csid , writeToFile) :
  fileToGrade = ""
  late = 0
  grade = 70
  style = 30
  wrongFileName = False
  header = 'y'
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
  if not fileToGrade == "":
    answers = []
    for x in range(0,len(inputArray),3):
      process = subprocess.Popen(['python3', fileToGrade], stdin = subprocess.PIPE, stdout = subprocess.PIPE)
      out = process.communicate(bytes(inputArray[x] + '\n' + inputArray[x+1] + '\n' + inputArray[x+2], 'UTF-8'))[0]
      answers.append(str(out)[2:-1])
     
    perfectCount = 0
    closeCount = 0 
    answerCount = 0
    wrongCount = 0
    for correctAnswer in correct.splitlines():
      if correctAnswer in answers[answerCount]:  #Does not contain the correct formatted answer
        print('Correct answer for #', answerCount+1)
        perfectCount += 1
      else:
        correctSplitted = correctAnswer.split()
        if  correctSplitted[-1][:-1].lower() in answers[answerCount].lower() :
          print ("Correct answer for #", answerCount+1," but incorrect formatting")
          print ("\t", correctAnswer," vs. ",answers[answerCount])
          closeCount += 1
        else:
          print("Wrong answer")
          print ("\t", correctAnswer," vs. ",answers[answerCount])
          wrongCount += 1
      answerCount += 1
    print("Perfect:", str(perfectCount) + "/10")
    print("Close:", str(closeCount) + "/10")
    print("Wrong:", str(wrongCount) + "/10")
    if wrongCount != 0 or closeCount != 0:
        grade -= (2 * wrongCount) 
        grade -= (1 * closeCount)
        comments += " Output did not match instructor's. "


  #checking for header and style
  #os.system('vim ' + fileToGrade)
  input("Hit Enter to cat")
  print(subprocess.getoutput('cat ' + fileToGrade))
  headerInput = input("Header( (y or enter)  /  n / d (if problem with desription) )? ")
  header = 'y' if headerInput == '' else headerInput
  style = input("Style/Comments (Enter a number out of 30 to represent their grade, hit enter for 30): ")
  comments += input ("General Comments?:  ")
  if not style.isdigit() :
    style = 30
  else :
    style = int(style)
  
  #writing grade time!
  if late == -1:
    if writeToFile: outputFile.write('0\t More than 7 days late')
  else :
    if late == 3:
      comments += " 3 - 7 days late."
      grade -= 30
    elif late == 2 :
      comments += " 2 days late."
      grade -= 20
    elif late == 1 :
      comments += " 1 day late."
      grade -= 10
    
    if wrongFileName :
      comments += " Wrong filename. "
      grade -= 10
    if header  == 'n':
      comments += " You need a header at the top of your code. "
      grade -= 10
    elif header  == 'd':
      comments += " The description in your header should briefly explain what the program does. "
      grade -= 2

    if writeToFile: outputFile.write(str(grade+style) + "\t"+comments)
      
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
