# # 1. Even or Odd > %
# # Ask the user to enter a number.
# # Print whethheder the number is even or odd.

# Number=int(input('Type a number:'))
# if Number % 2 != 1:
#     print('the number:', Number, 'is a even num')
# else:
#     print('the number:', Number, 'is a odd num')




# Number=int(input('Type a number:'))

# if Number <= 0:
#     print('Positive')

# elif Number > 0:
#     print('nagative')


# # 2. Day Type Checker
# # Ask the user to enter a day of the week (e.g., "Monday").
# # Print "Weekend" if it's Friday or Saturday, else print "Weekday".

# Day=input('Type a day of the week:')

# if Day == 'Friday' or 'Saturday':
#     print('Weekend')
# else:
#     print('Weekday')



# # 3. Age Category
# # Ask the user to enter their age.
# # Print:
# #   - "Child" if age is 0–12
# #   - "Teen" if 13–19
# #   - "Adult" if 20–59
# #   - "Senior" if 60 or more


# Age=int(input('your age:'))
# if Age <= 12:
#     print('Child')

# elif Age >= 14 and Age <= 19 :
#     print('Teen')

# elif Age >= 20 and Age <= 59 :
#     print('Adult')

# else :
# #     print('Senior')
 

# # # 4. Simple Calculator
# # # Ask the user to input two numbers and an operator (+, -, *, /).
# # # Use if/elif/else to perform the correct operation and show the result.

# number1=int(input('type first number:'))
# number2=int(input('type secound number:'))
# operator=input('choose operator(+, -, *, /):' )
# if operator=='+':
#     print('addition is:', number1+number2)
# elif operator=='-':
#     print('minus is:', number1-number2)
# elif operator=='*':
#     print('multiple is:', number1*number2)
# elif operator=='/':
#     print('divi is:', number1/number2)
# else:
#     print('chose wrong oparstor')




# 5. Number Comparison
# Ask the user for two numbers.
# Print which one is larger, or if they are equal.

# number1=int(input('type first number:'))
# number2=int(input('type secound number:'))
# if number1>number2:
#     print('number',number1,' is grater')
# elif number1<number2:
#     print('number',number2,' is grater')
# else:
#     print('they are equal')







# 6. Simple Login
# Set a password one and password in the program.
# Ask the user to input username and password.
# Print:
#   - "Password matc" if both match
#   - "Password not same" or "Password not Matched" as needed
# name = input('username: ')
# password = input('password: ')
# password1 =input('confrm password: ')


# if password == password1 :
#     print('Password matc')
# else:
#     print('Password not same')

# 7. Water Temperature Checker
# Ask the user to enter the water temperature in Celsius.
# Print:
#   - "Freezing" if below 0
#   - "Cold" if 0–30
#   - "Warm" if 31–60
#   - "Hot" if above 60

# Celsius=int(input('type the water temperature in Celsius:'))

# if Celsius < 0:
#     print("Freezing")

# elif Celsius >= 0 and Celsius <= 30 :
#     print("Cold")

# elif Celsius >= 31 and Celsius <= 60 :
#     print("Warm")

# elif Celsius > 60:
#     print("Hot")

# Question 8: Password Strength
# Ask the user to enter a password.


# "Weak" if password length < 6

# "Medium" if 6–10 characters

# "Strong" if more than 10 characters