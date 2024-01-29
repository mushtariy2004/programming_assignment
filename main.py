import tkinter as tk
from tkinter import messagebox
import psycopg2

class RestaurantApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Restaurant App")
        self.geometry("500x500")
        
        self.manager_button = tk.Button(self, text="Stuff", command=self.open_manager_login)
        self.manager_button.pack()

    def open_manager_login(self):
        manager_login_window = ManagerLoginWindow(self)

class ManagerLoginWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Stuff Login")
        self.geometry("300x300")

        self.username_label = tk.Label(self, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        self.password_label = tk.Label(self, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self, text="Login", command=self.login)
        self.login_button.pack()

    def login(self):
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="postgres",
                user="postgres",
                password="mushtariy2004"
            )
            cursor = conn.cursor()
            query = f"SELECT * FROM manager WHERE username = '{self.username_entry.get()}' AND password = '{self.password_entry.get()}'"
            cursor.execute(query)
            if cursor.fetchone() is not None:
                self.destroy()  # Close the login window
                manager_window = ManagerWindow(self.master)
            else:
                messagebox.showerror("Error", "Invalid username or password")
            cursor.close()
            conn.close()
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
            messagebox.showerror("Error", "Failed to connect to the database")

class ManagerWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Stuff Window")

        self.add_food_button = tk.Button(self, text="Add Food", command=self.open_add_food)
        self.add_food_button.pack()

        self.view_food_list_button = tk.Button(self, text="View Food List", command=self.open_view_food_list)
        self.view_food_list_button.pack()

        self.view_order_list_button = tk.Button(self, text="Order List", command=self.view_order_list)
        self.view_order_list_button.pack()

        self.add_table_button = tk.Button(self, text="Add Table", command=self.open_add_table)
        self.add_table_button.pack()

        self.uptade_food_button = tk.Button(self, text="Uptade Food", command=self.open_edit_food)
        self.uptade_food_button.pack()

        self.geometry("300x150")

    def view_order_list(self):
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="postgres",
                user="postgres",
                password="mushtariy2004"
            )
            cursor = conn.cursor()
            query = "SELECT * FROM customer"
            cursor.execute(query)
            rows = cursor.fetchall()
            order_list_window = tk.Toplevel(self)
            order_list_window.title("Order List")
            for row in rows:
                order_info_label = tk.Label(order_list_window, text=f"{row[0]} - {row[1]} - {row[2]}-{row[3]}")
                order_info_label.pack()
            cursor.close()
            conn.close()
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
            messagebox.showerror("Error", "Failed to fetch order list")

    def open_edit_food(self):
        edit_food_window = EditFoodWindow(self)

    def open_add_food(self):
        add_food_window = AddFoodWindow(self)

    def open_add_table(self):
        add_table_window = AddTableWindow(self)

    def open_view_food_list(self):
        view_food_list_window = ViewFoodListWindow(self)

class AddFoodWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add Food")

        self.food_name_label = tk.Label(self, text="Food Name:")
        self.food_name_label.pack()
        self.food_name_entry = tk.Entry(self)
        self.food_name_entry.pack()

        self.food_description_label = tk.Label(self, text="Food Description:")
        self.food_description_label.pack()
        self.food_description_entry = tk.Entry(self)
        self.food_description_entry.pack()

        self.price_label = tk.Label(self, text="Price:")
        self.price_label.pack()
        self.price_entry = tk.Entry(self)
        self.price_entry.pack()

        self.add_food_button = tk.Button(self, text="Add Food", command=self.add_food)
        self.add_food_button.pack()

    def add_food(self):
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="postgres",
                user="postgres",
                password="mushtariy2004"
            )
            cursor = conn.cursor()
            query = "INSERT INTO menu (food_name, food_description, price) VALUES (%s, %s, %s)"
            values = (self.food_name_entry.get(), self.food_description_entry.get(), self.price_entry.get())
            cursor.execute(query, values)
            conn.commit()
            messagebox.showinfo("Success", "Food added successfully")
            cursor.close()
            conn.close()
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
            messagebox.showerror("Error", "Failed to add food")

class AddTableWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add Table")

        self.table_number_label = tk.Label(self, text="Table Number:")
        self.table_number_label.pack()
        self.table_number_entry = tk.Entry(self)
        self.table_number_entry.pack()

        self.category_label = tk.Label(self, text="Category:")
        self.category_label.pack()
        self.category_entry = tk.Entry(self)
        self.category_entry.pack()

        self.save_button = tk.Button(self, text="Save", command=self.save_table)
        self.save_button.pack()

    def save_table(self):
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="postgres",
                user="postgres",
                password="mushtariy2004"
            )
            cursor = conn.cursor()
            query = "INSERT INTO tables (table_number, category) VALUES (%s, %s)"
            values = (self.table_number_entry.get(), self.category_entry.get())
            cursor.execute(query, values)
            conn.commit()
            messagebox.showinfo("Success", "Table added successfully")
            cursor.close()
            conn.close()
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
            messagebox.showerror("Error", "Failed to add table")

class ViewFoodListWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("View Food List")

        self.food_listbox = tk.Listbox(self, selectmode=tk.SINGLE)
        self.food_listbox.pack()

        self.delete_button = tk.Button(self, text="Delete", command=self.delete_food)
        self.delete_button.pack()

        self.update_food_list()

    def delete_food(self):
        selected_item = self.food_listbox.curselection()
        if selected_item:
            try:
                conn = psycopg2.connect(
                host="localhost",
                database="postgres",
                user="postgres",
                password="mushtariy2004"
                )
                cursor = conn.cursor()
                query = "DELETE FROM menu WHERE food_name = %s"
                cursor.execute(query, (self.food_listbox.get(selected_item),))
                conn.commit()
                messagebox.showinfo("Success", "Food item deleted successfully")
                cursor.close()
                conn.close()
                self.update_food_list()
            except (Exception, psycopg2.Error) as error:
                print("Error while connecting to PostgreSQL", error)
                messagebox.showerror("Error", "Failed to delete food item")
        else:
            messagebox.showerror("Error", "No food item selected")

    def update_food_list(self):
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="postgres",
                user="postgres",
                password="mushtariy2004"
            )
            cursor = conn.cursor()
            query = "SELECT food_name FROM menu"
            cursor.execute(query)
            foods = [row[0] for row in cursor.fetchall()]
            self.food_listbox.delete(0, tk.END)
            for food in foods:
                self.food_listbox.insert(tk.END, food)
            cursor.close()
            conn.close()
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
            messagebox.showerror("Error", "Failed to fetch food items")


class EditFoodWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Edit Food")

        self.food_listbox = tk.Listbox(self, selectmode=tk.SINGLE)
        self.food_listbox.pack()

        self.load_food_list()
        self.food_listbox.bind("<<ListboxSelect>>", self.load_selected_food)

        self.food_name_label = tk.Label(self, text="Food Name:")
        self.food_name_label.pack()
        self.food_name_entry = tk.Entry(self)
        self.food_name_entry.pack()

        self.food_description_label = tk.Label(self, text="Food Description:")
        self.food_description_label.pack()
        self.food_description_entry = tk.Entry(self)
        self.food_description_entry.pack()

        self.price_label = tk.Label(self, text="Price:")
        self.price_label.pack()
        self.price_entry = tk.Entry(self)
        self.price_entry.pack()

        self.save_button = tk.Button(self, text="Save", command=self.save_food_changes)
        self.save_button.pack()

    def load_food_list(self):
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="postgres",
                user="postgres",
                password="mushtariy2004"
            )
            cursor = conn.cursor()
            query = "SELECT food_name FROM menu"
            cursor.execute(query)
            foods = [row[0] for row in cursor.fetchall()]
            self.food_listbox.delete(0, tk.END)
            for food in foods:
                self.food_listbox.insert(tk.END, food)
            cursor.close()
            conn.close()
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
            messagebox.showerror("Error", "Failed to fetch food items")

    def load_selected_food(self, event):
        selected_index = self.food_listbox.curselection()
        if selected_index:
            try:
                conn = psycopg2.connect(
                host="localhost",
                database="postgres",
                user="postgres",
                password="mushtariy2004"
                )
                cursor = conn.cursor()
                query = "SELECT food_name, food_description, price FROM menu WHERE food_name = %s"
                cursor.execute(query, (self.food_listbox.get(selected_index),))
                food_data = cursor.fetchone()
                if food_data:
                    self.food_name_entry.delete(0, tk.END)
                    self.food_name_entry.insert(tk.END, food_data[0])
                    self.food_description_entry.delete(0, tk.END)
                    self.food_description_entry.insert(tk.END, food_data[1])
                    self.price_entry.delete(0, tk.END)
                    self.price_entry.insert(tk.END, str(food_data[2]))
                cursor.close()
                conn.close()
            except (Exception, psycopg2.Error) as error:
                print("Error while connecting to PostgreSQL", error)
                messagebox.showerror("Error", "Failed to fetch food details")

    def save_food_changes(self):
        selected_index = self.food_listbox.curselection()
        if selected_index:
            try:
                conn = psycopg2.connect(
                host="localhost",
                database="postgres",
                user="postgres",
                password="mushtariy2004"
                )
                cursor = conn.cursor()
                query = "UPDATE menu SET food_name = %s, food_description = %s, price = %s WHERE food_name = %s"
                new_values = (
                    self.food_name_entry.get(),
                    self.food_description_entry.get(),
                    self.price_entry.get(),
                    self.food_listbox.get(selected_index)
                )
                cursor.execute(query, new_values)
                conn.commit()
                messagebox.showinfo("Success", "Food details updated successfully")
                cursor.close()
                conn.close()
                self.load_food_list()  # Refresh the food list after update
            except (Exception, psycopg2.Error) as error:
                print("Error while connecting to PostgreSQL", error)
                messagebox.showerror("Error", "Failed to update food details")
        else:
            messagebox.showerror("Error", "No food item selected")


if __name__ == "__main__":
    app = RestaurantApp()
    app.mainloop()
