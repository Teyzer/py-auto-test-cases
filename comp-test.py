#!/usr/bin/env python3

import os
import sys

import subprocess
import time
import random

current_directory = os.getcwd()

""" DISPLAY HELPERS """

class Symbols:
    class Squares:
        white = "⬜"
        green = "🟩"
        red = "🟥"
        black = "⬛"
    curved_arrow = "⤷"


class Colors:
    blue = '\033[94m'
    cyan = '\033[96m'
    green = '\033[92m'
    warning = '\033[93m'
    red = '\033[91m'
    endc = '\033[0m'
    bold = '\033[1m'
    underline = '\033[4m'
    white = '\033[37m'
    grey = '\033[90m'
    orange = '\033[33m'


""" GENERAL SETTINGS """

LANGUAGE_ASSOCIATIONS = {
    "py": {"name": "python", "compiled": False},
    "cpp": {"name": "C++", "compiled": True},
    "c": {"name": "C", "compiled": True},
    "ml": {"name": "Ocaml", "compiled": True}
}

""" GENERAL CLASSES """

def format_output(text: str, characters: int = 40):
    
    if text[-1] == '\n':
        text = text[:-1]

    lines = text.split('\n')
    line = lines[0][:characters]

    if line != text:
        line += ".."

    return line


class FailedCompilation(Exception):
    pass


class Program():
    
    def __init__(self, filename: str):
        self.filename = filename
        self.language = Language(filename.split(".")[-1])
        self.compiled = not self.language.need_compilation

    def __repr__(self) -> str:
        return f"({Colors.cyan}[Program]{Colors.grey} File: {self.filename} / Language: {self.language.name} / Compiled: {self.compiled})"

    def __str__(self) -> str:
        return self.__repr__()

    def compile(self) -> bool:

        if self.compiled is True or not self.language.need_compilation:
            return True
        
        complete_path_in = current_directory + "/" + self.filename
        complete_path_out = current_directory + "/" + self.filename.replace(".", "_")   
        
        if self.language.extension == "cpp":
            output = subprocess.run(["g++", complete_path_in, "-o", complete_path_out], capture_output=True)
        elif self.language.extension == "c":
            output = subprocess.run(["gcc", complete_path_in, "-o", complete_path_out], capture_output=True)
        
        if output.stderr == b'':
            self.compiled = True
            return True
        
        raise FailedCompilation(f"{Colors.red}Compilation error{Colors.grey}: {output.stderr}")
    

    def run(self, program_input: str = None, timeout_delay: int = 0.5) -> bool:

        if program_input is None:
            program_input = ""

        if program_input != '' and program_input[-1] != '\n':
            program_input = program_input + '\n'

        if not self.compiled:
            self.compile()

        executable_path = current_directory + "/" + self.filename.replace(".", "_")
        if self.language.extension in ["py"]:
            executable_path = current_directory + "/" + self.filename

        if self.language.extension == "py":
            command_line = ["python3", executable_path]
        elif self.language.extension == "cpp":
            command_line = [executable_path]
        elif self.language.extension == "c":
            command_line = [executable_path]
        
        try:
            result = subprocess.run(command_line, capture_output=True, check=False, input=(program_input + "\n").encode("UTF-8"), timeout=timeout_delay)
            if result.stderr != b'':
                print(f"{Colors.red}: Program {Colors.cyan}{self.filename} {Colors.grey}crashed")
            value = str(result.stdout.decode("utf-8"))
        except subprocess.TimeoutExpired:
            value = "TIMEOUT"

        if value[-1] != '\n': # Careful
            value += '\n'

        return value        


class Language():
    
    def __init__(self, extension: str):
        self.name = LANGUAGE_ASSOCIATIONS[extension]["name"]
        self.extension = extension
        self.need_compilation = LANGUAGE_ASSOCIATIONS[extension]["compiled"]
    
    def __repr__(self) -> str:
        return f"({Colors.cyan}[Language] {Colors.grey}{self.name})"

    def __str__(self) -> str:
        return self.__repr__()


class TestContainer():

    def __init__(self, filename: str):
        self.test_file = filename

    def __repr__(self) -> str:
        return f"(Test container: {self.test_file})"

    def __str__(self) -> str:
        return self.__repr__()

class CompareContainer():

    def __init__(self, filename: str):
        
        self.generator = Program(filename)
        if self.generator.language.extension != "py":
            print(f"{Colors.red}WARNING: {Colors.grey}Comparator not coded in python are not supported yet.")

    def __repr__(self) -> str:
        return f"({Colors.cyan}[Compare container] {Colors.grey}{self.generator})"

    def __str__(self) -> str:
        return self.__repr__()
    
    def create_test(self):
        return self.generator.run()
        

class Execution():

    def __init__(self, _program_list: list[Program], _testing_object: TestContainer, confident: Program = None):
        self.program_list = _program_list
        self.testing_object = _testing_object
        self.confident_program = confident

    def submit(self):
        pass



    




if __name__ == "__main__":

    print(f"{Colors.grey}", end="")

    main = Program("main.py")
    #print(main)

    generator = CompareContainer("gen7.py")
    #print(generator)
    

    program = Program("prog.cpp")
    #print(program)
    
    q = generator.create_test()
    z = program.run(q, 0.2)
    
    