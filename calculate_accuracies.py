def main():
	file_names = [
		'algebra__polynomial_roots_decoded.transformer.transformer_tpu.algorithmic_math_deepmind_all.beam4.alpha0.6',
		'arithmetic__mixed_data.transformer.transformer_tpu.algorithmic_math_deepmind_all.beam4.alpha0.6',
		'numbers__div_remainder_data.transformer.transformer_tpu.algorithmic_math_deepmind_all.beam4.alpha0.6',
		'polynomials__evaluate_data.transformer.transformer_tpu.algorithmic_math_deepmind_all.beam4.alpha0.6',
		'polynomials__simplify_power_data.transformer.transformer_tpu.algorithmic_math_deepmind_all.beam4.alpha0.6'
	]

	for file_name in file_names:
		with open(file_name+'.decodes') as predictions_file:
			with open(file_name+'.targets') as targets_file:
				correct = 0
				n = 0
				
				prediction = predictions_file.readline()
				target = targets_file.readline()

				while prediction:
					n += 1
					if prediction == target:
						correct += 1
					prediction = predictions_file.readline()
					target = targets_file.readline()
				print('Accuracy for {}: \n{}\n\n'.format(file_name, correct/n))


if __name__ == '__main__':
	main()