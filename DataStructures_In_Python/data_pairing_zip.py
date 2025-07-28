products = ["Laptop", "Mouse", "Keyboard", "Monitor"]
prices = [999.99, 25.50, 75.00, 299.99]
quantities = [5, 20, 15, 8]

# ---- 1. Create Product-Price Pairs ----
product_price_pairs = list(zip(products, prices))
print("Product-Price Pairs:")
print(product_price_pairs)
print()

# ---- 2. Calculate Total Value for Each Product ----
print("Total Inventory Value per Product:")
for product, price, qty in zip(products, prices, quantities):
    total_value = price * qty
    print(f"{product}: ${total_value:.2f}")
print()

# ---- 3. Build a Product Catalog Dictionary ----
catalog = {
    product: {"price": price, "quantity": qty}
    for product, price, qty in zip(products, prices, quantities)
}
print("Product Catalog Dictionary:")
print(catalog)
print()

# ---- 4. Find Low Stock Products (qty < 10) ----
low_stock = [product for product, info in catalog.items() if info["quantity"] < 10]
print("Low Stock Products (<10):")
print(low_stock)
