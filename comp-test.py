#!/usr/bin/env python3

import os
import sys

import subprocess
import time
import random

current_directory = os.getcwd()

""" DISPLAY HELPERS """

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

class FailedCompilation(Exception):
    pass


class Program():
    
    def __init__(self, filename: str):
        self.filename = filename
        self.language = Language(filename.split(".")[-1])
        self.compiled = not self.language.need_compilation

    def __repr__(self) -> str:
        return f"(File: {self.filename} / Language: {self.language.name} / Compiled: {self.compiled})"

    def __str__(self) -> str:
        return self.__repr__()

    def compile(self):
        if self.compiled is True:
            return self.compiled
        
        complete_path_in = current_directory + "/" + self.filename
        complete_path_out = current_directory + "/" + self.filename.replace(".", "_")
        
        if not self.language.need_compilation:
            return True            
        
        if self.language.extension == "cpp":
            output = subprocess.run(["g++", complete_path_in, "-o", complete_path_out], capture_output=True)
        elif self.language.extension == "c":
            output = subprocess.run(["gcc", complete_path_in, "-o", complete_path_out], capture_output=True)
        
        if output.stderr == b'':
            return True
        
        raise FailedCompilation(f"Error while compiling: {output.stderr}")
    
    def run(self, input):
        
        
        
        


class Language():
    
    def __init__(self, extension: str):
        self.name = LANGUAGE_ASSOCIATIONS[extension]["name"]
        self.extension = extension
        self.need_compilation = LANGUAGE_ASSOCIATIONS[extension]["compiled"]
    
    def __repr__(self) -> str:
        return f"<{self.name} language>"

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
            print(f"{Colors.red}WARNING: {Colors.white}Comparator not coded in python are not supported yet.")

    def __repr__(self) -> str:
        return f"(Compare container: {self.generator})"

    def __str__(self) -> str:
        return self.__repr__()
    
    def generate_container(self):
        
        

class Execution():

    def __init__(self, _program_list: list[Program], _testing_object: TestContainer, confident: Program = None):
        self.program_list = _program_list
        self.testing_object = _testing_object
        self.confident_program = confident



    




if __name__ == "__main__":

    main = Program("main.py")
    print(main)

    generator = CompareContainer("gen.py")
    print(generator)
    
    program = Program("proge.cpp")
    print(program)
    
    g = CompareContainer("prog.cpp")
    
    
    
    