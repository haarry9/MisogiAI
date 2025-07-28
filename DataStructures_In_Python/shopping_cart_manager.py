# Shopping Cart Manager

# Start with an empty cart
cart = []

# ---- Functions ----
def add_item(item):
    cart.append(item)
    print(f"Added '{item}' to the cart.")

def remove_item(item):
    if item in cart:
        cart.remove(item)
        print(f"Removed '{item}' from the cart.")
    else:
        print(f"Item '{item}' not found in the cart.")

def remove_last_item():
    if cart:
        removed = cart.pop()
        print(f"Removed last added item: '{removed}'")
    else:
        print("Cart is empty, nothing to remove.")

def display_sorted():
    if cart:
        print("Cart Items (Alphabetical Order):")
        for item in sorted(cart):
            print(item)
    else:
        print("Cart is empty.")

def display_cart_with_indices():
    if cart:
        print("Current Cart:")
        for index, item in enumerate(cart):
            print(f"{index}: {item}")
    else:
        print("Cart is empty.")

# ---- Sample Operations ----
add_item("apples")
add_item("bread")
add_item("milk")
add_item("eggs")

remove_item("bread")
remove_last_item()

display_sorted()
display_cart_with_indices()


