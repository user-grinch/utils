import PySimpleGUI as sg 
import struct, re, sys, webbrowser

###############################################
sg.theme('Material 2')
sg.theme_input_background_color("White")
sg.theme_input_text_color("Black")
sg.theme_text_color("Black")
###############################################
# Format
header_format = "4s18i"
inst_format = "7f3i"
cars_format = "4f8i"
header_size = struct.calcsize(header_format)
inst_size = struct.calcsize(inst_format)
cars_size = struct.calcsize(cars_format)
###############################################

program_name = "IPL Editor"
filename:str = None
filetype:str = " "

# string variables to shorten loop and menu code
file_new: str =  'New   CTRL+N'
file_open: str = 'Open  CTRL+O'
file_save: str = 'Save  CTRL+S'

doc_links = ['Auzo','Cars','Cull','Enex','Grge','Inst','Jump','Mult','Occl','Path','Pick','Tcyc','Zone']

menu_layout: list = [['File', [file_new, file_open, file_save, 'Save As Text', 'Save As Binary']],
                     ['Documentation', doc_links],
                     ['Help', ['About']]]

layout: list = [[sg.Menu(menu_layout)],
                [sg.Multiline(font=('Consolas', 11), key='_BODY_',enable_events=True,size=sg.Window.get_screen_size())]
                ]

window: object = sg.Window(program_name, layout=layout,size=(750,450),margins=(0,0), resizable=True, return_keyboard_events=True,font=("Consolas",11),finalize=True)

def new_file() -> str:
    ''' Reset body and info bar, and clear filename variable '''
    window['_BODY_'].update(value='')
    filename = None
    window.TKroot.title(program_name)
    return filename

def open_file() -> str:
    ''' Open file and update the infobar '''
    try:
        filename: str = sg.popup_get_file('Open File', no_window=True,file_types=(('IPL Files', '*.ipl*'),),icon="C:\\Users\\Grinch_\\Desktop\\Notepad-master\\icon.png")
    except:
        return
    if filename not in (None, '') and not isinstance(filename, tuple):
        window['_BODY_'].update(value=read_file(filename))
        window.TKroot.title(program_name + "    " + filename + filetype)

    return filename

    return filename

def save_file(filename: str):
    ''' Save file instantly if already open; otherwise use `save-as` popup '''
    if filename not in (None, ''):
        write_file(filename)
    else:
        save_file_as()

def save_file_as() -> str:
    ''' Save new file or save existing file with another name '''
    try:
        filename: str = sg.popup_get_file('Save File',file_types=(('IPL Files', '*.ipl*'),), save_as=True, no_window=True,default_extension=".ipl")
    except:
        return
    if filename not in (None, '') and not isinstance(filename, tuple):
        write_file(filename)
    return filename

def about_me():
    sg.Popup(program_name + " v1.1\nCreated by Grinch_\nWebsite:user-grinch.github.io",button_type=5,title="")

def read_file(filename) -> str: 
    global filetype
    file : str = None
    data : str = None

    try:
        file = open(filename, "rb")
        data = struct.unpack(header_format, file.read()[:header_size])
    except:
        sg.Popup("The binary file format is not recognized",button_type=5,title="Error")
        return

    # reading 'bnry' identifier
    if str(data[0])[2:-1] != "bnry":
        file.close()
        filetype = " (text)"
        with open(filename, 'r') as file:
            return file.read()
    else:
        filetype = " (binary)"

    inst_instances = data[1]
    car_instances = data[5]
    text : str = "# Binary file converted to text using "+ program_name +"\ninst\n"

    size = header_size

    for x in range(inst_instances):
        file.seek(0, 0)
        try:
            data = struct.unpack(inst_format, file.read()[size:(size + inst_size)])
            size += inst_size
        except:
            sg.Popup("Error reading the IPL file",button_type=5,title="Error")
            return
        text += "{}, dummy, {}, {:.4f}, {:.4f}, {:.4f}, {:.4f}, {:.4f}, {:.4f}, {:.4f}, {}\n".format(data[7],data[8],data[0],data[1],data[2],data[3],
        data[4],data[5],data[6],data[9])

    text += "end\ncars\n"

    for x in range(car_instances):
        file.seek(0, 0)
        try:
            data = struct.unpack(cars_format, file.read()[size:(size + cars_size)])
            size += cars_size
        except:
            sg.Popup("Error reading file",button_type=5,title="Error")
            return
        text += "{:.4f}, {:.4f}, {:.4f}, {:.4f}, {}, {}, {}, {}, {}, {}, {}, {}\n".format(data[0],data[1],data[2],data[3],data[4],data[5],data[6],
        data[7],data[8],data[9],data[10],data[11])
    text += "end"
    file.close()
    return text

def write_file(save_name):
    global filetype
    global filename

    if filetype == " (text)":
        with open(save_name,'w') as f:
            f.write(values.get('_BODY_'))
            filename = save_name
        return
    else:
        try:
            is_inst_section : bool = False
            is_cars_section : bool = False
            inst_data : list = []
            cars_data : list = []
            inst_count : int = 0
            cars_count : int = 0

            for line in values.get('_BODY_').splitlines():
                temp: str = re.findall(r'[-,+]?\b\d[\d,.]*\b',line)

                if line == "inst":
                    is_inst_section = True
                if line == "cars":
                    is_cars_section = True
                
                if line == "end":
                    if is_inst_section:
                        is_inst_section = False
                        
                    if is_cars_section:
                        is_cars_section = False

                if (line.lstrip())[0:1] != '#':
                    if is_inst_section and len(temp) == 10:
                        inst_data.append(temp)
                        inst_count = inst_count + 1

                    if is_cars_section and len(temp) == 12:
                        cars_data.append(temp)
                        cars_count = cars_count + 1
            
            with open(save_name,'wb') as f:

                write_data :bytes = b""
                cars_offset : int  = 0

                for data in inst_data:
                    write_data += struct.pack(inst_format,float(data[2]),float(data[3]),float(data[4]),float(data[5]),float(data[6]),float(data[7]),float(data[8]),int(data[0]),int(data[1]),int(data[9]))
                    cars_offset += inst_size

                for data in cars_data:
                    write_data += struct.pack(cars_format,float(data[0]),float(data[1]),float(data[2]),float(data[3]),int(data[4]),int(data[5]),int(data[6]),int(data[7]),int(data[8]),int(data[9]),int(data[10]),int(data[11]))
                
                write_data = struct.pack(header_format,b'bnry',inst_count,0,0,0,cars_count,0,76,0,0,0,0,0,0,0,cars_offset,0,0,0) + write_data

                f.write(write_data)
                filename = save_name
        except:
            sg.Popup("An error occur while writing to file",button_type=5,title="Error")

    window.TKroot.title(program_name + '    ' + filename + filetype)

window.TKroot.iconbitmap("icon.ico")

while True:
    event, values = window.read()

    if event is None:
        break
    if event in (file_new, 'n:78'):
        filename = new_file()
    if event in (file_open, 'o:79'):
        filename = open_file()
    if event in (file_save, 's:83'):
        save_file(filename)
    if event is 'Save As Text':
        filetype = " (text)"
        filename = save_file_as()   
    if event is 'Save As Binary':
        filetype = " (binary)"
        filename = save_file_as()   
    if event is 'About':
        about_me()
    if event in doc_links:
        webbrowser.open('https://gtamods.com/wiki/' + event, new=2)