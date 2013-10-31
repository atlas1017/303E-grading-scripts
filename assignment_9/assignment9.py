from os.path import os, exists
from datetime import datetime, timedelta
from functools import *
import subprocess
import sys
import re
import difflib

correct = open('correct.txt', 'r').read().strip().split("\n")
outputFilename = 'assignment9.txt'
outputFile = open(outputFilename, 'w+')
outputFile.write('CSID\tGrade\tComments\n')
filename = "Goldbach.py"
dateString = "10-22-2013 23:00:00"
inputArray = open('input.txt','r').read().strip().split("\n")

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
      assign9( csid , True)
  #singleton mode
  else:
    csid = sys.argv[1]
    os.system('clear')
    print('======================')
    print(csid)
    print('======================')
    assign9( csid , False)
  outputFile.close()

def assign9( csid , writeToFile) :
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
  perfectScore = 0
  closeScore = 0
  wrongScore = 0
  if not fileToGrade == "" and late != -1:
    questionCount = 0
    maxScore = 0
    for x in range(len(inputArray)):
      questionCount += 1
      process = subprocess.Popen(['python3', fileToGrade], stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
      try:
        out = process.communicate(bytes('\n'.join(inputArray[x].split()), 'UTF-8'))[0]
      except KeyboardInterrupt:
        pass
      answerValues = str(out)[2:].replace('\\n','\n').strip()
      answerValues = answerValues.replace('\n \n','\n') # get rid of blank lines with an extra space
      answerValues = answerValues.replace('\n\n','\n') # get rid of standard blank lines
      answerValues = answerValues.replace('limit: \nEnter','limit: Enter') # make sure all input lines are joined together
      answerValues = answerValues.replace('limit:\nEnter','limit: Enter') # make sure all input lines are joined together
      print(answerValues)
      # if some of the numeric output is on the same line as the input elements, split them apart
      needNewLine = re.search('(limit: )([1-9])', answerValues)
      while needNewLine:
        answerValues = answerValues.replace(needNewLine.group(1) + needNewLine.group(2), needNewLine.group(1) + "\n" + needNewLine.group(2))
        needNewLine = re.search('(limit: )([1-9])', answerValues)
      answerValues = answerValues.split('\n')
      for temp in range(len(answerValues)):
        answerValues[temp] = answerValues[temp].strip()
      emptyLines = answerValues.count('')
      for temp in range(emptyLines):
        answerValues.remove('')

      inputValues = inputArray[x].split()
      for inputSet in range(round(len(inputValues)/2)):
        lowerLimit = int(inputValues[inputSet * 2])
        upperLimit = int(inputValues[inputSet * 2 + 1])

      scoreValue = 5
      maxScore += scoreValue
      perfectInputRequest = True
      correctValue = getNextCorrectLine(correct)
      answerValue = getAnswerValue(answerValues, 0)
      if answerValue == correctValue:
        print('Perfect input prompts for #' + str(questionCount))
        perfectScore += scoreValue
      else:
        perfectInputRequest = False
        if closeStrings(answerValue, correctValue):
          print('Close input prompts for #' + str(questionCount))
          closeScore += scoreValue
        else:
          print('Wrong input prompts for #' + str(questionCount))
          wrongScore += scoreValue
        print("\tPerfect: '" + correctValue + "'\n\tActual:  '" + answerValue + "'")

      scoreValue = 15
      maxScore += scoreValue
      totalAnswers = round((upperLimit - lowerLimit)/2 + 2)
      perfectData = True
      closeCount = 0
      wrongCount = 0
      for answerCount in range(1, totalAnswers):
        correctValue = getNextCorrectLine(correct)
        answerValue = getAnswerValue(answerValues, answerCount)
        if answerValue != correctValue:
          perfectData = False
          if closeStrings(answerValue, correctValue):
            print('Close data output for #' + str(questionCount) + ", line " + str(answerCount))
            closeCount += 1
          else:
            print('Wrong data output for #' + str(questionCount) + ", line " + str(answerCount))
            wrongCount += 1
          print("\tPerfect: '" + correctValue + "'\n\tActual:  '" + answerValue + "'")
      if perfectData == True:
        print('Perfect data output for #' + str(questionCount))
        perfectScore += scoreValue
      else:
        if closeCount > wrongCount:
          closeScore += scoreValue
        else:
          wrongScore += scoreValue

      scoreValue = 5
      maxScore += scoreValue
      perfectMaximum = True
      correctValue = getNextCorrectLine(correct)
      answerValue = getAnswerValue(answerValues, totalAnswers)
      # Do some synchronization here, in the case the data answer got out of sync
      while (correctValue[:11] != 'The maximum' and correctValue != ''):
        correctValue = getNextCorrectLine(correct)
      while (answerValue[:11] != 'The maximum' and answerValue != ''):
        totalAnswers += 1
        answerValue = getAnswerValue(answerValues, totalAnswers)
      if answerValue != correctValue:
        perfectMaximum = False
        if closeStrings(answerValue, correctValue):
          print('Close maximum output for #' + str(questionCount))
          closeScore += scoreValue
        else:
          print('Wrong maximum output for #' + str(questionCount))
          wrongScore += scoreValue
        print("\tPerfect: '" + correctValue + "'\n\tActual:  '" + answerValue + "'")
      else:
        print('Perfect maximum output for #' + str(questionCount))
        perfectScore += scoreValue

    print("Perfect: " + str(perfectScore) + "/" + str(maxScore))
    print("Close:   " + str(closeScore) + "/" + str(maxScore))
    print("Wrong:   " + str(wrongScore) + "/" + str(maxScore))
    if wrongScore != 0 or closeScore != 0:
      comments += "Output did not match the instructor's  P: "+str(perfectScore)+"  C: "+str(closeScore)+"  W: "+str(wrongScore)+ ", "

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

def closeStrings(string1, string2):
  return ("".join(string1.split()) == "".join(string2.split()))

def getAnswerValue(answerValues, answerNumber):
  if answerNumber < len(answerValues):
    return answerValues[answerNumber]
  return ''

def getNextCorrectLine(correct):
  if getNextCorrectLine.lineCounter < len(correct):
    getNextCorrectLine.lineCounter += 1
    return correct[getNextCorrectLine.lineCounter - 1]
  return ''
getNextCorrectLine.lineCounter = 0
      
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
