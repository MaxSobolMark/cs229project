import argparse
import re # Regex for finding numbers
import os

from Naked.toolshed.shell import muterun_js

SEPARATOR_CHAR = '||' # Signaling where a step ends and another begins

def main(original_dataset_directory, steps_dataset_directory, train_modes, start_index, end_index):
	# Preprocess paths
	original_dataset_directory = os.path.abspath(original_dataset_directory)
	steps_dataset_directory = os.path.abspath(steps_dataset_directory)

	print(original_dataset_directory, steps_dataset_directory, train_modes)
	for mode in train_modes:
		print('Generating {}\n'.format(mode))
		generate_numbers_div_remainder(original_dataset_directory, steps_dataset_directory, mode)
		print('\tnumbers_div_remainder successful')
		generate_polynomials_evaluate(original_dataset_directory, steps_dataset_directory, mode)
		print('\tpolynomials_evaluate successful')
		generate_arithmetic_mixed(original_dataset_directory, steps_dataset_directory, mode, start_index, end_index)
		print('\tarithmetic_mixed successful')
		generate_polynomials_simplify_power(original_dataset_directory, steps_dataset_directory, mode, start_index, end_index)
		print('\tpolynomails_simplify_power successful')




def generate_numbers_div_remainder(original_dataset_directory, steps_dataset_directory, mode):
	if mode is not 'extrapolate': # extrapolate is the only mode not supported by the original dataset
		task_path = os.path.join(original_dataset_directory, mode, 'numbers__div_remainder.txt')
		write_path = os.path.join(steps_dataset_directory, mode, 'numbers__div_remainder.txt')
		if os.path.exists(write_path):
			print('TASK ALREADY EXISTS: {}/numbers__div_remainder.txt\tIf you want to generate it again please erase the file :)'.format(mode))
			return

		# Create steps dataset directory if it doesn't exist
		write_directory = os.path.dirname(write_path)
		if not os.path.exists(write_directory):
			os.makedirs(write_directory)
		
		with open(task_path) as task_file:
			with open(write_path, 'a') as write_file:
				question = task_file.readline()
				while question:
					answer = task_file.readline()
					dividend, divisor = re.findall('\d+', question)
					dividend = int(dividend)
					divisor = int(divisor)
					new_answer = str(dividend / divisor) + SEPARATOR_CHAR + str(dividend % divisor)
					write_file.write(question + new_answer + '\n')
					question = task_file.readline()


def generate_polynomials_evaluate(original_dataset_directory, steps_dataset_directory, mode):
	# Example question: Let m(k) = -44*k**2 - 3513*k - 6359. What is m(-78)?
	if mode is not 'extrapolate': # extrapolate is the only mode not supported by the original dataset
		task_path = os.path.join(original_dataset_directory, mode, 'polynomials__evaluate.txt')
		write_path = os.path.join(steps_dataset_directory, mode, 'polynomials__evaluate.txt')
		if os.path.exists(write_path):
			print('TASK ALREADY EXISTS: {}/polynomials__evaluate.txt\tIf you want to generate it again please erase the file :)'.format(mode))
			return

		# Create steps dataset directory if it doesn't exist
		write_directory = os.path.dirname(write_path)
		if not os.path.exists(write_directory):
			os.makedirs(write_directory)
		
		with open(task_path) as task_file:
			with open(write_path, 'a') as write_file:
				question = task_file.readline()
				while question:
					answer = task_file.readline()
					# Get the polynomial part
					polynomial = question.split('=')[1].split('.')[0]
					terms = polynomial.split()

					variable = '(' + question.split('(')[-1].split(')')[0] + ')'

					# Replace variable in terms
					for index, term in enumerate(terms):
						terms[index] = ''.join([char if not char.isalpha() else variable for char in term])

					terms = [str(eval(term)) if len(term) > 1 else term for term in terms]

					new_answer = ''.join(terms) + SEPARATOR_CHAR + answer
					write_file.write(question + new_answer + '\n')
					question = task_file.readline()

def generate_arithmetic_mixed(original_dataset_directory, steps_dataset_directory, mode, start_index, end_index):
	# Example question: Simplify (t*t/(t**(-3/8)*t*t))**(1/3)/(t**16)**(-9) assuming t is positive.
	if mode is not 'extrapolate': # extrapolate is the only mode not supported by the original dataset
		task_path = os.path.join(original_dataset_directory, mode, 'arithmetic__mixed.txt')
		write_path = os.path.join(steps_dataset_directory, mode, 'arithmetic__mixed.txt')
		if os.path.exists(write_path):
			print('TASK ALREADY EXISTS: {}/arithmetic__mixed.txt\tIf you want to generate it again please erase the file :)'.format(mode))
			return

		# Create steps dataset directory if it doesn't exist
		write_directory = os.path.dirname(write_path)
		if not os.path.exists(write_directory):
			os.makedirs(write_directory)
		
		with open(task_path) as task_file:
			with open(write_path, 'a') as write_file:
				# Skip to the start_index
				# There are two lines for each training sample (question and answer)
				for _ in range(start_index * 2):
					task_file.readline()
				
				i = start_index

				question = task_file.readline()
				while question and i <= end_index:
					print('started question')
					answer = task_file.readline()
					# Get the numbers part
					polynomial = re.sub(r"[a-zA-Z]+", '', question).replace(' ', '').replace('.', '').replace('?', '')
					#print('polynomial: {}'.format(polynomial))
					
					# Call mathsteps
					response = muterun_js('mathsteps.js', polynomial)
					if response.exitcode is not 0:
						print('ERROR WITH INTERFACING WITH MATHSTEPS: ', response.stderr)
						return
					new_answer = response.stdout.decode("utf-8").replace('\n', SEPARATOR_CHAR)

					write_file.write(question + new_answer + '\n')
					question = task_file.readline()
					i += 1

def generate_polynomials_simplify_power(original_dataset_directory, steps_dataset_directory, mode, start_index, end_index):
	# Example question: Simplify (t*t/(t**(-3/8)*t*t))**(1/3)/(t**16)**(-9) assuming t is positive.
	if mode is not 'extrapolate': # extrapolate is the only mode not supported by the original dataset
		task_path = os.path.join(original_dataset_directory, mode, 'polynomials__simplify_power.txt')
		write_path = os.path.join(steps_dataset_directory, mode, 'polynomials__simplify_power.txt')
		if os.path.exists(write_path):
			print('TASK ALREADY EXISTS: {}/polynomials__simplify_power.txt\tIf you want to generate it again please erase the file :)'.format(mode))
			return

		# Create steps dataset directory if it doesn't exist
		write_directory = os.path.dirname(write_path)
		if not os.path.exists(write_directory):
			os.makedirs(write_directory)
		
		with open(task_path) as task_file:
			with open(write_path, 'a') as write_file:
				for _ in range(start_index * 2):
					task_file.readline()
				
				i = start_index

				question = task_file.readline()
				while question and i <= end_index:
					print('started question')
					answer = task_file.readline()
					# Get the polynomial part
					prefix = 'Simplify '
					suffix = ' assuming x is positive.'
					polynomial = question[len(prefix) : -len(suffix)]
					
					# Call mathsteps
					response = muterun_js('mathsteps.js', polynomial)
					if response.exitcode is not 0:
						print('ERROR WITH INTERFACING WITH MATHSTEPS: ', response.stderr)
						return
					new_answer = response.stdout.decode("utf-8").replace('\n', SEPARATOR_CHAR)

					write_file.write(question + new_answer + '\n')
					question = task_file.readline()

					i += 1



if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('original_dataset_directory', nargs='?', type=str,
						help='The directory in which the math dataset is located.')
	parser.add_argument('steps_dataset_directory', nargs='?', type=str,
						help='The directory in which the modified dataset will be written.')
	parser.add_argument('train_modes', nargs='+', type=str,
						help='List every mode to generate. Options: extrapolate, interpolate, train-easy, train-medium, train-hard')
	parser.add_argument('start_index', type=int,
						help='Index to start generating the dataset')
	parser.add_argument('end_index', type=int,
						help='Index to stop generating the dataset')
	args = parser.parse_args()
	main(args.original_dataset_directory, args.steps_dataset_directory, args.train_modes, int(args.start_index), int(args.end_index))