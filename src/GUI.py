import PySimpleGUI as sg

# VIDEO LINK: https://www.youtube.com/watch?v=QeMaWQZllhg&list=WL&index=2&t=9090s

layout = [
    [sg.Text('Network Topology', key='-TOPOLOGY_SIZE-'), sg.Spin(['ex-small', 'small', 'medium', 'large'])],
    [sg.Text('Mapping Protocol'), sg.Spin(['Single-Mapping Path One', 'Multi-Mapping Path One', 'Single-Mapping Path Two', 'Multi-Mapping Path Two'])],
    [sg.Button('RUN SIMULATION', key='-START-'), sg.Button('SHOW RESULTS', key='-SHOW-')],
    [sg.Text('Number to convert: '), sg.Input(key='-X-'), sg.Text(key='-OUTPUT-')]
] # Each list is its own row!

window = sg.Window('FOG simulator', layout)   # WAITS FOR INPUT AND LOOKS FOR ANY KIND OF EVENT/RETURN VALUE
# ONCE WE ADD INPUT ITS GOING TO RETURN PAST THIS LINE

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break
    if event == '-START-':
        print(values)   # print(values['-INPUT-']) <-- if you only want one value
        # window['-TOPOLOGY_SIZE-'].update(values['-INPUT-']) <-- update something on your visual elements
        x = values['-X-']
        output = int(x) / 1000
        window['-OUTPUT-'].update(output)
    if event == '-SHOW-':
        print("SHOWING RESULTS")

window.close()