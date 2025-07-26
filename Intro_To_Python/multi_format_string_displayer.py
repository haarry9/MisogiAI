name = "Alice"
age = 28
city = "Delhi"

print("Using % formatting:")
sentence_percent = "My name is %s, I am %d years old, and I live in %s." % (name, age, city)
print(sentence_percent)

print("-" * 20)

print("Using .format():")
sentence_format = "My name is {}, I am {} years old, and I live in {}.".format(name, age, city)
print(sentence_format)

print("-" * 20)

print("Using f-strings:")
sentence_fstring = f"My name is {name}, I am {age} years old, and I live in {city}."
print(sentence_fstring)