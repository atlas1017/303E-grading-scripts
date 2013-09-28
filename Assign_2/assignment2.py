from os.path import os, exists
from datetime import datetime, timedelta
import subprocess
import sys
import re
import difflib

outputFile = open('assignment2.txt', 'w')
correct = open('correct.txt', 'r').read()
filename = "CreditCard.py"
dateString = "09-23-2013 23:00:00"
outputFile.write('CSID\tGrade\tComments\n')
inputArray = open('numbers.txt','r').read().split()

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
      assign2( csid , True)
  #singleton mode
  else:
    csid = sys.argv[1]
    os.system('clear')
    print('======================')
    print(csid)
    print('======================')
    assign2( csid , False)
  outputFile.close()

def assign2( csid , writeToFile) :
  fileToGrade = ""
  late = 0
  linesWrong = 0
  grade = 70
  style = 30
  wrongFileName = False
  header = True
  comments = " "
  manualComments = ""

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
      if writeToFile: outputFile.write("0\tno file")
    else :
      splitted = subprocess.getoutput('ls -l ' + fileToGrade.replace(' ','\ ')).split()
      late = isLate(splitted)
      wrongFileName = True

  #grading time!
  if not fileToGrade == "" and late < 3:
    answers = []
    for creditCardNumber in inputArray:
      process = subprocess.Popen(['python3', fileToGrade], stdin = subprocess.PIPE, stdout = subprocess.PIPE)
      out = process.communicate(bytes(creditCardNumber, 'UTF-8'))[0]
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
        if correctAnswer.lower()[0:5] in answers[answerCount].lower() and not "in" + correctAnswer.lower()[0:5] in answers[answerCount].lower(): #We can change to to account for invalid or not
          print ("Correct answer for #", answerCount+1," but incorrect formatting")
          print ("\t", correctAnswer[0:1],"-",answers[answerCount])
          closeCount += 1
        else:
          print("Wrong answer")
          wrongCount += 1
      answerCount += 1
    print("Perfect:", str(perfectCount) + "/8")
    print("Close:", str(closeCount) + "/8")
    print("Wrong:", str(wrongCount) + "/8")
    if(0 >= closeCount >= 4):
    	grade = 70 - (4 * wrongCount) 
    	comment = " Output did not match instructors "
    elif(closeCount >= 4):
    	grade = 60 - (4 * wrongCount)
    	comment = " Output did not match instructors "

      #TODO take of 5 points if they're closeCount is 0 to 4 and take off 10 if closeCount is greater than 4
      #TODO take off 4 * wrongCount points as well
      #TODO fix the else below to output the correct comments
     
  else:
    #print('Their output:')
    #print(out)
    #print('Correct output:')
    #print(correct)
    #print('logo has ' + str(len(lines)) +' lines, not 19')
    #don't dock points for lateness or wrong filename here
    gradeInput = input("Grade out of 70 (no style, hit enter if 65): ")
    if gradeInput == '' :
      grade = 65
    else :
      grade = int(gradeInput)
    manualComments = input("Comments: ")

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
  comment += input ("General Comments?:  ")
  if not style.isdigit() :
    style = 30
  else :
    style = int(style)
  
  #writing grade time!
  if late == 3 :
    if writeToFile: outputFile.write('0\t 3 days late')
  else :
    if late == 2 :
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

    if linesWrong > 0 and linesWrong < 3 : 
      comments += "improperly formed superman logo, "
      grade -= 5
    elif linesWrong > 3 :
      comments += "nonsensical superman logo, "
      grade -= 5
    if writeToFile: outputFile.write(str(grade+style) + "\t"+comments.rstrip(', ') + manualComments)
      
  if writeToFile: outputFile.write('\n')
  os.chdir("..")
      
#returns the number of days late an assignment is
def isLate( splitted ):
  dueDate = datetime.strptime(dateString,"%m-%d-%Y %H:%M:%S")  
  lateOne = dueDate + timedelta(days=1) 
  lateTwo = lateOne + timedelta(days=1)
  turninDate = datetime.strptime(splitted[5] + " " +( ("0" + splitted[6]) if len(splitted[6]) == 1 else splitted[6])+ " " + splitted[7] +" 2013", "%b %d %H:%M %Y")
  if turninDate <= dueDate :
    return 0
  elif turninDate <= lateOne :
    return 1
  elif turninDate <= lateTwo :
    return 2
  else :
    return 3

main()
