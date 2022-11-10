import os
import subprocess
import sys
import time

CURRENT_DIRECTORY = None
DISPLAY_DIRECTORY = True
SEPARATOR = ">"
COMMANDS = None
CODE_SEPARATOR = "##"

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
    files = list(filter(lambda s: s.startswith(filename.split(".")[0] + "_test"), get_files()))
    print("Choose a test file among the ones here:")
    for index, file in enumerate(files):
        print("{0}: {1}".format(index + 1, file))
    response = input("Choice: ")
    print(end="\n")
    return files[int(response) - 1]


"""
CONSOLE HANDLING
"""

def console_start():
    global CURRENT_DIRECTORY
    CURRENT_DIRECTORY = os.getcwd()
    print("Automatic Test Cases Checker", end="\n\n")


def req():
    print("{0}{1} ".format(directory(), SEPARATOR), end="")
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

    if len(args) < 2:
        print("Not enough arguments")
        return

    language = args[0]
    file = args[1]

    if language == "cpp":

        if ".cpp" not in file:
            file += ".cpp"
        
        subprocess.run(["g++", file, "-o", "to_run"])
        print("Compilation successful", end="\n\n")

        test_file = choose_test_file(file)

        with open(CURRENT_DIRECTORY + "/" + test_file, "r") as f:
            content = "".join(f.readlines())

        content = list(filter(lambda x: x != "" and x != "\n", content.split(CODE_SEPARATOR)))
        content = list(map(lambda x: x[:-1], content))
        #print(content)

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

        #print(name, to_give, expected)

        print("Running {0} tests".format(len(name)))

        for i in range(len(name)):
            print("Test #{0} - '{1}': ".format(i + 1, name[i]), end="")
            starting_time = time.time()
            result = subprocess.run(["./to_run"], capture_output=True, input=(to_give[i] + "\n").encode("UTF-8"))
            value = str(result.stdout.decode("UTF-8"))[:-1]
            if value == expected[i]:
                print("Succeeded", end="")
            else:
                print("Comme Mael, {0} != {1}".format(value, expected[i]), end="")
            print(" [{0}s]".format(round(time.time() - starting_time, 6)))



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
    