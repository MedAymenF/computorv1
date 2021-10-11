#!/usr/bin/env python3

import sys


def		split_equation(equation):
	split_equation = equation.split('=')
	if (len(split_equation) != 2):
		print("Entry not well formatted")
		exit(1)
	left_side = split_equation[0].strip().replace(' * ', '*').replace('+ ', '+').replace('- ', '-')
	right_side = split_equation[1].strip().replace(' * ', '*').replace('+ ', '+').replace('- ', '-')
	return left_side, right_side


def		split_term(term):
	split_term = term.split('*')
	if (len(split_term) != 2):
		print("Entry not well formatted")
		exit(1)
	try:
		coeff = float(split_term[0])
	except Exception as e:
		print("Coefficient not a float")
		exit(1)
	if (split_term[1][:2] != 'X^'):
		print("Entry not well formatted")
		exit(1)
	try:
		power = int(split_term[1][2:])
	except Exception as e:
		print("Power not an integer")
		exit(1)
	return power, coeff


def		get_coefficients(expression):
	reduced_form = []
	count = 0
	for term in expression.split():
		power, coeff = split_term(term)
		if (power != count):
			print("Terms are not organized")
			exit(1)
		reduced_form.append(coeff)
		count = count + 1
	if (not count):
		print("Entry not well formatted")
		exit(1)
	return reduced_form


def     get_reduced_form(equation):
	left_side, right_side = split_equation(equation)
	if (not left_side or not right_side):
		print("Entry not well formatted")
		exit(1)
	left_reduced_form = get_coefficients(left_side)
	right_reduced_form = get_coefficients(right_side)
	reduced_form = []
	for i in range(max(len(left_reduced_form), len(right_reduced_form))):
		left_coeff = left_reduced_form[i] if i < len(left_reduced_form) else 0
		right_coeff = right_reduced_form[i] if i < len(right_reduced_form) else 0
		reduced_form.append(left_coeff - right_coeff)
	while (reduced_form and reduced_form[-1] == 0):
		reduced_form.pop()
	return reduced_form


def		print_first_degree_solution(reduced_form):
	print("Resolution steps:")
	if (reduced_form[0]):
		print(f"{reduced_form[1]} * X = {-reduced_form[0]}")
	if (reduced_form[1] != 1):
		print(f"X = {-reduced_form[0]} / {reduced_form[1]}")
	print("The solution is:")
	print(-reduced_form[0]/reduced_form[1])


def		print_second_degree_solution(reduced_form):
	quadratic = reduced_form[2]
	linear = reduced_form[1]
	constant = reduced_form[0]
	if (constant == 0 and linear == 0):
		print("The solution is:\n0.0")
		exit(0)
	if (linear):
		linear_term = f" + ({linear}/{quadratic}) * X^1"
	else:
		linear_term = ''
	if (constant):
		constant_term = f" + {constant}/{quadratic}"
	else:
		constant_term = ''
	print("Resolution steps:")
	# Step 1
	if (quadratic != 1):
		print(f"Divide each side by {quadratic}:\t\t\t\t", end='')
		print("X^2", end='')
		print(linear_term + constant_term + " = 0")
	# Step 2
	if (constant):
		print(f"Substract {constant}/{quadratic} from both sides:\t\t\t", end='')
		print(f"X^2" + linear_term + f" = {-constant}/{quadratic}")
	# Step 3
	if (linear):
		print(f"Add the square of one-half of {linear}/{quadratic} to both sides:\t", end='')
		print(f"X^2" + linear_term + f" + ((1/2) * ({linear}/{quadratic}))^2 = ", end='')
		if (constant):
			print(f"{-constant}/{quadratic} + ", end='')
		print(f"((1/2) * ({linear}/{quadratic}))^2")
	# Step 4
	if (linear):
		print("Factor and combine:\t\t\t\t\t", end='')
		print(f"(X + {linear}/(2*{quadratic}))^2 = ", end='')
		if (constant):
			print(f"({linear}^2 - 4*{quadratic}*{constant})/(4*{quadratic}^2)")
		else:
			print(f"{linear}^2/(4*{quadratic}^2)")
	# Step 5
	print("Find the square root of each side:\t\t\t", end='')
	print("X ", end='')
	if (linear):
		print(f"+ {linear}/(2*{quadratic}) ",end='')
	if (linear):
		delta_term = f"{linear}^2"
		if (constant):
			delta_term = delta_term + f" - 4*{quadratic}*{constant}"
	else:
		delta_term = f"- 4*{quadratic}*{constant}"
	print(f"= ± √({delta_term})/(2*{quadratic})")
	# Step 6
	if (linear):
		print("Solve for X:\t\t\t\t\t\t", end='')
		print(f"X = ({-linear} ± √({delta_term}))/2*{quadratic}")
	delta = linear**2 - 4 * quadratic * constant
	if (not delta):
		print(f"The discriminant ({delta_term}) is zero.\nThe solution is:")
		print(f"{-linear/(2*quadratic)}")
	elif (delta > 0):
		print(f"The discriminant ({delta_term}) is strictly positive.\nThe equation has two solutions:")
		print(f"{(-linear + delta**(.5))/(2*quadratic)}\n{(-linear - delta**(.5))/(2*quadratic)}")
	else:
		print(f"The discriminant ({delta_term}) is strictly negative.\nThe equation has two complex solutions:")
		print(f"{-linear/(2*quadratic)} + i * {(-delta)**(.5)/(2*quadratic)}\n{-linear/(2*quadratic)} - i * {(-delta)**(.5)/(2*quadratic)}")


def		print_information(reduced_form):
	if (reduced_form == []):
		print("Each real number is a solution.")
		exit(0)
	print('Reduced form: ', end='')
	for i, coeff in enumerate(reduced_form):
		if (coeff >= 0):
			print('+ ', end='')
		else:
			print('- ', end='')
		print(f"{abs(coeff)} * X^{i} ", end='')
	print('= 0')
	print(f'Polynomial degree: {len(reduced_form) - 1}')
	if (len(reduced_form) == 1):
		print("There are no solutions")
	elif (len(reduced_form) > 3):
		print("The polynomial degree is strictly greater than 2, I can't solve.")
	elif (len(reduced_form) == 2):
		print_first_degree_solution(reduced_form)
	else:
		print_second_degree_solution(reduced_form)


def     main():
	if (len(sys.argv) <= 1):
		equation = input("Enter an equation: ")
	elif (len(sys.argv) > 2):
		print(f"Usage: {sys.argv[0]} Equation")
		exit(1)
	else:
		equation = sys.argv[1]
	if (not equation):
		exit(1)
	reduced_form = get_reduced_form(equation)
	print_information(reduced_form)


if __name__ == "__main__":
    main()
