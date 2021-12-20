print ('''
This script detects parent packages and deletes their child files and packaegs.
It also deletes jrxml files.
You can comment a line to prevent jrxml deletion.
You may need to manually delete some paths like pom.xml
It's tested on SPS3 project only but may work seamlessly for other projects.

usage:
open cmd and navigate to the path where you saved the script
run it using:
python "Collecting Paths.py"
It will prompt for (input file name).
the output file will be in the same directory of the script:
Output file is named: Patch 3.1.xxx Program_Output.txt
I didn't prompt the user for output file for time saving purposes.
Feel free to edit and customize the script. ^_^ :)


Best regards
Omar AbdelWahab
01091392684
''')

import os
filename = input("Please, enter file path: ")
print (
'''If you have a black list file, you can enter its path below.
If you don't press enter.''')
black_list_path = input ("Please, enter black list file path:")
if (black_list_path.find(".txt") > -1):
    black = True
else:
    black = False
    print ("No blacklist considered")
#print (filename) #For debugging
#quit() # For debugging
no_of_packages = 0
#filename = "E:\\Omar AbdelWahab\\Temp\\Patch 3.1.444 5-12-2021 at 1422 Before editing.txt"
if (black):
    blacklist = open(black_list_path, 'r')
input_file = open(filename, 'r')
input_file2 = open(filename, 'r')
output_file_name = "Patch 3.1.xxx Program_Output.txt"
output_file = open(output_file_name, 'w')
paths_to_delete = []
packages = []

#Here we will iterate on the blacklist and add it to paths_to_delete
#We will find all the ones that match the blacklist names
#and print the ones that don't
if (black):
    print ("Unmatched paths in blacklist:")
    found = False
    unmatched = False
    for path in blacklist:
        path_n = path.replace("\n", "") #removes \n (end of line character)
        found = False
        input_file.seek(0) #To return to the begining of the file
        for line in input_file:
            line_n = line.replace("\n", "") #removes \n (end of line character)
            if (line_n.find(path_n) > -1):
                paths_to_delete.append(path_n)
                found = True
                break;
        if (not found):
            unmatched = True
            print (path_n)
    if (not unmatched):
        print ('''None. All blacklist paths have been found and deleted.''')
    else:
        print ("Matched paths in blacklist:")
        for matched in paths_to_delete:
            print(matched)
    input_file.seek(0)

#i = 0; #iterations for debugging
for line in input_file:
    pos = line.rfind("/") + 1
    if (line.find('.', pos) > -1):
        continue; # Skip files and keep directories
    #print(line[pos:])# prints the package name
    # Check if there's a line containing the same path but longer
    line_length = len(line)
    no_of_packages += 1
    line_n = line.replace("\n", "") #removes \n (end of line character)
    packages.append(line_n)
    #print(line_n)#This prints all packages even the ones inside packages

    input_file2.seek(0)
    for line2 in input_file2:
        line2_n = line2.replace("\n", "")
        if (line2.find(line_n) > -1 
            and len(line2_n) > line_length
            # To avoid packages named exportdeliveryrequestrevision
            # from being detected as a child of exportdeliveryrequest
            # So I count /s to assure different packages
            and (line2_n.count("/") > line_n.count("/")) 
            and (line2_n not in paths_to_delete)): 
            paths_to_delete.append(line2_n) 
            #print(line2_n)                
'''
    i+=1
    if (i > 3):
        break;
    
'''
#Print packages
no_of_child_packages = 0
no_of_parent_packages = 0
for p in packages:
    if (p not in paths_to_delete):
        #print(p)# Prints Packages For debugging
        output_file.write(p + "\n")
        no_of_parent_packages += 1
    else:
        no_of_child_packages += 1
        #print("d:", p) # prints child packages

no_of_printed_files = 0
input_file2.seek(0)
files = []
for line2 in input_file2:
    line2_n = line2.replace("\n", "")
    if (line2.find('.') > -1
        and line2.find('.jrxml') == -1 # Add a hash before this line to
        #                                prevent jrxml deletion
        and (line2_n not in paths_to_delete)):
        no_of_printed_files += 1
        files.append(line2_n)
        # print(line2_n) #prints files
# This loop is made to prevent trailing new line in the output file
lines = 0
for file in files:
    lines += 1
    if (lines < no_of_printed_files):
        output_file.write(file + "\n")
    else:
        #print("Entered else") # For debugging
        output_file.write(file)

#print(lines, no_of_printed_files) # For debugging
#Trying to delete the last line
#output_file.seek(output_file.tell() -1)
#output_file.write("\0")

# This loop is for integrity checking.
# It counts the number of undeleted jrxml files
# No. of undeleted jrxml is used in the sum of total document lines
# The undeleted jrxmls are the ones that are not inside a package (leaf files)
no_of_undeleted_jrxml_files = 0
input_file2.seek(0)
for line2 in input_file2:
    line2_n = line2.replace("\n", "")
    if(line2.find('.jrxml') > -1 and
       (line2_n not in paths_to_delete)):
        no_of_undeleted_jrxml_files += 1

print("no_of_packages:", no_of_packages)
print("no_of_parent_packages:", no_of_parent_packages)
print("no_of_child_packages:", no_of_child_packages)
print("no_of_printed_files:", no_of_printed_files)
#print("no_of_undeleted_jrxml_files:", no_of_undeleted_jrxml_files)
print("no_of_paths_to_delete:", len(paths_to_delete))
print("Total lines of original document should be:",
      no_of_parent_packages + no_of_printed_files
      + no_of_undeleted_jrxml_files + len(paths_to_delete))
if (black):
    blacklist.close()
input_file.close()
input_file2.close()
output_file.close()
# To prevent the command prompt from disappearing after the program finishes working
filename= "o"
while (filename[0] != 'e' and filename[0] != 'E'):
    filename = input("Please, enter e to exit: ")
