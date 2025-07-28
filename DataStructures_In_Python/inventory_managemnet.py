# Initial inventory
inventory = {
    "apples": {"price": 1.50, "quantity": 100},
    "bananas": {"price": 0.75, "quantity": 150},
    "oranges": {"price": 2.00, "quantity": 80}
}

# ---- 1. Add a New Product ----
inventory["grapes"] = {"price": 3.00, "quantity": 50}
print("Added new product: grapes")
print(inventory)
print()

# ---- 2. Update Product Price ----
inventory["bananas"]["price"] = 0.85
print("Updated price of bananas")
print(inventory)
print()

# ---- 3. Sell 25 Apples ----
if inventory["apples"]["quantity"] >= 25:
    inventory["apples"]["quantity"] -= 25
    print("Sold 25 apples.")
else:
    print("Not enough apples in stock.")
print(inventory)
print()

# ---- 4. Calculate Total Inventory Value ----
total_value = sum(info["price"] * info["quantity"] for info in inventory.values())
print(f"Total Inventory Value: ${total_value:.2f}")
print()

# ---- 5. Find Low Stock Products (quantity < 100) ----
low_stock = [product for product, info in inventory.items() if info["quantity"] < 100]
print("Low Stock Products (<100):", low_stock)
