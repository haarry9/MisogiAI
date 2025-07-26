def get_valid_age():
    while True:
        user_input = input("Enter your age (1-128): ")

        try:
            age = int(user_input)
            if 1 <= age <= 120:
                print(f"You entered a valid age: {age}")
                break
            else:
                print("Out of range. Please enter a number between 1 and 120.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        
get_valid_age()

            