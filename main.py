variables = []
functions = []
digits = '0123456789'

UNDEFINED = 'UNDEFINED'

class Variable:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    
    def change(self, value):
        self.value = value

class Function:
    def __init__(self, name, codelines):
        self.name = name
        self.codelines = codelines
    
    def execute(self):
        for codeline in self.codelines:
            run(codeline)

def run(code, lines):
    details = code.split(' ')
    command = details[0]
    lastfuncname = ''
    if code.startswith('//'):
        return ''
    if command == 'exit':
        exit()
    elif command == 'print':
        toprint = details[1]
        if toprint.startswith('"'):
            return code.split('"')[1]
        else:
            variablename = details[1]
            for var in variables:
                if var.name == variablename:
                    return var.value
    elif command == 'var':
        name = details[1]
        value = UNDEFINED

        if len(details) > 2 and details[2] == '=':
            if details[3].startswith('"'):
                value = code.split('"')[1]
            else:
                for var in variables:
                    if var.name == details[3]:
                        value = var.value
                        break
                value = details[3]
    
        variables.append(Variable(name, value))
        return ''
    for var2 in variables:
        if var2.name == command:
            expression = details[1]
            value = ''
            if expression == '=':
                if details[2].startswith('"'):
                    value = code.split('"')[1]
                else:
                    for var in variables:
                        if var.name == details[3]:
                            value = var.value
                            break
                    value = details[3]
                var2.value = value
            elif expression == '++':
                var2.value = str(int(var2.value) + 1)
            elif expression == '--':
                var2.value = str(int(var2.value) - 1)
        return ''
    if command == 'sleep':
        seconds = details[1]
        return '&sleep:' + seconds
    elif command == 'clear':
        return '&clear:NONE'
    elif ':' in code:
        lastfuncname = code.split(':')[0]
        return ''
    elif code == '.':
        infunc = False
        funclines = []
        for line in lines:
            if infunc:
                funclines.append(line)
            if ':' in line:
                infunc = True
            if line == '.':
                infunc = False
                break
        func = Function(lastfuncname, funclines)
        functions.append(func)
        return ''
    elif command == 'exec':
        for func in functions:
            if func.name == details[1]:
                func.execute()
        return ''
    elif command == 'input':
        inp = input(code.split('"')[1])
        var = details[2]
        run(var + ' = "' + input + '"')
        return ''

import sys
import time
from os import system, name

def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
  
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

f = open(sys.argv[1], "r")
content = f.read()
lines = content.split("\n")
index = 0
for line in lines:
    if line == '' or line == None:
        continue
    result = run(line, lines)
    if len(result) <= 0:
        continue
    if result.startswith("&"):
        func = result.split("&")[1].split(":")[0]
        value = result.split(":")[1]
        if func == "sleep":
            time.sleep(float(value))
        if func == "clear":
            clear()
        continue
    print(result)