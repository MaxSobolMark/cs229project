import argparse
import re # Regex for finding numbers
import os

SEPARATOR_CHAR = '||' # Signaling where a step ends and another begins

def main(original_dataset_directory, steps_dataset_directory, train_modes):
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



if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('original_dataset_directory', nargs='?', type=str,
						help='The directory in which the math dataset is located.')
	parser.add_argument('steps_dataset_directory', nargs='?', type=str,
						help='The directory in which the modified dataset will be written.')
	parser.add_argument('train_modes', nargs='+', type=str,
						help='List every mode to generate. Options: extrapolate, interpolate, train-easy, train-medium, train-hard')
	args = parser.parse_args()
	main(args.original_dataset_directory, args.steps_dataset_directory, args.train_modes)