#!/usr/bin/env python3

import os
import subprocess
import sys
import time
import random

CURRENT_DIRECTORY = None
DISPLAY_DIRECTORY = True
LAST_USED_COMMAND = None
LAST_USED_COMMAND_ARGS = None
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

def choose_random_generator():

	files = list(filter(lambda s: (".py" in s) and ("gen" in s), get_files()))
	print("\n{space}{white}[-]{grey} Choose a random test generator among the ones here:".format(space=SINGLE_SPACE, white=COLORS.WHITE, grey=COLORS.GREY))
	
	for index, file in enumerate(files):
		print("{space}{space}{white}{arrow} {0}{grey}: {1}".format(index + 1, file, space=SINGLE_SPACE, arrow=CURVED_ARROW, white=COLORS.WHITE, grey=COLORS.GREY))
	
	response = input("{space}{white}[-] {grey}Choice: {white}".format(space=SINGLE_SPACE, white=COLORS.WHITE, grey=COLORS.GREY))
	print(end="\n")
	
	return files[int(response) - 1]

def ask_compare_inputs():

	print("{space}{white}[-]{grey} Choose a number of test:".format(space=SINGLE_SPACE, white=COLORS.WHITE, grey=COLORS.GREY))
	test_number = int(input("{space}{white}[-] {grey}Choice: {white}".format(space=SINGLE_SPACE, white=COLORS.WHITE, grey=COLORS.GREY)))
	print(end="\n")
	
	return [test_number]

def compile_file(file):
	
	#print(file)
	
	filename = file.split(".")[0]
	language = file.split(".")[-1]
	complete_path = CURRENT_DIRECTORY + "/" + file
	
	#print(filename, language)

	if language == "py":
		pass
	elif language == "cpp":
		res = subprocess.run(["g++", complete_path, "-o", CURRENT_DIRECTORY + "/" + ".".join(file.split(".")[:-1])])
	elif language == "c" :
		res = subprocess.run(["gcc", complete_path, "-o", CURRENT_DIRECTORY + "/" + ".".join(file.split(".")[:-1])])
	elif language == "ml" :
		res = subprocess.run(["ocamlopt", complete_path, "-o", CURRENT_DIRECTORY + "/" + ".".join(file.split(".")[:-1])])


def uncompile_file(file):

	filename = file.split(".")[0]
	language = file.split(".")[-1]
	complete_path = CURRENT_DIRECTORY + "/" + file

	if language == "cpp" or language == "c" :
		os.remove(CURRENT_DIRECTORY + "/" + ".".join(file.split(".")[:-1]))
	elif language == "ml" :
		os.remove(CURRENT_DIRECTORY + "/" + ".".join(file.split(".")[:-1]))
		os.remove(CURRENT_DIRECTORY + "/" + ".".join(file.split(".")[:-1]) + ".cmx")
		os.remove(CURRENT_DIRECTORY + "/" + ".".join(file.split(".")[:-1]) + ".cmi")
		os.remove(CURRENT_DIRECTORY + "/" + ".".join(file.split(".")[:-1]) + ".o")


def run_file(file, language, to_input, timeout_time=10):

	#print(file, language, to_input)

	new_input = str(to_input).splitlines()
	if '' in new_input:
		new_input.remove('')
	new_input = '\n'.join(new_input)

	if language == "cpp":
		try:
			result = subprocess.run([CURRENT_DIRECTORY + "/" + ".".join(file.split(".")[:-1])], capture_output=True, input=(to_input + "\n").encode("UTF-8"), timeout=timeout_time)
			value = str(result.stdout.decode("UTF-8"))[:-1]
		except subprocess.TimeoutExpired:
			value = "TIMEOUT"

	if language == "c" :
		try:
			result = subprocess.run([CURRENT_DIRECTORY + "/" + ".".join(file.split(".")[:-1])], capture_output=True, input=(to_input + "\n").encode("UTF-8"), timeout=timeout_time)
			value = str(result.stdout.decode("UTF-8"))[:-1]
		except subprocess.TimeoutExpired:
			value = "TIMEOUT"

	if language == "ml" :
		try:
			result = subprocess.run([CURRENT_DIRECTORY + "/" + ".".join(file.split(".")[:-1])], capture_output=True, check=False, input=(new_input + "\n").encode("UTF-8"), timeout=timeout_time)
			try:
				result.check_returncode()
				value = str(result.stdout.decode("UTF-8"))[:-1]
			except subprocess.CalledProcessError:
				value = str(result.stdout.decode("UTF-8"))[:-1] + '\n' + str(result.stderr.decode("UTF-8"))[:-1]
				
		except subprocess.TimeoutExpired:
			value = "TIMEOUT"

	if language == "py":
		try:
			p = subprocess.Popen(["python3", CURRENT_DIRECTORY + "/" + file], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
			value = "\n".join(p.communicate(input=(new_input + "\n").encode("UTF-8"), timeout=timeout_time)[0].decode("UTF-8").split("\n")[:-1])
		except subprocess.TimeoutExpired:
			value = "TIMEOUT"

	return value


def create_write_test_file():

	q = random.randint(0, 100000000)

	with open(CURRENT_DIRECTORY + "/" + "write_test{0}.txt".format(str(q)), "x") as f:
		pass

	return "write_test{0}.txt".format(str(q))


def write_test_in_file(filename, name, test, awaited="None"):
	
	with open(CURRENT_DIRECTORY + "/" + filename, "a") as f:
		f.write("####\n{0}\n##\n{1}\n##\n{2}\n".format(name, test, awaited))



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
	global LAST_USED_COMMAND
	global LAST_USED_COMMAND_ARGS

	command = req.split()[0]
	if len(req.split()) != 0:
		args = req.split()[1:]
	else:
		args = []

	if command == "!":
		COMMANDS[LAST_USED_COMMAND](LAST_USED_COMMAND_ARGS)

	if command not in COMMANDS.keys():
		print('Unknown command')
	else:
		LAST_USED_COMMAND = command
		LAST_USED_COMMAND_ARGS = args
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

def compare_scripts(args):

	if len(args) < 1:
		print("Not enough arguments")
		return

	files = args[0].split(":")

	if len(files) == 1:
		print("No use of comparing one script")
		return

	number_of_files = len(files)

	for file in files:
		filename = file.split(".")[0]
		language = file.split(".")[1]
		compile_file(file)
	
	random_generator = choose_random_generator()
	a_random_test = lambda: run_file(random_generator, "py", "")

	specs = ask_compare_inputs()
	number_of_tests = specs[0]

	max_char_allowed_per_row = 20
	digit_precision = 5

	timeout_count = []
	none_count = []
	different_count = []

	writing_file = create_write_test_file()

	for i in range(number_of_files):
		timeout_count.append(0)
		none_count.append(0)
		different_count.append(0)


	# Configure first row of print
	print("{grey}{space}{space}+----------+".format(grey=COLORS.GREY, space=SINGLE_SPACE), end="")
	for i in range(number_of_files):
		print("-" * max_char_allowed_per_row + "+", end="")
	print(end="\n")
	
	# Actual compute
	for i in range(number_of_tests):
		
		times = []
		results = []

		test_to_give = a_random_test()
		write_test_in_file(writing_file, "Test #{0}".format(i + 1), test_to_give)

		for script in files:

			script_name = script.split(".")[0]
			script_language = script.split(".")[1]
			
			start = time.time()

			temp_result = run_file(script_name + "." + script_language, script_language, test_to_give, timeout_time=0.5)
			results.append(temp_result)

			#print(temp_result)

			times.append(time.time() - start)

		most_common = None

		#print(results, test_to_give)

		for result in results:
			if 2 * results.count(result) >= len(results):
				most_common = result
				break

		# output results
		print("{space}{space}| Ouputs  #{0} |".format(str(i + 1) + " "*(len(str(number_of_tests)) - len(str(i+1))), space=SINGLE_SPACE), end="")
		for j in range(len(files)):

			display_color = COLORS.ORANGE

			res = results[j]

			if res == "TIMEOUT":
				timeout_count[j] += 1
			elif res == "":
				none_count[j] += 1
			elif res != most_common:
				different_count[j] += 1

			if res == "" or (res != most_common and most_common is not None) or res == "TIMEOUT":
				display_color = COLORS.FAIL
			elif res == most_common:
				display_color = COLORS.OKGREEN

			if res == "":
				res = "None"

			res_len = len(res)

			print(" {col}".format(col=display_color) + res + (" " * abs(max_char_allowed_per_row - res_len - 1)) + "{grey}|".format(grey=COLORS.GREY), end="")

		print(end="\n")
		
		print("{space}{space}| Runtimes {0}|".format(" "*(len(str(number_of_tests)) + 1), space=SINGLE_SPACE), end="")
		for j in range(len(files)):

			res = str(round(times[j], digit_precision))
			res_len = len(res)

			print(" " + res + (" " * abs(max_char_allowed_per_row - res_len - 1)) + "|", end="")

		print(end="\n")

		print("{space}{space}+----------{0}+".format("-"*(len(str(number_of_tests)) + 1), space=SINGLE_SPACE), end="")
		for i in range(number_of_files):
			print("-" * max_char_allowed_per_row + "+", end="")
		print(end="\n")

	print(end="\n")

	print("{space}{space}+-------------+".format(space=SINGLE_SPACE), end="")
	for i in range(number_of_files):
		print("-" * max_char_allowed_per_row + "+", end="")
	print(end="\n")


	# Resultats ---------------------------
	print("{space}{space}| Results     |".format(space=SINGLE_SPACE), end="")
	for file in files:

		res = file.split(".")[0]
		res_len = len(res)

		print(" {white}".format(white=COLORS.WHITE) + res + (" " * abs(max_char_allowed_per_row - res_len - 1)) + "{grey}|".format(grey=COLORS.GREY), end="")
	print(end="\n")

	print("{space}{space}+-------------+".format(space=SINGLE_SPACE), end="")
	for i in range(number_of_files):
		print("-" * max_char_allowed_per_row + "+", end="")
	print(end="\n")

	print("{space}{space}| Crashed     |".format(space=SINGLE_SPACE), end="")
	for i in range(number_of_files):

		res = str(none_count[i]) + "/" + str(number_of_tests)
		res_len = len(res)

		print(" {white}".format(white=COLORS.WHITE) + res + (" " * abs(max_char_allowed_per_row - res_len - 1)) + "{grey}|".format(grey=COLORS.GREY), end="")
	print(end="\n")

	print("{space}{space}| Timeout     |".format(space=SINGLE_SPACE), end="")
	for i in range(number_of_files):

		res = str(timeout_count[i]) + "/" + str(number_of_tests)
		res_len = len(res)

		print(" {white}".format(white=COLORS.WHITE) + res + (" " * abs(max_char_allowed_per_row - res_len - 1)) + "{grey}|".format(grey=COLORS.GREY), end="")
	print(end="\n")

	print("{space}{space}| Diff        |".format(space=SINGLE_SPACE), end="")
	for i in range(number_of_files):

		res = str(different_count[i]) + "/" + str(number_of_tests)
		res_len = len(res)

		print(" {white}".format(white=COLORS.WHITE) + res + (" " * abs(max_char_allowed_per_row - res_len - 1)) + "{grey}|".format(grey=COLORS.GREY), end="")
	print(end="\n")

	print("{space}{space}| Success     |".format(space=SINGLE_SPACE), end="")
	for i in range(number_of_files):

		res = str(number_of_tests - different_count[i] - timeout_count[i] - none_count[i]) + "/" + str(number_of_tests)
		res_len = len(res)

		print(" {white}".format(white=COLORS.WHITE) + res + (" " * abs(max_char_allowed_per_row - res_len - 1)) + "{grey}|".format(grey=COLORS.GREY), end="")
	print(end="\n")
	
	print("{space}{space}+-------------+".format(space=SINGLE_SPACE), end="")
	for i in range(number_of_files):
		print("-" * max_char_allowed_per_row + "+", end="")
	print(end="\n")
	# Fin affichage resultats ------------------------

	print(end="\n")
	print("{space}{white}[+] {grey}Output in file: {white}{0}{grey}".format(writing_file, space=SINGLE_SPACE, white=COLORS.WHITE, grey=COLORS.GREY))
	print("{space}{white}[-] {grey}Save file ? (y/n): {white}".format(space=SINGLE_SPACE, white=COLORS.WHITE, grey=COLORS.GREY), end="")
	resp = input()

	if resp.lower() != "y":
		os.remove(CURRENT_DIRECTORY + "/" + writing_file)
		
	for fil in files:
		uncompile_file(fil)



def test_cases(args):

	# Basic checks
	if len(args) < 1:
		print("Not enough arguments")
		return

	# Extract data
	language = args[0].split(".")[1]
	file = args[0].split(".")[0]

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

	# Precompile
	compile_file(file)
		
	print("{space}{white}[{green}+{white}] {grey}Compilation {green}successful{white}\n".format(space=SINGLE_SPACE, white=COLORS.WHITE, grey=COLORS.GREY, green=COLORS.OKGREEN))
	
	print("{space}{white}[+]{grey}Running {green}{0} {grey}tests".format(len(name), space=SINGLE_SPACE, white=COLORS.WHITE, grey=COLORS.GREY, green=COLORS.OKGREEN))

	# Additional variables
	test_cases_number = len(name)
	success_cases = 0

	# Running each test case
	for i in range(len(name)):
		
		print("{space}{space}{grey}{arrow} {white}#{0}{grey}: Provided value for test '{grey}{1}{grey}', testing...".format(i + 1, name[i], space=SINGLE_SPACE, arrow=CURVED_ARROW, white=COLORS.WHITE, grey=COLORS.GREY))
		starting_time = time.time()
		value = run_file(file, language, to_give[i] )
		
		print("{space}{space}  ".format(space=SINGLE_SPACE), end="")

		if value == expected[i]:
			print("{green}Test passed, {grey}obtained {green}{0}{grey}.".format(value, green=COLORS.OKGREEN, grey=COLORS.GREY), end="")
			success_cases += 1
		else:
			print("{red}Test Failed, {grey}obtained {red}{0} {grey}â‰  {green}{1}{grey}.".format(value, expected[i], red=COLORS.FAIL, grey=COLORS.GREY, green=COLORS.OKGREEN), end="")

		print(" [Runtime: {0}s]".format(round(time.time() - starting_time, 3)))

	output_color = COLORS.OKGREEN
	if 2 * success_cases <= test_cases_number:
		output_color = COLORS.FAIL
	elif success_cases < test_cases_number:
		output_color = COLORS.ORANGE

	print("\n{space}{white}[-]{grey} Ran {white}{0}{grey} tests, with {green}{1}{grey} tests passed. {white}({col}{2}%{white})".format(test_cases_number, success_cases, round(success_cases / test_cases_number * 100), space=SINGLE_SPACE, grey=COLORS.GREY, white=COLORS.WHITE, green=COLORS.OKGREEN, col=output_color))

	uncompile_file(file)

if __name__ == "__main__":

	COMMANDS = {
		"dirhid": lambda args: dirhid(args),
		"dirshow": lambda args: dirshow(args),
		"dir": lambda args: dir(args),
		"ls": lambda args: dir(args), 
		"cd": lambda args: cd(args),
		"test": lambda args: test_cases(args),
		"compare": lambda args: compare_scripts(args),
	}
	
	console_start()

	if "compare" in sys.argv:
		process("compare {0}".format(sys.argv[2]))
	else:
		while True:
			response = req()
			process(response)
