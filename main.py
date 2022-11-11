import os
import subprocess
import sys
import time

CURRENT_DIRECTORY = None
DISPLAY_DIRECTORY = True
SEPARATOR = ">"
COMMANDS = None
CODE_SEPARATOR = "##"

CURVED_ARROW = "⤷"
SINGLE_SPACE = "  "

class COLORS:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    WHITE = '\033[37m'
    GREY = '\033[90m'
    ORANGE = '\033[33m'

"""
COMMAND UTILITIES
"""

def directory():
    if DISPLAY_DIRECTORY is False:
        return "cases"
    else:
        return CURRENT_DIRECTORY

def get_directory_elements():
    
    files_folders = os.listdir(CURRENT_DIRECTORY)

    files = []
    folders = []

    for element in files_folders:
        if (os.path.isfile(os.path.join(CURRENT_DIRECTORY, element))):
            files.append(element)
        else:
            folders.append(element)

    return [files, folders]

def get_files():
    return get_directory_elements()[0]

def get_folders():
    return get_directory_elements()[1]


def choose_test_file(filename):
    
    files = list(filter(lambda s: ".txt" in s, get_files()))
    print("\n{space}{white}[-]{grey} Choose a test file among the ones here:".format(space=SINGLE_SPACE, white=COLORS.WHITE, grey=COLORS.GREY))
    
    for index, file in enumerate(files):
        print("{space}{space}{white}{arrow} {0}{grey}: {1}".format(index + 1, file, space=SINGLE_SPACE, arrow=CURVED_ARROW, white=COLORS.WHITE, grey=COLORS.GREY))
    
    response = input("{space}{white}[-] {grey}Choice: {white}".format(space=SINGLE_SPACE, white=COLORS.WHITE, grey=COLORS.GREY))
    print(end="\n")
    
    return files[int(response) - 1]


def run_file(file, language, to_input):

    if language == "cpp":
        result = subprocess.run(["./" + file], capture_output=True, input=(to_input + "\n").encode("UTF-8"))
        value = str(result.stdout.decode("UTF-8"))[:-1]
    
    

    return value


"""
CONSOLE HANDLING
"""

def console_start():
    global CURRENT_DIRECTORY
    CURRENT_DIRECTORY = os.getcwd()
    print("Automatic Test Cases Checker", end="\n\n")


def req():
    print("{col1}{bold}{0}{white}{1}{nobold} ".format(directory(), SEPARATOR, col1=COLORS.OKBLUE, bold=COLORS.BOLD, white=COLORS.WHITE, nobold=COLORS.ENDC), end="")
    return input()

def process(req):

    command = req.split()[0]
    if len(req.split()) != 0:
        args = req.split()[1:]
    else:
        args = []

    if command not in COMMANDS.keys():
        print('Unknown command')
    else:
        COMMANDS[command](args)
    
    print("")


"""
ACTUAL COMMANDS
"""


def dirhid(args):
    global DISPLAY_DIRECTORY
    DISPLAY_DIRECTORY = False

def dirshow(args):
    global DISPLAY_DIRECTORY
    DISPLAY_DIRECTORY = True

def dir(args):
    elements = get_directory_elements()
    print(" ".join(elements[0]), end=" ")
    print(" ".join(list(map(lambda s: "/" + s, elements[1]))))

def cd(args):

    global CURRENT_DIRECTORY

    if len(args) == 0:
        print(CURRENT_DIRECTORY)
        return
    
    folders = get_folders()
    target_directory = args[0].replace("/", "")
    
    if target_directory in folders:
        CURRENT_DIRECTORY += "/" + target_directory
    elif target_directory == "..":
        CURRENT_DIRECTORY = "/".join(CURRENT_DIRECTORY.split("/")[:-1])
    else:
        print("Cannot access directory")


def test_cases(args):

    # Basic checks
    if len(args) < 2:
        print("Not enough arguments")
        return

    # Extract data
    language = args[0]
    file = args[1]

    # Reformat
    if "." + language not in file:
        file += "." + language 

    # For clarity
    complete_path = CURRENT_DIRECTORY + "/" + file
    
    # Ask file, and get content
    test_file = choose_test_file(file)

    with open(CURRENT_DIRECTORY + "/" + test_file, "r") as f:
        content = "".join(f.readlines())

    content = list(filter(lambda x: x != "" and x != "\n", content.split(CODE_SEPARATOR)))
    content = list(map(lambda x: x[:-1], content))

    name = []
    to_give = []
    expected = []

    for index, element in enumerate(content):
        if index % 3 == 0:
            name.append(element.replace("\n", ""))
        elif index % 3 == 1:
            to_give.append(element)
        else:
            expected.append(element.replace("\n", ""))

    # Precompile programs if necessary
    was_compiled = language in ["cpp"]

    if language == "cpp":
        res = subprocess.run(["g++", complete_path, "-o", file])
        
    print("{space}{white}[{green}+{white}] {grey}Compilation {green}successful{white}\n".format(space=SINGLE_SPACE, white=COLORS.WHITE, grey=COLORS.GREY, green=COLORS.OKGREEN))
    
    print("{space}{white}[+]{grey}Running {green}{0} {grey}tests".format(len(name), space=SINGLE_SPACE, white=COLORS.WHITE, grey=COLORS.GREY, green=COLORS.OKGREEN))

    # Additional variables
    test_cases_number = len(name)
    success_cases = 0

    # Running each test case
    for i in range(len(name)):
        
        print("{space}{space}{grey}{arrow} {white}#{0}{grey}: Provided value for test '{grey}{1}{grey}', testing...".format(i + 1, name[i], space=SINGLE_SPACE, arrow=CURVED_ARROW, white=COLORS.WHITE, grey=COLORS.GREY))
        starting_time = time.time()
        value = run_file(file, language, to_give[i])
        
        print("{space}{space}  ".format(space=SINGLE_SPACE), end="")

        if value == expected[i]:
            print("{green}Test passed, {grey}obtained {green}{0}{grey}.".format(value, green=COLORS.OKGREEN, grey=COLORS.GREY), end="")
            success_cases += 1
        else:
            print("{red}Test Failed, {grey}obtained {red}{0} {grey}≠ {green}{1}{grey}.".format(value, expected[i], red=COLORS.FAIL, grey=COLORS.GREY, green=COLORS.OKGREEN), end="")

        print(" [Runtime: {0}s]".format(round(time.time() - starting_time, 3)))

    output_color = COLORS.OKGREEN
    if 2 * success_cases <= test_cases_number:
        output_color = COLORS.FAIL
    elif success_cases < test_cases_number:
        output_color = COLORS.ORANGE

    print("\n{space}{white}[-]{grey} Ran {white}{0}{grey} tests, with {green}{1}{grey} tests passed. {white}({col}{2}%{white})".format(test_cases_number, success_cases, round(success_cases / test_cases_number * 100), space=SINGLE_SPACE, grey=COLORS.GREY, white=COLORS.WHITE, green=COLORS.OKGREEN, col=output_color))

if __name__ == "__main__":

    COMMANDS = {
        "dirhid": lambda args: dirhid(args),
        "dirshow": lambda args: dirshow(args),
        "dir": lambda args: dir(args),
        "ls": lambda args: dir(args), 
        "cd": lambda args: cd(args),
        "test": lambda args: test_cases(args),
    }
    
    console_start()
    
    while True:
        response = req()
        process(response)
    