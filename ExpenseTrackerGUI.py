import tkinter as tk
from tkinter import simpledialog, messagebox
import pandas as pd
import networkx as nx
import csv
from tkinter import filedialog
from tkinter import ttk
from tkinter import PhotoImage
from maxheap import MaxHeap




class SuiteShareGUI:
    def __init__(self, root_window):
        self.root_window = root_window
        root_window.title("SuiteShare")
        root_window.configure(bg="#4C7330")
        self.load()

        self.image = PhotoImage(file="suiteshare.png")

        # Image Label
        self.image = self.image.subsample(2, 2)
        self.label_image = tk.Label(root_window, image=self.image, bg="#4C7330")
        self.label_image.place(x=62.5)

        # Add User Button
        self.button_add_user = tk.Button(root_window, text="Add User", font=("Segoe UI", 16, "bold"), bg="#D9B777", fg="#4C7330", command=self.add_user, pady = 2,)
        self.button_add_user.grid(row=2, column=0, padx=10, pady=(125, 30), sticky="we")

        self.button_remove_user = tk.Button(root_window, text="Remove User", font=("Segoe UI", 16, "bold"), bg="#D9B777", fg="#4C7330", command=self.remove_user, pady = 2,)
        self.button_remove_user.grid(row=2, column=1, padx=10, pady=(125, 30), sticky="we")

        # Debtor Entry Widget
        self.debtor_label = tk.Label(root_window, text="Debtor:", font=("Segoe UI", 16, "bold"), bg="#4C7330", fg="#D9B777")
        self.debtor_label.grid(row=3, column=0, padx=10, pady=10, sticky="we")
        self.debtor_entry = tk.Entry(root_window, font=("Segoe UI", 16), bg="#D9B777", fg="#4C7330")
        self.debtor_entry.grid(row=3, column=1, padx=10, pady=10, sticky="we")

        # Creditor Entry Widget
        self.creditor_label = tk.Label(root_window, text="Creditor:", font=("Segoe UI", 16, "bold"), bg="#4C7330", fg="#D9B777")
        self.creditor_label.grid(row=4, column=0, padx=10, pady=10, sticky="we")
        self.creditor_entry = tk.Entry(root_window, font=("Segoe UI", 16), bg="#D9B777", fg="#4C7330")
        self.creditor_entry.grid(row=4, column=1, padx=10, pady=10, sticky="we")

        # Amount Entry Widget
        self.amount_label = tk.Label(root_window, text="Amount:", font=("Segoe UI", 16, "bold"), bg="#4C7330", fg="#D9B777")
        self.amount_label.grid(row=5, column=0, padx=10, pady=10, sticky="we")
        self.amount_entry = tk.Entry(root_window, font=("Segoe UI", 16), bg="#D9B777", fg="#4C7330")
        self.amount_entry.grid(row=5, column=1, padx=10, pady=10, sticky="we")

        # Add Debt and Remove Debt Buttons
        self.add_debt_button = tk.Button(root_window, text="Add Debt", font=("Segoe UI", 16, "bold"), bg="#D9B777", fg="#4C7330", command=self.add_debt, pady = 2)
        self.add_debt_button.grid(row=3, column=2, rowspan = 2, padx=(10,20), pady=(10, 10), sticky="we")
        self.remove_debt_button = tk.Button(root_window, text="Remove Debt", font=("Segoe UI", 16, "bold"), bg="#D9B777", fg="#4C7330", command=self.remove_debt, pady = 2)
        self.remove_debt_button.grid(row=4, column=2, rowspan = 3, padx=(10,20), pady=(10, 10), sticky="we")

        # Settle Debt and Calculate Sales Tax Buttons

        self.button_clear_debts = tk.Button(root_window, text="Settle Debt", font=("Segoe UI", 16, "bold"), bg="#D9B777", fg="#4C7330", command=self.clear_debt, pady = 2)
        self.button_clear_debts.grid(row=7, column=0, padx=10, pady=(40,10), sticky="we")

        self.button_sales_tax = tk.Button(root_window, text="Sales Tax", font=("Segoe UI", 16, "bold"), bg="#D9B777", fg="#4C7330", command=self.sales_tax, pady = 2,)
        self.button_sales_tax.grid(row=7, column=1, padx=10, pady=(40,10), sticky="we")

        # Save and Load Buttons

        #self.button_save = tk.Button(root_window, text="Save", font=("Courier New", 18, "bold"), bg="#f0f0f0", fg="#333333", command=self.save, pady = 4)
        #self.button_save.grid(row=1, column=1, padx=10, pady=(30, 30), sticky="we")

        #self.button_load = tk.Button(root_window, text="Load", font=("Courier New", 16, "bold"), bg="#f0f0f0", fg="#333333", command=self.load, pady = 2)
        #self.button_load.grid(row=8, column=0, padx=10, pady=10, sticky="we")

        # Debt Log and Debt Table Buttons

        self.button_show_debts = tk.Button(root_window, text="Debt Log", font=("Segoe UI", 16, "bold"), bg="#D9B777", fg="#4C7330", command=self.show_debts, pady = 2)
        self.button_show_debts.grid(row=8, column=0, padx=10, pady=10, sticky="we")

        self.button_show_graph = tk.Button(root_window, text="Debt Table", font=("Segoe UI", 16, "bold"), bg="#D9B777", fg="#4C7330", command=self.show_graph, pady = 2)
        self.button_show_graph.grid(row=8, column=1, padx=10, pady=10, sticky="we")

        # Clear Data Button

        self.button_clear_data = tk.Button(root_window, text="Clear Data", font=("Segoe UI", 16, "bold"), bg="#D9B777", fg="#4C7330", command=self.clear_data, pady = 2)
        self.button_clear_data.grid(row=9, column=0, padx=10, pady=(10,20), sticky="we")

        self.button_sort_users = tk.Button(root_window, text="Sort Users", font=("Segoe UI", 16, "bold"), bg="#D9B777", fg="#4C7330", command=self.sort_users_by_debt, pady=2)
        self.button_sort_users.grid(row=7, column=2, padx=(10, 20), pady=(40, 10), sticky="we")


        # Create data structures
        self.users = []
        self.debts = pd.DataFrame(columns=["From", "To", "Amount"])
        self.total_debt = {}

        # Create directed graph
        self.graph = nx.DiGraph()


    def load(self):
        self.total_debt = {}
        # Load users and debts data from CSV files
        self.users_df = pd.read_csv("users.csv")
        self.users = list(self.users_df["Name"])

        self.debts = pd.read_csv("debts.csv")

        # Load graph data from CSV file
        graph_df = pd.read_csv("graph.csv", index_col=0, header=0)
        self.graph = nx.DiGraph(graph_df.values)
        self.graph = nx.relabel_nodes(self.graph, dict(enumerate(graph_df.columns)))

        # Load user debts from a file
        with open("user_debts.txt", "r") as file:
            for line in file:
                user, debt = line.strip().split(",")
                self.total_debt[user] = float(debt)


    def add_user(self):
        self.load()
        # Get user name from user input
        user_name = tk.simpledialog.askstring("Add User", "Enter user name:")

        # Check if the user name already exists
        if user_name in self.users:
            tk.messagebox.showerror("Error", "User already exists.")
            return

        # Add the user to the users list
        self.users.append(user_name)

        # Add the user as a node to the graph
        self.graph.add_node(user_name)

        # Display a message confirming that the user has been added
        tk.messagebox.showinfo("Success", f"User {user_name} has been added.")
        self.save()

    def remove_user(self):
        self.load()
        # Get user name from user input
        user_name = tk.simpledialog.askstring("Remove User", "Enter user name:")

        # Check if the user name doesn't exists
        if user_name  not in self.users:
            tk.messagebox.showerror("Error", "User does not exist.")
            return

        # Add the user to the users list
        self.users.remove(user_name)

        # Add the user as a node to the graph
        self.graph.remove_node(user_name)

        # Display a message confirming that the user has been added
        tk.messagebox.showinfo("Success", f"User {user_name} has been removed.")
        self.save()



    def add_debt(self):
        self.load()
        # Get debt details from user input
        from_user = self.debtor_entry.get()
        to_user = self.creditor_entry.get()
        amountt = self.amount_entry.get()
        amount = float(amountt)

        # Add debt to dataframe
        self.debts = self.debts.append({
            "From": from_user,
            "To": to_user,
            "Amount": amount
        }, ignore_index=True)

        # Update graph with new debt
        if from_user not in self.users:
            self.users.append(from_user)
            self.graph.add_node(from_user)
        if to_user not in self.users:
            self.users.append(to_user)
            self.graph.add_node(to_user)
        if (from_user, to_user) in self.graph.edges():
            self.graph[from_user][to_user]['weight'] += amount
        else:
            self.graph.add_edge(from_user, to_user, weight=amount)

        # Update total debt
        if from_user not in self.total_debt:
            self.total_debt[from_user] = 0
        if to_user not in self.total_debt:
            self.total_debt[to_user] = 0
        self.total_debt[from_user] += amount
        self.total_debt[to_user] -= amount

        # Display a message confirming that the debt has been added
        tk.messagebox.showinfo("Success", f"{from_user} owes {to_user} ${amount:.2f}")
        self.save()
        self.debtor_entry.delete(0, tk.END)
        self.creditor_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)

    def remove_debt(self):
        self.load()
         # Get debt details from user input
        from_user = self.debtor_entry.get()
        to_user = self.creditor_entry.get()
        amountt = self.amount_entry.get()
        amount = float(amountt)

        # Add debt to dataframe
        self.debts = self.debts.append({
            "From": from_user,
            "To": to_user,
            "Amount": -amount
        }, ignore_index=True)

        # Update graph with new debt
        if from_user not in self.users:
            self.users.append(from_user)
            self.graph.add_node(from_user)
        if to_user not in self.users:
            self.users.append(to_user)
            self.graph.add_node(to_user)
        if (from_user, to_user) in self.graph.edges():
            self.graph[from_user][to_user]['weight'] -= amount
        else:
            self.graph.add_edge(from_user, to_user, weight=amount)

        # Update total debt
        if from_user not in self.total_debt:
            self.total_debt[from_user] = 0
        if to_user not in self.total_debt:
            self.total_debt[to_user] = 0
        self.total_debt[from_user] -= amount
        self.total_debt[to_user] += amount

        # Display a message confirming that the debt has been added
        tk.messagebox.showinfo("Success", f"The amount {amount} has been removed from the debt between {from_user} and {to_user}.")
        self.save()
        self.debtor_entry.delete(0, tk.END)
        self.creditor_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)


    def clear_debt(self):
        self.load()
        # Get user name from user input
        user = tk.simpledialog.askstring("Clear Debt", "Enter the name of the user to clear debts for:")

        # Remove all debts involving the user
        self.debts = self.debts.loc[(self.debts["From"] != user) & (self.debts["To"] != user)]
        self.total_debt = {}
        for edge in list(self.graph.edges()):  # Make a copy of the edges list
            if edge[0] == user:
                self.graph.remove_edge(*edge)
            elif edge[1] == user:
                self.graph.remove_edge(*edge)

        # Display a message confirming that the debts have been cleared
        tk.messagebox.showinfo("Success", f"All debts involving {user} have been cleared.")
        self.save()


    def sales_tax(self):
        # Code to calculate sales tax for debts
        pass



    def save(self):
        # Save user names to users.csv
        pd.DataFrame(self.users, columns=["Name"]).to_csv("users.csv", index=False)

        # Save debts to debts.csv
        self.debts.to_csv("debts.csv", index=False)

        # Save graph to graph.csv
        nodes = sorted(list(self.graph.nodes()))
        adjacency_matrix = pd.DataFrame(0, index=nodes, columns=nodes)
        for edge in self.graph.edges():
            from_user, to_user = edge
            amount = self.graph.get_edge_data(*edge)["weight"]
            adjacency_matrix.at[from_user, to_user] = amount
        adjacency_matrix.to_csv("graph.csv")

        # Save user debts to a file
        with open("user_debts.txt", "w") as file:
            for user, debt in self.total_debt.items():
                file.write(f"{user},{debt}\n")



    def load(self):
        self.total_debt = {}
        # Load users and debts data from CSV files
        self.users_df = pd.read_csv("users.csv")
        self.users = list(self.users_df["Name"])

        self.debts = pd.read_csv("debts.csv")

        # Load graph data from CSV file
        graph_df = pd.read_csv("graph.csv", index_col=0, header=0)
        self.graph = nx.DiGraph(graph_df.values)
        self.graph = nx.relabel_nodes(self.graph, dict(enumerate(graph_df.columns)))

        # Load user debts from a file
        with open("user_debts.txt", "r") as file:
            for line in file:
                user, debt = line.strip().split(",")
                self.total_debt[user] = float(debt)

        # Display a message confirming that everything has been loaded in
        #tk.messagebox.showinfo("Success", f"All debts have been loaded in.")



    def show_debts(self):
        self.load()
        # Create a new window to show the table
        table_window = tk.Toplevel(self.root_window)

        # Load the debts from the debts.csv file into a pandas dataframe
        debts_df = pd.read_csv("debts.csv")

        # Create a treeview widget to display the debts
        tree = ttk.Treeview(table_window, columns=("From", "To", "Amount"))

        # Set the headings for the columns
        tree.heading("From", text="From")
        tree.heading("To", text="To")
        tree.heading("Amount", text="Amount")

        # Insert the debts into the treeview
        for index, row in debts_df.iterrows():
            tree.insert("", "end", text=index, values=(row["From"], row["To"], f"${row['Amount']:.2f}"))

        # grid the treeview into the window
        tree.grid()

        # Set the window title
        table_window.title("Debt Log")



    def show_graph(self):
        self.load()
        # Create a new window to show the graph
        graph_window = tk.Toplevel(self.root_window)

        # Load the data from the graph.csv file into a pandas dataframe
        graph_df = pd.read_csv("graph.csv", index_col=0)

        # Create a treeview widget to display the data
        tree = ttk.Treeview(graph_window, columns=graph_df.columns.tolist())

        # Set the headings for the columns
        for column in graph_df.columns:
            tree.heading(column, text=column)

        # Insert the data into the treeview
        for index, row in graph_df.iterrows():
            tree.insert("", "end", text=index, values=row.tolist())

        # grid the treeview into the window
        tree.grid()

        # Set the window title
        graph_window.title("Debt Table")



    def clear_data(self):
        self.load()
        # Ask the user to confirm if they want to clear the data
        confirm = messagebox.askyesno("Clear Data", "Are you sure you want to clear all data?")

        if confirm:
            # Clear debts dataframe
            self.debts = pd.DataFrame(columns=["From", "To", "Amount"])

            # Clear total debt
            self.total_debt = {}

            # Clear graph
            self.graph.clear()

            # Clear users list
            self.users = []

            # Write empty dataframe to debts CSV file
            with open("debts.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerows([self.debts.columns.values.tolist()])

            # Display a message confirming that the data has been cleared
            messagebox.showinfo("Success", "All data has been cleared.")
            self.save()



    def sort_users_by_debt(self):

        self.load()
        # Create a max heap to store the users based on their total debt
        max_heap = MaxHeap()
        # Iterate over each user and their total debt
        for user, debt in self.total_debt.items():
            # Create a tuple with the negative value of the debt (to use as a priority) and the user
            user_debt = (-debt, user)
            # Insert the user_debt tuple into the max heap
            max_heap.insert(user_debt)

        # Create a new window to display the sorted users
        sorted_users_window = tk.Toplevel(self.root_window)

        # Create a treeview widget to display the sorted users
        tree = ttk.Treeview(sorted_users_window, columns=("User", "Debt"))

        # Set the headings for the columns
        tree.heading("User", text="User")
        tree.heading("Debt", text="Debt")

        # Insert the sorted users into the treeview
        while not max_heap.is_empty():
            debt, user = max_heap.extract_max()
            tree.insert("", "end", text=user, values=(user, f"${-debt:.2f}"))

        # Grid the treeview into the window
        tree.grid()

        # Set the window title
        sorted_users_window.title("Users Sorted by Debt")





'''
Problems:



'''
