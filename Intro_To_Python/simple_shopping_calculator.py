def shopping_calc(price1: int, qty1: int, price2: int, qty2: int, price3: int, qty3: int ):
    print(f"Iten 1: {price1} x {qty1} = {price1 * qty1}")
    print(f"Iten 2: {price2} x {qty2} = {price2 * qty2}")
    print(f"Iten 3: {price3} x {qty3} = {price3 * qty3}")
    subtotal = price1 * qty1 + price2 * qty2 + price3 * qty3 
    print(f"Subtotal: {subtotal} ")
    print(f"Tax (8.5%): {0.85 * subtotal}")
    print(f"Total: {subtotal + 0.085 * subtotal }")

if __name__ == "__main__":
    item1_price = int(input("Enter price of item 1: "))
    item1_qty = int(input("Enter quantity of iten 1: "))
    item2_price = int(input("Enter price of item 1: "))
    item2_qty = int(input("Enter quantity of iten 1: "))
    item3_price = int(input("Enter price of item 1: "))
    item3_qty = int(input("Enter quantity of iten 1: "))
    shopping_calc(item1_price, item1_qty, item2_price, item2_qty, item3_price,item3_qty)



