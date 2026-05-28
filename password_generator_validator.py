import random
import string
def pwd_check(pwd):

    lower_letter = any(x.islower() for x in pwd)
    upper_letter = any(x.isupper() for x in pwd)
    special_char = any(not x.isalnum() for x in pwd)
    errors = []
    if not lower_letter:
        errors.append("Validation Error: The password must have at least one lowercase letter")

    if not upper_letter:
        errors.append("Validation Error: The password must have at least one uppercase letter")

    if not special_char:
        errors.append("Validation Error: The password must have at least one special character")
    
    if len(pwd) < 6:
        errors.append("Validation Error: The password must be at least 6 characters long.")
    
    if len(errors) == 0:
        print("The password is Valid")
    else:
        raise ValueError("\n".join(errors))

def generate_pwd(x):
    characters = string.ascii_letters + string.digits
    pwd =[random.choice(string.ascii_uppercase), random.choice(string.ascii_lowercase), random.choice("!@#$%^&*")]
    for i in range(x-3):
        pwd.append(random.choice(characters))
    random.shuffle(pwd)
    return "".join(pwd)

print("=== Password Validation and Generator ===")
status = str(input("Do you want to generate a new password? (yes/no): "))
if status == "no":
    pwd = str(input("Enter your password to validate: "))
    try:
        pwd_check(pwd)
    except ValueError as e:
        print(e)
elif status == "yes":
    length = int(input("Enter the desired password length (minimum 6): "))
    print(f"Generated password: {generate_pwd(length)}")
else:
    print("Wrong input")

    

