def display_formatted_summary(name: str, age:int,city:str, hobby: str):
    print(f"Hello, {name}")
    print(f"You are {age} yers old and live in {city}")
    print(f"In your free time, you enjoy {hobby}.")

if __name__ == "__main__":
    Name = str(input("Enter your full name: "))
    Age = str(input("Enter your age: "))
    City = str(input("Enter your city: "))
    Hobby = str(input("Enter your hobby: "))

    display_formatted_summary(Name, Age, City, Hobby)