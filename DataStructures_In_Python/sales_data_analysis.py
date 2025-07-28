# Given data
sales_data = [
    ("Q1", [("Jan", 1000), ("Feb", 1200), ("Mar", 1100)]),
    ("Q2", [("Apr", 1300), ("May", 1250), ("Jun", 1400)]),
    ("Q3", [("Jul", 1350), ("Aug", 1450), ("Sep", 1300)])
]

# ---- 1. Calculate Total Sales per Quarter ----
print("Total Sales per Quarter:")
for quarter, monthly_sales in sales_data:
    total = sum(sale for month, sale in monthly_sales)  # unpack (month, sale)
    print(f"{quarter}: {total}")
print()

# ---- 2. Find the Month with Highest Sales ----
highest_month = ("", 0)
for quarter, monthly_sales in sales_data:
    for month, sale in monthly_sales:
        if sale > highest_month[1]:
            highest_month = (month, sale)
print(f"Month with Highest Sales: {highest_month[0]} ({highest_month[1]})")
print()

# ---- 3. Create a Flat List of Monthly Sales ----
flat_sales = [(month, sale) for quarter, monthly_sales in sales_data for month, sale in monthly_sales]
print("Flat List of Monthly Sales:")
print(flat_sales)
print()

# ---- 4. Use Unpacking in Loops (demonstration) ----
print("Iterating with Tuple Unpacking:")
for quarter, monthly_sales in sales_data:
    print(f"\n{quarter}:")
    for month, sale in monthly_sales:
        print(f"  {month} -> {sale}")
