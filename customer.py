import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import simpledialog
import psycopg2

class CustomerOrderApp:
    def __init__(self):
        self.selected_foods = []
        self.connect_to_db()
        self.create_main_window()

    def connect_to_db(self):
        try:
            self.conn = psycopg2.connect(
                host="localhost",
                database="postgres",
                user="postgres",
                password="mushtariy2004"
            )
            self.cursor = self.conn.cursor()
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
            messagebox.showerror("Error", "Failed to connect to the database")

    def fetch_food_items(self):
        query = "SELECT food_name, price FROM menu"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def fetch_table_info(self):
        query = "SELECT table_number, category FROM tables"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def submit_order(self, name, table):
        try:
            query = "INSERT INTO customer (name, tables, food) VALUES (%s, %s, %s) RETURNING id"
            values = (name, table, ', '.join([f[0] for f in self.selected_foods]))
            self.cursor.execute(query, values)
            order_id = self.cursor.fetchone()[0]  # Get the ID of the inserted order
            self.conn.commit()

        # Calculate total price
            total_price = sum(price for _, price in self.selected_foods)
            table_value = self.table_var.get()
            if table_value:
                table_category = table_value.split(' - ')[1].strip()
                if table_category == "A":
                    total_price += total_price * 0.1  # Add 10% fee for category A tables

        # Display order information in a pop-up message
            order_info_message = f"Order ID: {order_id}\nName: {name}\nFood: {', '.join([f[0] for f in self.selected_foods])}\nTotal Price: ${total_price:.2f}"
            messagebox.showinfo("Order Information", order_info_message)

            messagebox.showinfo("Success", "Order submitted successfully")
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
            messagebox.showerror("Error", "Failed to submit order")


    

    def on_checkbox_click(self, food_name, price):
        if len(self.selected_foods) < 10:
            self.selected_foods.append((food_name, price))
        else:
            messagebox.showwarning("Warning", "You can select up to 10 food items")
        self.update_total_price()

    def update_total_price(self):
        total_price = sum(price for _, price in self.selected_foods)
        table_value = self.table_var.get()
        if table_value:
            table_category = table_value.split(' - ')[1].strip()
            if table_category == "A":
                total_price += total_price * 0.1  # Add 10% fee for category A tables
        self.total_price_label.config(text=f"Total Price: ${total_price:.2f}")

    def create_main_window(self):
        self.main_window = tk.Tk()
        self.main_window.title("Customer Order")

        # Make order button
        make_order_button = tk.Button(self.main_window, text="Make Order", command=self.open_order_window)
        make_order_button.pack()

        # My order button
        my_order_button = tk.Button(self.main_window, text="My Order", command=self.view_my_order)
        my_order_button.pack()
       

        self.main_window.mainloop()

    def open_order_window(self):
        order_window = tk.Toplevel(self.main_window)
        order_window.title("Place Order")

        # Name field
        name_label = tk.Label(order_window, text="Name:")
        name_label.pack()
        self.name_entry = tk.Entry(order_window)
        self.name_entry.pack()

        # Food selection
        food_label = tk.Label(order_window, text="Food:")
        food_label.pack()
        foods = self.fetch_food_items()

        # Create checkboxes for food selection
        for food_info in foods:
            food_name, price = food_info
            var = tk.IntVar()
            checkbox = tk.Checkbutton(order_window, text=f"{food_name} - ${price:.2f}", variable=var, onvalue=1, offvalue=0, command=lambda f=food_name, p=price: self.on_checkbox_click(f, p))
            checkbox.pack(anchor=tk.W)

        # Table selection
        table_label = tk.Label(order_window, text="Table:")
        table_label.pack()
        tables = self.fetch_table_info()
        table_options = [f"{table[0]} - {table[1]}" for table in tables]
        self.table_var = tk.StringVar()
        table_dropdown = ttk.Combobox(order_window, textvariable=self.table_var, values=table_options)
        table_dropdown.pack()
        self.table_var.trace('w', lambda *args: self.update_total_price())  # Update total price when table selection changes

        # Total price label
        self.total_price_label = tk.Label(order_window, text="Total Price: $0.00")
        self.total_price_label.pack()

        # Submit button
        submit_button = tk.Button(order_window, text="Submit Order", command=lambda: self.submit_order(self.name_entry.get(), self.table_var.get()))
        submit_button.pack()

    def view_my_order(self):
        order_id = simpledialog.askstring("Enter Order ID", "Please enter your order ID:")
        if order_id:
            try:
                query = "SELECT * FROM customer WHERE id = %s"
                self.cursor.execute(query, (order_id,))
                order = self.cursor.fetchone()
                if order:
                    # Display order details and options for canceling or updating the order
                    order_details = f"Order ID: {order[0]}\nName: {order[1]}\nTable: {order[2]}\nFood: {order[3]}"
                    action = messagebox.askquestion("Order Details", f"Order details:\n{order_details}\n\nDo you want to cancel this order?")
                    if action == "yes":
                        # Cancel order
                        self.cancel_order(order_id)
                    else:
                        # Update order (you can implement this based on your requirements)
                        pass  # Placeholder for updating the order (you can implement this based on your requirements)
                else:
                    messagebox.showerror("Error", "Order not found")
            except (Exception, psycopg2.Error) as error:
                print("Error while fetching order details:", error)
                messagebox.showerror("Error", "Failed to fetch order details")

    def cancel_order(self, order_id):
        try:
            query = "DELETE FROM customer WHERE id = %s"
            self.cursor.execute(query, (order_id,))
            self.conn.commit()
            messagebox.showinfo("Success", "Order cancelled successfully")
        except (Exception, psycopg2.Error) as error:
            print("Error while cancelling order:", error)
            messagebox.showerror("Error", "Failed to cancel order")


# Run the app
app = CustomerOrderApp()
