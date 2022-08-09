# IPL Spliter Script v1.0
#
# A simple script to split ipl files with a given range
#
#
# Put your .ide and ipl files in the same dir as the program.Multiple file processing is also supported.
#
# Contact: user.grinch@gmail.com
#
# Script tested using Python 3.7.1 32-bit
# Last Updated on : 23/02/2019 

import glob,os

# ----- Functions -----

def get_files_with_extention(str_extention):
    str_extention = "./*." + str_extention
    return glob.glob(str_extention)

def is_inst_line(ipl_line,total_lines,counter):
    if(ipl_line[:3] == "end"):
        return "end file" 
    elif (total_lines < counter):
        return "next file" 
    elif (ipl_line[0] != '#' or ipl_line[0] != '\n'):
        return "inst line"

def split_ipl_files(func_ipl_list,total_lines):
    for y in func_ipl_list:
        file_count = 1
        with open(y,'r') as ipl:
            counter = 0
            file_loc = (os.path.splitext(os.path.basename(y))[0]) + str(file_count) + ".ipl"
            out_file = open(file_loc,"w+")
            out_file.write("inst\n")
            for a in ipl:
                if(a == "inst" or a == "end" or a[0] == "#"):
                    pass
                elif(total_lines > counter):
                    out_file.write(a)
                    counter = counter + 1
                elif(total_lines == counter):
                    out_file.write("end")
                    file_count = file_count + 1
                    file_loc = (os.path.splitext(os.path.basename(y))[0]) + str(file_count) + ".ipl"
                    out_file.close()
                    out_file = open(file_loc,"w+")
                    out_file.write("inst\n")
                    counter = 0
                    
            out_file.write("end")
            out_file.close()
                        

    print("Splitting files sucessfully.")

#----------------------

#-----Main-----
print("IPL Spliter Script\nAuthor:Grinch_\nContact: user.grinch@gmail.com\nUsage: Put all your ide and ipl files in this dir and press any key to run this script.")
input()
ipl_files_list = get_files_with_extention("ipl")

if ipl_files_list:
    print("Found IPL files", ipl_files_list)
else:
    print("Necessary files are missing,exiting...")

total_lines = int(input("Enter total number of lines:"))

print("\nThis might take a while depending on the file count and size.Please be patient...\n\n--------------------------------------------------\n")

split_ipl_files(ipl_files_list,total_lines)
