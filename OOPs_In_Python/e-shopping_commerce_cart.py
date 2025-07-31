# ---------- Product Class ----------
class Product:
    total_products = 0
    category_sales = {}

    def __init__(self, product_id, name, price, category, stock_quantity):
        if price < 0 or stock_quantity < 0:
            raise ValueError("Price and stock must be non-negative.")
        self.product_id = product_id
        self.name = name
        self.price = price
        self.category = category
        self.stock_quantity = stock_quantity
        Product.total_products += 1

    def get_product_info(self):
        return f"{self.name} ({self.category}) - ${self.price} | Stock: {self.stock_quantity}"

    def update_stock(self, quantity):
        if self.stock_quantity + quantity < 0:
            raise ValueError("Insufficient stock.")
        self.stock_quantity += quantity

    @classmethod
    def get_total_products(cls):
        return cls.total_products

    @classmethod
    def update_category_sales(cls, category, amount):
        cls.category_sales[category] = cls.category_sales.get(category, 0) + amount

    @classmethod
    def get_most_popular_category(cls):
        if not cls.category_sales:
            return "No sales yet"
        return max(cls.category_sales, key=cls.category_sales.get)


# ---------- Customer Class ----------
class Customer:
    total_revenue = 0

    def __init__(self, customer_id, name, email, membership="regular"):
        if not name or not email:
            raise ValueError("Customer name and email cannot be empty.")
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.membership = membership.lower()

    def get_discount_rate(self):
        return 10 if self.membership == "premium" else 0

    def __str__(self):
        return f"{self.name} ({self.membership.title()} Member)"

    @classmethod
    def add_revenue(cls, amount):
        cls.total_revenue += amount

    @classmethod
    def get_total_revenue(cls):
        return round(cls.total_revenue, 2)


# ---------- ShoppingCart Class ----------
class ShoppingCart:
    def __init__(self, customer):
        self.customer = customer
        self.items = {}  # product_id -> (Product, quantity)

    def add_item(self, product, quantity):
        if product.stock_quantity < quantity:
            raise ValueError(f"Not enough stock for {product.name}.")
        if product.product_id in self.items:
            self.items[product.product_id] = (product, self.items[product.product_id][1] + quantity)
        else:
            self.items[product.product_id] = (product, quantity)

    def remove_item(self, product_id):
        if product_id in self.items:
            del self.items[product_id]

    def clear_cart(self):
        self.items.clear()

    def get_cart_items(self):
        return {pid: qty for pid, (prod, qty) in self.items.items()}

    def get_total_items(self):
        return sum(qty for _, qty in self.items.values())

    def get_subtotal(self):
        return round(sum(prod.price * qty for prod, qty in self.items.values()), 2)

    def calculate_total(self):
        subtotal = self.get_subtotal()
        discount = (self.customer.get_discount_rate() / 100) * subtotal
        return round(subtotal - discount, 2)

    def place_order(self):
        if not self.items:
            return "Cart is empty. Cannot place order."

        total_price = self.calculate_total()

        # Deduct stock & update sales data
        for product, qty in self.items.values():
            product.update_stock(-qty)
            Product.update_category_sales(product.category, qty)
        # Add revenue to business
        Customer.add_revenue(total_price)

        self.clear_cart()
        return f"Order placed successfully! Total charged: ${total_price}"


# ---------- ✅ TEST CASES ----------
laptop = Product("P001", "Gaming Laptop", 1299.99, "Electronics", 10)
book = Product("P002", "Python Programming", 49.99, "Books", 25)
shirt = Product("P003", "Cotton T-Shirt", 19.99, "Clothing", 50)

print(f"Product info: {laptop.get_product_info()}")
print(f"Total products in system: {Product.get_total_products()}")

customer = Customer("C001", "John Doe", "john@email.com", "premium")
cart = ShoppingCart(customer)

print(f"Customer: {customer}")
print(f"Customer discount: {customer.get_discount_rate()}%")

cart.add_item(laptop, 1)
cart.add_item(book, 2)
cart.add_item(shirt, 3)

print(f"Cart total items: {cart.get_total_items()}")
print(f"Cart subtotal: ${cart.get_subtotal()}")

final_total = cart.calculate_total()
print(f"Final total (with {customer.get_discount_rate()}% discount): ${final_total}")

print(f"Laptop stock before order: {laptop.stock_quantity}")
order_result = cart.place_order()
print(f"Order result: {order_result}")
print(f"Laptop stock after order: {laptop.stock_quantity}")

popular_category = Product.get_most_popular_category()
print(f"Most popular category: {popular_category}")

total_revenue = Customer.get_total_revenue()
print(f"Total revenue: {total_revenue}")

cart.remove_item("P002")
print(f"Items after removal: {cart.get_cart_items()}")

cart.clear_cart()
print(f"Items after clearing: {cart.get_total_items()}")
