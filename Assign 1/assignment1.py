from os.path import os, exists
from datetime import datetime, timedelta
import subprocess
import sys
import re
import difflib

outputFile = open('assignment1.txt', 'w')
correct = open('correct.txt', 'r').read()
filename = "Logo.py"
dateString = "09-11-2013 23:00:00"
outputFile.write('CSID\tGrade\tComments\n')

def main():
  out = subprocess.getoutput('ls ./')
  CSIDS = out.split("\n")
  if len(sys.argv) == 2:
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
      assign1( csid )
    outputFile.close()
  #singleton mode
  else:
    


def assign1( csid ) :
  fileToGrade = ""
  late = 0
  linesWrong = 0
  grade = 70
  style = 30
  wrongFileName = False
  header = True
  comments = ""
  manualComments = ""

  os.chdir(csid)
  outputFile.write(csid + "\t")
  files = os.listdir('.')

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
      outputFile.write("0\tno file")
    else :
      splitted = subprocess.getoutput('ls -l ' + fileToGrade.replace(' ','\ ')).split()
      late = isLate(splitted)
      wrongFileName = True

  #grading time!
  if not fileToGrade == "" and late < 3:
    out = subprocess.getoutput('python3 ' + fileToGrade)
    lines = out.split('\n')
    if len(lines) == 19 :
      if re.match('\s*', lines[0]) is None :
        linesWrong += 1
      if re.match('         \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\s*', lines[1]) is None :
        linesWrong += 1
      if re.match('        \*\*\*\$\$\$\$\$\$\$\$\$\$\$\$\$\$\*\*\s*', lines[2]) is None :
        linesWrong += 1
      if re.match('       \*\* \$\$         \$\$ \$ \*\*\s*', lines[3]) is None :
        linesWrong += 1
      if re.match('      \*\* \$\$           \$\$\$  \*\*\s*', lines[4]) is None :
        linesWrong += 1
      if re.match('     \*\* \$\$\$                 \*\*\s*', lines[5]) is None :
        linesWrong += 1
      if re.match('      \*\$\$\$\$\$\$\$\$\$           \*\*\s*', lines[6]) is None :
        linesWrong += 1
      if re.match('       \*\$\$\$\$\$\$\$\$\$\$\$\$\$\$    \*\*\s*', lines[7]) is None :
        linesWrong += 1
      if re.match('        \*\*\$\$\$\$\$\$\$\$\$\$\$\$\$\$\$\*\*\s*', lines[8]) is None :
        linesWrong += 1
      if re.match('         \*\*      \$\$\$\$\$\$\$\*\*\s*', lines[9]) is None :
        linesWrong += 1
      if re.match('          \*\*         \$\$\*\*\s*', lines[10]) is None :
        linesWrong += 1
      if re.match('           \*\*\$\$\$    \$\$\*\*\s*', lines[11]) is None :
        linesWrong += 1
      if re.match('            \*\$\$\$\$\$\$\$\$\*\*\s*', lines[12]) is None :
        linesWrong += 1
      if re.match('             \*\*     \*\*\s*', lines[13]) is None :
        linesWrong += 1
      if re.match('              \*\*   \*\*\s*', lines[14]) is None :
        linesWrong += 1
      if re.match('               \*\* \*\*\s*', lines[15]) is None :
        linesWrong += 1
      if re.match('                \*\*\*\s*', lines[16]) is None :
        linesWrong += 1
      if re.match('                 \*\s*', lines[17]) is None :
        linesWrong += 1
      if re.match('\s*', lines[18]) is None :
        linesWrong += 1
    else :
      print('Their output:')
      print(out)
      print('Correct output:')
      print(correct)
      print('logo has ' + str(len(lines)) +' lines, not 19')
      #don't dock points for lateness or wrong filename here
      gradeInput = input("Grade out of 70 (no style, hit enter if 65): ")
      if gradeInput == '' :
        grade = 65
      else :
        grade = int(gradeInput)
      manualComments = input("Comments: ")

    #checking for header and style
    #os.system('vim ' + fileToGrade)
    print(subprocess.getoutput('cat ' + fileToGrade))
    headerInput = input("Header(y or enter/n)? ")
    if headerInput == 'y' or headerInput == '' :
      header = True
    else :
      header = False
    style = input("Style/Comments (out of 30, hit enter for 30): ")
    if not style.isdigit() :
      style = 30
    else :
      style = int(style)
    
    #writing grade time!
    if late == 3 :
      outputFile.write('0\t 3 days late')
    else :
      if late == 2 :
        comments = "2 days late, "
        grade -= 20
      elif late == 1 :
        comments = "1 day late, "
        grade -= 10
      
      if wrongFileName :
        comments += "wrong filename, "
        grade -= 10
      if not header :
        comments += "no/malformed header, "
        grade -= 10

      if linesWrong > 0 and linesWrong < 3 : 
        comments += "improperly formed superman logo, "
        grade -= 5
      elif linesWrong > 3 :
        comments += "nonsensical superman logo, "
        grade -= 5
      outputFile.write(str(grade+style) + "\t"+comments.rstrip(', ') + manualComments)
      
  outputFile.write('\n')
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
