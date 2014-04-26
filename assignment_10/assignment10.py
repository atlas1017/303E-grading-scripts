from os.path import os, exists
from datetime import datetime, timedelta
from functools import *
import math
import subprocess
import sys
import re
import difflib

pipes = {'stdout':subprocess.PIPE, 'stdin':subprocess.PIPE, 'stderr':subprocess.PIPE}

outputFilename = 'assignment10.txt'
outputFile = open(outputFilename, 'a')
filename = "Cipher.py"
files_to_encrypt = ('encrypt1.txt', 'encrypt2.txt', 'encrypt3.txt')
files_to_decrypt = ('decrypt1.txt', 'decrypt2.txt', 'decrypt3.txt')
dateString = "04-04-2014 23:59:59"

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
      assign10( csid , True)
  #singleton mode
  else:
    csid = sys.argv[1]
    os.system('clear')
    print('======================')
    print(csid)
    print('======================')
    assign10( csid , False)
  outputFile.close()

def assign10(csid , writeToFile) :
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


  # copies ../FILE_TO_COPY to ./ and runs the program in ./
  # diffs output.txt with FILE_CORRECT
  # returns tuple (file output matches, stdout output matches)
  def cp_run_and_diff (stdin_text, file_to_copy, file_correct, stdout_correct):
    os.chdir('..')
    subprocess.getoutput('rm %soutput.txt' % csid)
    os.system("cp %s '%s/input.txt'" % (file_to_copy, csid))
    os.chdir(csid)
    process = subprocess.Popen(['python3', fileToGrade], **pipes)
    stdout_output = str(process.communicate(bytes(stdin_text, 'UTF-8'))[0])[2:-1]
    print("%s %s" % ("Encrypting" if stdin_text == 'E' else "Decrypting", file_to_copy))
    try:
      differences = subprocess.getoutput('diff -w output.txt ../%s' % file_correct)
      if differences != '':
        print("Expected:")
        line = ""
        [print("\t|%s" % line.strip()) for line in open('../%s' % file_correct, 'r')]
        print("Actual:")
        line = ""
        [print("\t|%s" % line.strip()) for line in open('output.txt', 'r')]
      else:
        print("File outputs match")
    except:
      print("Program did not output to file.")
    subprocess.getoutput('rm output.txt')
    subprocess.getoutput('rm input.txt')
    stdout_output = '\n'.join([line if line.count(' ') != len(line) else '\n' for line in stdout_output.replace(r'\n', '\n').replace('decrpyt', 'decrypt').strip().split('\n')])
    print("STDOUT matches\n" if stdout_output == stdout_correct else "STDOUT does not match:\n%s\n" % stdout_output)
    return (differences == '', stdout_output == stdout_correct)

  if late != -1:
    # encrypting (3 tests; worth 4 points each; max 15)
    encrypt_tests = []
    # decrypting (3 tests: worth 4 points each; max 15)
    decrypt_tests = []
    # program formatting (1 test: worth 5 points)
    format_test = True
    correct_format = 'Do you want to encrypt or decrypt? (E / D): \nOutput written to output.txt'

    for decrypted, encrypted in zip (files_to_encrypt, files_to_decrypt):
      (correctness, format_test1) = cp_run_and_diff ('E', decrypted, encrypted, correct_format)
      encrypt_tests.append(correctness)
      (correctness, format_test2) = cp_run_and_diff ('D', encrypted, decrypted, correct_format)
      decrypt_tests.append(correctness)
      format_test = format_test and format_test1 and format_test2

    
      
    if all(encrypt_tests) and all(decrypt_tests) and format_test:
      print("Perfect! ^_^")
      comments.append("passed all tests")
    elif not (any(encrypt_tests) or any(decrypt_tests) or format_test):
      print("Failed every test... ='(")
      comments.append("failed all tests (-30)")
      grade -= 30
    else:
      first_fail = True

      def print_fail (string):
        nonlocal first_fail
        if first_fail:
          first_fail = False
          print(string)

      functionality_fail = "Tests failed (5 points each):"
      num_off = 0
      if not encrypt_tests[0]:
        print_fail (functionality_fail)
        print("\tEncrypt even length")
        comments.append("failed encrypt even (-5)")
        num_off += 5
      if not encrypt_tests[1]:
        print_fail (functionality_fail)
        print("\tEncrypt odd length")
        comments.append("failed encrypt odd (-5)")
        num_off += 5
      if not encrypt_tests[2]:
        print_fail (functionality_fail)
        print("\tEncrypt multiple lines")
        comments.append("failed encrypt multi (-5)")
        num_off += 5
      if not decrypt_tests[0]:
        print_fail (functionality_fail)
        print("\tDecrypt even length")
        comments.append("failed decrypt even (-5)")
        num_off += 5
      if not decrypt_tests[1]:
        print_fail (functionality_fail)
        print("\tDecrypt odd length")
        comments.append("failed decrypt odd (-5)")
        num_off += 5
      if not decrypt_tests[2]:
        print_fail (functionality_fail)
        print("\tDecrypt multiple lines")
        comments.append("failed decrypt multi (-5)")
        num_off += 5
      if not format_test:
        print_fail (functionality_fail)
        print("\tSTDOUT Formatting")
        comments.append("incorrect formatting (-5)")
        num_off += 5
      grade -= num_off
      print("Total off: (-%d)" % num_off)

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
