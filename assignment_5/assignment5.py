from os.path import os, exists
from datetime import datetime, timedelta
import subprocess
import sys
import re
import difflib

correct = open('correct.txt', 'r').read().split()
outputFilename = 'assignment5.txt'
outputFile = open(outputFilename, 'w+')
outputFile.write('CSID\tGrade\tComments\n')
filename = "CalcSqrt.py"
dateString = "10-07-2013 23:00:00"
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
      assign5( csid , True)
  #singleton mode
  else:
    csid = sys.argv[1]
    os.system('clear')
    print('======================')
    print(csid)
    print('======================')
    assign5( csid , False)
  outputFile.close()

def assign5( csid , writeToFile) :
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
  if not fileToGrade == "" and late < 3:
    answers = []
    for x in range(0,len(inputArray)-2):
      process = subprocess.Popen(['python3', fileToGrade], stdin = subprocess.PIPE, stdout = subprocess.PIPE)
      out = process.communicate(bytes(inputArray[x], 'UTF-8'))[0]
      answers.append(str(out)[2:-1])

    correctCount = 0
    perfectCount = 0
    closeCount = 0 
    wrongCount = 0
    for answer in answers:
      nums = re.findall("\D+(\d+\.\d+)\D+(\d+\.\d+e?-?\d*)", answer)
      if len(nums) != 1:
        wrongCount += 1
        continue
      elif len(nums[0]) != 2:
        wrongCount += 1
        continue
      sqrt = float(nums[0][0])
      diff = float(nums[0][1])
      rounded = round(float(correct[correctCount]),11)

      #perfect check
      perfect = "Enter a positive number: Square root is: " + str(sqrt) +"\\nDifference is: " + str(diff)+"\\n"
      if perfect == answer:
        print('Perfect answer for #', correctCount + 1)
        perfectCount +=1
      elif diff < 1e-6 and (str(rounded) in str(sqrt) or str(correct[correctCount]) == str(sqrt)): 
        print('Close answer for #', correctCount + 1)
        print("\t"+perfect+"\n\tvs.\n\t"+answer)
        closeCount += 1
      else:
        print('Wrong answer for #', correctCount + 1)
        print("\t"+perfect+"\n\tvs.\n\t"+answer)
        wrongCount += 1
      correctCount += 1

    # Checking if the user handles bad input correctly
    # Counts for 5 test cases
    process = subprocess.Popen(['python3', fileToGrade], stdin = subprocess.PIPE, stdout = subprocess.PIPE)
    out = process.communicate(bytes(inputArray[len(inputArray)-2] + "\n" + inputArray[len(inputArray)-1], 'UTF-8'))[0]
    answer = str(out)[2:-1]
    nums = re.findall("\D+(\d+\.\d+)\D+(\d+\.\d+e?-?\d*)", answer)
    if len(nums) == 0:
      wrongCount += 5
    elif len(nums[0]) != 2:
      wrongCount += 5
    else:
      sqrt = float(nums[0][-2])
      diff = float(nums[0][-1])
      rounded = round(float(correct[correctCount]),11)
      perfect = "Enter a positive number: Square root is: " + str(sqrt) +"\\nDifference is: " + str(diff) +"\\n"
      if perfect in answer:
        print('Perfect answer for bad input')
        perfectCount +=5
      elif diff < 1e-6 and (str(rounded) in str(sqrt) or str(correct[correctCount]) == str(sqrt)): 
        print('Close answer for bad input')
        print("\t"+perfect+"\n\tvs.\n\t"+answer)
        closeCount += 5
      else:
        print('Wrong answer for bad input')
        print("\t"+perfect+"\n\tvs.\n\t"+answer)
        wrongCount += 5

    print("Perfect:", str(perfectCount) + "/10")
    print("Close:", str(closeCount) + "/10")
    print("Wrong:", str(wrongCount) + "/10")
    if wrongCount != 0 or closeCount != 0:
        grade -= (2 * wrongCount) 
        grade -= (1 * closeCount)
        comments += " Output did not match instructors P: "+str(perfectCount)+" C: "+str(closeCount)+" W: "+str(wrongCount)+ ", "


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
