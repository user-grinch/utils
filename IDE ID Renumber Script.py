# IDE ID Renumber Script v1.0 r2
#
# A simple script to renumber IDE id's
#
# What this script does?
#
# This simple script just renumbers your object ids from .ide files with your given value.
#
# Usage: Put all your ide files in this dir and press any key to run this script.
#
# Contact: user.grinch@gmail.com
#
# Script tested using Python 3.7.1 32-bit
# Last Updated on : 20/12/2018 

import glob,os,sys

# ----- Functions -----

def get_files_with_extention(str_extention):
    str_extention = "./*." + str_extention
    return glob.glob(str_extention)

def remove_file(file):
    if os.path.exists(file):
        os.remove(file)

# ---------------------


print("IDE ID Renumber Script\nAuthor : Grinch_ \nContact: user.grinch@gmail.com\nUsage: Put all your ide files in this dir and press any key to run this script.")
input()
ide_files_list = get_files_with_extention("ide")
if ide_files_list:
    print("Found IDE files",ide_files_list)
else:
    print("No IDE files found,exiting...")
    sys.exit()
 
start_id = input("Enter start id: ")


print("\nThis might take a while depending on the file count and size.Please be patient...\n\n--------------------------------------------------\n")

index = 0
for x in ide_files_list:
    with open(x,'r') as source_file:
        with open("temp_ide.txt",'w') as dst_file:

            valid_line : bool = False

            for line in source_file:
                
                if (line[:4] == "objs" or line[:4] == "tobj"):
                    valid_line = True
                
                if not (line[0] == '#' or line[0] == '\n' or (line[0] >= 'A' and line[0] <= 'z')):
                    if valid_line:
                        ide_line = line.split(',')
                        ide_line[0] = str(start_id)
                        ide_line.pop()
                        ide_line = ",".join(ide_line) + ", 0\n"
                        dst_file.write(ide_line)
                        start_id = int(start_id) + 1
                    else:
                        dst_file.write(line)
                else:
                    dst_file.write(line)

                if (line[:3] == "end"):
                    valid_line = False

    filename = str(ide_files_list[index])
    remove_file(filename)
    os.rename("temp_ide.txt",filename)
    index += 1


print("IDE files renumbered sucessfully.Press any key to exit.")
input()
