from os.path import os, exists
from datetime import datetime, timedelta
from functools import *
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
dateString = "03-05-2012 23:05:00"
inputArray = open('input.txt','r').read().split("\n")

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
  if not fileToGrade == "" and late != -1:
    answers = []
    for x in range(len(inputArray)):
      process = subprocess.Popen(['python3', fileToGrade], stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
      try:
        out = process.communicate(bytes('\n'.join(inputArray[x].split()) + '\n', 'UTF-8'))[0]
      except KeyboardInterrupt:
        pass
      answers.append(str(out)[2:-1])

    count = 0
    perfectCount = 0
    closeCount = 0 
    wrongCount = 0
    for answer, cor in zip(answers,correct):
      cor = cor.split()
      #extracting relevant data form the students output
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
      if count >= 6: #negative testing time! 
        perfect = "Enter starting number of the range: \nEnter ending number of the range: \n" * 6 +"The number " + str(cor[0]) + " has the longest cycle length of " + str(cor[1]+".")
      else:
        perfect = "Enter starting number of the range: \nEnter ending number of the range: \nThe number " + str(cor[0]) + " has the longest cycle length of " + str(cor[1]+".")

      if perfect == answer.replace('\\n','\n').rstrip('\n'):
        print('Perfect answer for #', count + 1)
        perfectCount +=1
      elif longNum == int(cor[0]) and cycleLength == int(cor[1]):
        print('Close answer for #', count + 1)
        print(perfect+"\n\tvs.\n\t"+answer.replace('\\n','\n\t'))
        closeCount += 1
      else:
        print('Wrong answer for #', count + 1)
        print(perfect+"\n\tvs.\n\t"+answer.replace('\\n','\n\t'))
        wrongCount += 1
      count += 1

    print("Perfect:", str(perfectCount) + "/10")
    print("Close:", str(closeCount) + "/10")
    print("Wrong:", str(wrongCount) + "/10")
    if wrongCount != 0 or closeCount != 0:
        grade -= (3 * wrongCount) 
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
