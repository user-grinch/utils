# IPL Object Renamer Script v1.0
#
# A simple script to rename objects against using ids.
#
# What does this script do?
#
# This script renames your ipl object names comparing with the ids of ide file.
#
# Put your .ide and ipl files in the same dir as the program.Multiple file processing is also supported.
#
# Contact: user.grinch@gmail.com
#
# Script tested using Python 3.7.1 32-bit
# Last Updated on : 12/02/2019 

import glob, os

# ----- Functions -----

def get_files_in_directory(str_extention):
    str_extention = "./*" + str_extention
    return glob.glob(str_extention)

def get_files_in_game_directory(root_dir,str_extention):
    list = []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(str_extention):
                list.insert(-1,os.path.join(dirpath, filename))
    return list

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
                                if (ide_line[0] != ipl_line[0]):
                                    full_ipl_line = ",".join(ipl_line)
                                elif (ide_line[0] == ipl_line[0]):
                                    ipl_line[1] = ide_line[1]
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
    print("Renaming finished sucessfully.")

# ---------------------

# ----- Main -----

print("IPL Object Renamer Script\nAuthor:Grinch_\nContact: user.grinch@gmail.com\nUsage: Put all your ipl files in this dir and press any key to run this script.")

game_dir = input("\nProvide path to ide files (game directory, no quotes):")

ipl_files_list = get_files_in_directory(".ipl")
ide_files_list = get_files_in_game_directory(game_dir,".ide")

if ide_files_list and ipl_files_list:
    print("\n--------------------\nIDE files found: ",len(ide_files_list),"\nIPL files found: ",len(ipl_files_list),"\n--------------------\n")
    input("\nPress any key to procceed")
    print("\nThis might take a while depending on the file count and size.Please be patient...\n\n--------------------------------------------------\n")
    process_ide_files(ide_files_list)
    process_ipl_files(ipl_files_list)
else:
    print("Necessary files are missing,exiting...")

input("\nPress any key to procceed")
