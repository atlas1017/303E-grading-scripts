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
      if writeToFile: 
        outputFile.write("0\tno file\n")
        os.chdir("..")
        return
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
    wrongCount = 0
    VISA_answers = [0, 1, 2, 3]
    MasterCard_answers = [4, 5]
    correct_VISA_count = 0
    correct_MasterCard_count = 0
    # Used to ensure the inverse of the right answer is not also in the output.
    inverse = {'Valid credit card number': 'Invalid credit card number',
               'Invalid credit card number': 'Valid credit card number'}
    correct_answers = correct.splitlines()
    for answerCount, correctAnswer in enumerate(correct_answers):
      answer = answers[answerCount]
      # Contains the correct formatted answer.
      if correctAnswer in answer and not inverse[correctAnswer] in answer:  
        print('Correct answer for #', answerCount+1)
        perfectCount += 1
        # If the card number is a VISA, check if they did extra credit.
        if answerCount in VISA_answers and '\\nVISA' in answer:
            correct_VISA_count += 1
        # If the card number is a MasterCard, check if they did extra credit.
        if answerCount in MasterCard_answers and '\\nMasterCard' in answer:
            correct_MasterCard_count += 1
      # Contains right answer, but not correctly formatted.
      elif correctAnswer.lower()[0:5] in answer.lower() and not inverse[correctAnswer].lower()[0:5] in answer.lower():
        print ("Correct answer for #", answerCount+1," but incorrect formatting")
        print ("\t", correctAnswer[0:1],"-",answer)
        closeCount += 1
      else:
        print("Wrong answer for #", answerCount+1)
        wrongCount += 1
    print("Perfect:", str(perfectCount) + "/" + str(len(correct_answers)))
    print("Close:", str(closeCount) + "/" + str(len(correct_answers)))
    print("Wrong:", str(wrongCount) + "/" + str(len(correct_answers)))
    print("Correct VISA:", str(correct_VISA_count) + "/" + str(len(VISA_answers)))
    print("Correct MasterCard:", str(correct_MasterCard_count) + "/" + str(len(MasterCard_answers)))
    grade = 70 - (5 * wrongCount) 
    if(1 <= closeCount <= 4):
      grade -= 5
      comments += " Output did not match instructor's, "
    elif(closeCount > 4):
      grade -= 10
      comments += " Output did not match instructor's, "
    # Add points for extra credit - 5 if all correct, 3 if some.
    if correct_VISA_count == len(VISA_answers) and correct_MasterCard_count == len(MasterCard_answers):
      grade += 5
    elif correct_VISA_count > 0 or correct_MasterCard_count > 0:
      grade += 3


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
  comments += input ("General Comments?:  ")
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
