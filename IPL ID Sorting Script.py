# IPL ID Sorting Script v1.0 r2
#
# A simple script to sort IPL id's
#
# What does this script do?
#
# This script sorts the id's of yout ipl file according to your ide files.
#
# Put your .ide and ipl files in the same dir as the program.Multiple file processing is also supported.
#
# Contact: user.grinch@gmail.com
#
# Script tested using Python 3.7.1 32-bit
# Last Updated on : 20/12/2018 

import glob, os

# ----- Functions -----

def get_files_with_extention(str_extention):
    str_extention = "./*." + str_extention
    return glob.glob(str_extention)

def process_ide_files(func_ide_list):
    if os.path.exists("temp_ide.txt"):
        os.remove("temp_ide.txt")

    for x in func_ide_list:
        with open(x,'r') as ide:
            with open("temp_ide.txt",'a') as temp_ide:
                valid_line : bool = False
                for line in ide:
                    
                    if (line[:4] == "objs" or line[:4] == "tobj"):
                        valid_line = True
                    
                    if valid_line and not (line[0] == '#' or line[0] == '\n' or (line[0] >= 'A' and line[0] <= 'z')):
                        temp_ide.write(line)

                    if (line[:3] == "end"):
                        valid_line = False

def get_id_name(func_line):
    if (func_line[0] != '\n'):
        data_line = func_line.split(',')
        return data_line

def is_inst_line(ipl_line):
    if(ipl_line[:3] == "end"):
        return "inst end" 
    elif not (ipl_line[0] == '#' or ipl_line[0] == '\n' or (ipl_line[0] >= 'A' and ipl_line[0] <= 'z')):
        return True
    return False

def remove_file(file):
    if os.path.exists(file):
        os.remove(file)

def process_ipl_files(func_ipl_list):      
    index = 0
    for y in func_ipl_list:
        should_break = False  
        with open(str(y),'r') as ipl:
            with open("temp_ipl.txt",'w') as temp_ipl:
                for a in ipl:
                    if(is_inst_line(a) == "inst end"):
                        temp_ipl.write("end\n")
                        for a in ipl:
                            temp_ipl.write(a)
                        should_break = True
                        break                
                    elif(is_inst_line(a)):
                        ipl_line = get_id_name(a)
                        with open("temp_ide.txt",'r') as temp_ide:
                            for b in temp_ide:
                                ide_line = get_id_name(b)
                                #ipl_line.pop()
                                if (ide_line[1] != ipl_line[1]):
                                    full_ipl_line = ",".join(ipl_line)
                                elif (ide_line[1] == ipl_line[1]):
                                    ipl_line[0] = ide_line[0]
                                    full_ipl_line = ",".join(ipl_line)
                                    break
                    else:
                        temp_ipl.write(a)
                        full_ipl_line = ''

                    if should_break:
                        break

                    if(full_ipl_line != ''):
                        temp_ipl.write(full_ipl_line)
        filename = str(ipl_files_list[index])
        remove_file(filename)
        os.rename("temp_ipl.txt",filename)
        index += 1
    remove_file("temp_ide.txt")
    print("Sorting finished sucessfully.")              

# ---------------------

# ----- Main -----

print("IPL ID Sorting Script\nAuthor:Grinch_\nContact: user.grinch@gmail.com\nUsage: Put all your ide and ipl files in this dir and press any key to run this script.")
input()
ide_files_list = get_files_with_extention("ide")
ipl_files_list = get_files_with_extention("ipl")

if ide_files_list and ipl_files_list:
    print("Found IDE files",ide_files_list,"\nFound IPL files", ipl_files_list)
else:
    print("Necessary files are missing,exiting...")
    
print("\nThis might take a while depending on the file count and size.Please be patient...\n\n--------------------------------------------------\n")

process_ide_files(ide_files_list)
process_ipl_files(ipl_files_list)
