from os.path import os, exists
from datetime import datetime, timedelta
import subprocess
import sys
import re
import difflib

correct = open('correct.txt', 'r').read().split("\n")
correct = correct[0:-1]
outputFilename = 'assignment6.txt'
outputFile = open(outputFilename, 'w+')
outputFile.write('CSID\tGrade\tComments\n')
filename = "Hailstone.py"
dateString = "10-11-2013 23:00:00"
inputArray = open('input.txt','r').read().split("\n")
inputArray = inputArray[0:-1]

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
      assign6( csid , True)
  #singleton mode
  else:
    csid = sys.argv[1]
    os.system('clear')
    print('======================')
    print(csid)
    print('======================')
    assign6( csid , False)
  outputFile.close()

def assign6( csid , writeToFile) :
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
    for x in range(0, len(inputArray) - 1):
      process = subprocess.Popen(['python3', fileToGrade], stdin = subprocess.PIPE, stdout = subprocess.PIPE)
      try:
        out = process.communicate(bytes(inputArray[x].split()[0] + '\n' + inputArray[x].split()[1], 'UTF-8'))[0]
      except KeyboardInterrupt:
        grade -= 10
      answers.append(str(out)[2:-1])

    count = 0
    perfectCount = 0
    closeCount = 0 
    wrongCount = 0
    for answer in answers:
      nums = re.findall("\D+(\d+)\D+(\d+)", answer)
      if len(nums) != 1:
        wrongCount += 1
        continue
      elif len(nums[0]) != 2:
        wrongCount += 1
        continue
      longNum = int(nums[0][0])
      cycleLength = int(nums[0][1])

      #perfect check
      perfect = "Enter starting number of the range: Enter ending number of the range: The number " + str(correct[count].split()[0]) + " has the longest cycle length of " + str(correct[count].split()[1])
      regExMatch = "\s*Enter\s+starting\s+number\s+of\s+the\s+range:\s+Enter\s+ending\s+number\s+of\s+the\s+range:\s+The\s+number\s+" + str(correct[count].split()[0]) + "\s+has\s+the\s+longest\s+cycle\s+length\s+of\s+" + str(correct[count].split()[1] + "\D")
      if re.match(regExMatch, answer, re.IGNORECASE):
        print('Perfect answer for #', count + 1)
        perfectCount +=1
      elif longNum == int(correct[count].split()[0]) and cycleLength == int(correct[count].split()[1]):
        print('Closed answer for #', count + 1)
        print("\tPerfect: "+perfect+"\n\tvs.\n\tActual : "+answer)
        closeCount += 1
      else:
        print('Wrong answer for #', count + 1)
        print("\tPerfect: "+perfect+"\n\tvs.\n\tActual : "+answer)
        wrongCount += 1
      count += 1

    # Checking if the user handles bad input correctly
    # Counts for 5 test cases
    process = subprocess.Popen(['python3', fileToGrade], stdin = subprocess.PIPE, stdout = subprocess.PIPE)
    try:
      badInput = inputArray[len(inputArray)-1].split()
      out = process.communicate(bytes(badInput[0] + "\n" + badInput[1] + "\n" + badInput[2] + "\n" + badInput[3] + "\n" + badInput[4] + "\n" + badInput[5], 'UTF-8'))[0]
    except KeyboardInterrupt:
      grade -= 10
    answer = str(out)[2:-1]
    nums = re.findall("\D+(\d+)\D+(\d+)", answer)
    if len(nums) != 1:
      wrongCount += 5
    elif len(nums[0]) != 2:
      wrongCount += 5
    else:
      longNum = int(nums[0][0])
      cycleLength = int(nums[0][1])

      #perfect check
      if longNum == int(correct[-1].split()[0]) and cycleLength == int(correct[-1].split()[1]):
        print('Perfect answer for #', count + 1)
        perfectCount +=1
      else:
        print('Wrong answer for #', count + 1)
        perfect = "Enter starting number of the range: Enter ending number of the range: The number " + str(correct[-1].split()[0]) + " has the longest cycle length of " + str(correct[-1].split()[1])
        print("\tPerfect: "+perfect+"\n\tvs.\n\tActual : "+answer)
        wrongCount += 1
      count += 1

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
