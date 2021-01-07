import os
import secrets
import PySimpleGUI as sg

#Final answer will be a hexadecimal like: 00-0000-00-00-00000000-000000 OR producttype-resinname-color-containersize-serial-buffer

#DATA (CHANGE THESE WITH THE SIMILAR FORMAT ANYTIME NEW RESIN COMES OUT)

new_color_mapping = {
                "00": {'name':'black','color':'#4A4A4A'},
                "01": {'name':'light grey','color':'#A1A1A1'},
                "02": {'name':'transluscent','color':'#C4C4C4'},
                "03": {'name':'white','color':'#C4C4C4'},
                "04": {'name':'blue','color':'#0068FF'},
                "05": {'name':'light blue','color':'#0099FF'},
                "06": {'name':'green','color':'#0EAC3A'},
                "07": {'name':'yellow','color':'#F0CE2B'},
                "08": {'name':'purple','color':'#B919D1'},
                "09": {'name':'red','color':'#FF0000'},
                "10": {'name':'orange','color':'#FF9626'},
                "11": {'name':'light brown','color':'#D7944E'}
                }


new_resin_full_mapping = {
                "0000": {'name':'xGPP-Blue','color':'04'},
                "0001": {'name':'xGPP-Transluscent','color':'02'},
                "0002": {'name':'xGPP-Gray','color':'01'},
                "0003": {'name':'xMED412','color':'02'},
                "0004": {'name':'xPRO410','color':'00'},
                "0005": {'name':'xCE-White','color':'02'},
                "0006": {'name':'xCast','color':'07'},
                "0007": {'name':'xCE-Black','color':'00'},
                "0008": {'name':'3843-xABS Black','color':'00'}
}

list_of_resins = []
for resins in new_resin_full_mapping:
    list_of_resins.append(new_resin_full_mapping[resins]['name'])

#switch places
Size_mapping = {
            '1 kg':"01",
            '2 kg':"02",
            '5 kg':"05",
            '10 kg':"10"
                }


sg.ChangeLookAndFeel('Dark Blue 3')
layout = [  [sg.Text('Resin RFID Hexadecimal Maker', size=(30, 1), font=("Helvetica", 25))],
            [sg.Text('Pick the resin type:')],
            [sg.Listbox(list_of_resins, size=(20, len(list_of_resins)), key='-Resin-', enable_events=True)],
            [sg.Text('Pick the container size:')],
            [sg.Listbox(list(Size_mapping.keys()), size=(20, len(list(Size_mapping.keys()))), key='-Size-', enable_events=True)]
             ]

window = sg.Window('RFID GUI', layout)

while True: # the event loop
    event, values = window.read()
    serial = str(secrets.token_hex(4)) #randomly generated serial
    buffer = "000000"
    serial_int = int("0x"+ serial, 0)
    if event == sg.WIN_CLOSED:
        break
    if values['-Resin-'] and values['-Size-']:    # if something is selected in the list
        product_type = "02" #Reffering to resins
        for resins in new_resin_full_mapping:
            if new_resin_full_mapping[resins]['name'] == values['-Resin-'][0]:
                resin = resins
                color = new_resin_full_mapping[resins]['color']
        size = Size_mapping[values['-Size-'][0]]
        RFIDcode_beginning = int(product_type + resin + color + size + str(serial_int))
        sum_of_digits = sum(int(digit) for digit in str(RFIDcode_beginning))
        RFIDcode = product_type + resin + color + size + serial + buffer
        if len(RFIDcode) == 24:
            code = [[sg.Multiline(RFIDcode)], [sg.Button("Exit", button_color=("white","Red"), size=(6, 1))]]
            coded = sg.Window('Copy/Paste your hexadecimal', code)
            event, values = coded.read()
            if event == "Exit":
              coded.close()
        else:
            print("Broken because length of code is " + str(len(RFIDcode)) + ", and it should be 24")
            break

#change settings when you want to add a new (pre-approved resin), changing the actual dictionary