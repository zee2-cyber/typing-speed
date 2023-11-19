class Table:
    def __init__(self, number):
        self.number = number
        self.waiter = None
        self.customers = 0
        self.orders = []

    def assign_waiter(self, waiter):
        self.waiter = waiter

    def add_customers(self, num_customers):
        self.customers = num_customers

    def add_order(self, order):
        self.orders.append(order)

    def clear_orders(self):
        self.orders = []
        self.waiter = None
        self.customers = 0


class Bill:
    def __init__(self, table_number):
        self.table_number = table_number
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)

    def calculate_total(self):
        total = 0
        for order in self.orders:
            total += order.price * order.quantity
        return total


class Order:
    def __init__(self, item, price, quantity):
        self.item = item
        self.price = price
        self.quantity = quantity


class PointOfSale:
    def __init__(self):
        self.tables = []
        self.waiters = {}
        self.sales_total = 0

        # Load waiter login credentials from file
        self.load_waiters()

    def load_waiters(self):
        try:
            with open('Login.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split(',')
                    self.waiters[username] = password
        except FileNotFoundError:
            print("Login file not found.")

    def login(self):
        username = input("Enter username: ")
        password = input("Enter password: ")

        if username in self.waiters and self.waiters[username] == password:
            print("Login successful.")
            return username
        else:
            print("Invalid username or password.")
            return None

    def display_menu(self):
        print("\nMain Menu:")
        print("1. Assign Table")
        print("2. Change customers")
        print("3. Add to Order")
        print("4. Prepare bill")
        print("5. Complete Sale")
        print("6. Cash up")
        print("0. Log Out")

    def assign_table(self, waiter):
        # Check if there are available tables
        if len(self.tables) >= 6:
            print("All tables are currently assigned.")
            return

        table_number = int(input("Enter table number: "))

        # Check if the table is already assigned
        for table in self.tables:
            if table.number == table_number:
                print("Table is already assigned.")
                return

        table = Table(table_number)
        table.assign_waiter(waiter)
        self.tables.append(table)
        print("Table assigned to waiter:", waiter)

    def change_customers(self, waiter):
        table_number = int(input("Enter table number: "))

        # Find the table assigned to the waiter
        table = None
        for t in self.tables:
            if t.number == table_number and t.waiter == waiter:
                table = t
                break

        if table:
            num_customers = int(input("Enter number of customers: "))
            table.add_customers(num_customers)
            print("Number of customers changed.")
        else:
            print("Invalid table or not assigned to the waiter.")

    def add_to_order(self, waiter):
        table_number = int(input("Enter table number: "))

        # Find the table assigned to the waiter
        table = None
        for t in self.tables:
            if t.number == table_number and t.waiter == waiter:
                table = t
                break

        if table:
            item = input("Enter item name: ")
            price = float(input("Enter item price: "))
            quantity = int(input("Enter quantity: "))
            order = Order(item, price, quantity)
            table.add_order(order)
            print("Order added.")
        else:
            print("Invalid table or not assigned to the waiter.")

    def prepare_bill(self, waiter):
        table_number = int(input("Enter table number: "))

        # Find the table assigned to the waiter
        table = None
        for t in self.tables:
            if t.number == table_number and t.waiter == waiter:
                table = t
                break

        if table:
            bill = Bill(table_number)
            for order in table.orders:
                bill.add_order(order)

            # Display the bill
            print("\nBill for Table", table_number)
            for order in bill.orders:
                print(f"{order.item} - {order.price} x {order.quantity}")

            total = bill.calculate_total()
            print("Total:", total)

            # Save the bill to a file
            file_name = input("Enter file name: ")
            with open(file_name, 'w') as file:
                file.write(f"Bill for Table {table_number}\n")
                for order in bill.orders:
                    file.write(f"{order.item} - {order.price} x {order.quantity}\n")
                file.write(f"Total: {total}\n")

            print("Bill prepared.")
        else:
            print("Invalid table or not assigned to the waiter.")

    def complete_sale(self, waiter):
        table_number = int(input("Enter table number: "))

        # Find the table assigned to the waiter
        table = None
        for t in self.tables:
            if t.number == table_number and t.waiter == waiter:
                table = t
                break

        if table:
            if len(table.orders) == 0:
                print("No orders for this table. Prepare a bill first.")
                return

            total = 0
            for order in table.orders:
                total += order.price * order.quantity

            self.sales_total += total
            print("Sale completed.")
            table.clear_orders()
        else:
            print("Invalid table or not assigned to the waiter.")

    def cash_up(self):
        print("Total sales:", self.sales_total)
        choice = input("Do you want to clear the daily total? (Y/N): ")
        if choice.upper() == 'Y':
            self.sales_total = 0
            print("Daily total cleared.")

    def run(self):
        logged_in_waiter = None

        while True:
            if logged_in_waiter is None:
                logged_in_waiter = self.login()

            if logged_in_waiter:
                self.display_menu()
                choice = input("Enter your choice: ")

                if choice == '1':
                    self.assign_table(logged_in_waiter)
                elif choice == '2':
                    self.change_customers(logged_in_waiter)
                elif choice == '3':
                    self.add_to_order(logged_in_waiter)
                elif choice == '4':
                    self.prepare_bill(logged_in_waiter)
                elif choice == '5':
                    self.complete_sale(logged_in_waiter)
                elif choice == '6':
                    self.cash_up()
                elif choice == '0':
                    logged_in_waiter = None
                else:
                    print("Invalid choice. Try again.")
            else:
                print("Please login first.")


# Create and run the PointOfSale application
pos = PointOfSale()
pos.run()
