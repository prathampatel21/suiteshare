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
        root_window.geometry("545x520")
        root_window.configure(bg="#4C7330")
        self.load()

        # Image Label
        self.image = PhotoImage(file="suiteshare.png")
        self.image = self.image.subsample(2, 2)
        self.label_image = tk.Label(root_window, image=self.image, bg="#4C7330")
        self.label_image.place(x=67)

        # User Entry Box
        self.user_entry = tk.Entry(root_window, font=("Segoe UI", 16), bg="#D9B777", fg="#4C7330", width = 15)
        self.user_entry.grid(row=2, column=0, padx=10, pady=(125, 30), sticky="we")

        # Add and Remove User Button
        self.button_add_user = tk.Button(root_window, text="Add User", font=("Segoe UI", 16, "bold"), bg="#D9B777", fg="#4C7330", command=self.add_user, pady = 2)
        self.button_add_user.grid(row=2, column=1, padx=10, pady=(125, 30), sticky="we")

        self.button_remove_user = tk.Button(root_window, text="Remove User", font=("Segoe UI", 16, "bold"), bg="#D9B777", fg="#4C7330", command=self.remove_user, pady = 2, width=13)
        self.button_remove_user.grid(padx=(10,90), pady=(125, 30), sticky="we")
        self.button_remove_user.place(x=374, y=125, width=160)

        # Debtor Entry Widget
        self.debtor_label = tk.Label(root_window, text="Debtor:", font=("Segoe UI", 16, "bold"), bg="#4C7330", fg="#D9B777")
        self.debtor_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.debtor_entry = tk.Entry(root_window, font=("Segoe UI", 16), bg="#D9B777", fg="#4C7330", width=15)
        self.debtor_entry.grid(row=3, column=1, padx=10, pady=10, sticky="we")

        # Creditor Entry Widget
        self.creditor_label = tk.Label(root_window, text="Creditor:", font=("Segoe UI", 16, "bold"), bg="#4C7330", fg="#D9B777")
        self.creditor_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.creditor_entry = tk.Entry(root_window, font=("Segoe UI", 16), bg="#D9B777", fg="#4C7330", width=15)
        self.creditor_entry.grid(row=4, column=1, padx=10, pady=10, sticky="we")

        # Amount Entry Widget
        self.amount_label = tk.Label(root_window, text="Amount:", font=("Segoe UI", 16, "bold"), bg="#4C7330", fg="#D9B777")
        self.amount_label.grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.amount_entry = tk.Entry(root_window, font=("Segoe UI", 16), bg="#D9B777", fg="#4C7330", width=15)
        self.amount_entry.grid(row=5, column=1, padx=10, pady=10, sticky="we")

        # Add Debt and Remove Debt Buttons
        self.add_debt_button = tk.Button(root_window, text="Add Debt", font=("Segoe UI", 16, "bold"), bg="#D9B777", fg="#4C7330", command=self.add_debt, pady = 2, width=13)
        self.add_debt_button.grid(padx=(10,90), pady=(10, 10), sticky="we")
        self.add_debt_button.place(x=374, y=220, width=160)

        self.remove_debt_button = tk.Button(root_window, text="Remove Debt", font=("Segoe UI", 16, "bold"), bg="#D9B777", fg="#4C7330", command=self.remove_debt, pady = 2, width=13)
        self.remove_debt_button.grid(padx=(10,90), pady=(10, 10), sticky="we")
        self.remove_debt_button.place(x=374, y=272, width=160)

        # Settle Debt and Calculate Split Tax Buttons
        self.button_clear_debts = tk.Button(root_window, text="Settle Debt", font=("Segoe UI", 16, "bold"), bg="#D9B777", fg="#4C7330", command=self.clear_debt, pady = 2)
        self.button_clear_debts.grid(padx=10, pady=(40,10), sticky="we")
        self.button_clear_debts.place(x=100, y=370, width=160)

        self.button_split_tax = tk.Button(root_window, text="Split Tax", font=("Segoe UI", 16, "bold"), bg="#D9B777", fg="#4C7330", command=self.split_tax, pady = 2, width=13)
        self.button_split_tax.grid(padx=10, pady=(40,10), sticky="we",columnspan=1)
        self.button_split_tax.place(x=285, y=370, width=160)

        # Debt Log and Debt Table Buttons
        self.button_show_debts = tk.Button(root_window, text="Debt Log", font=("Segoe UI", 16, "bold"), bg="#D9B777", fg="#4C7330", command=self.show_debts, pady = 2)
        self.button_show_debts.grid(padx=10, pady=10, sticky="we")
        self.button_show_debts.place(x=12, y=420, width=160)

        self.button_show_graph = tk.Button(root_window, text="Debt Table", font=("Segoe UI", 16, "bold"), bg="#D9B777", fg="#4C7330", command=self.show_graph, pady = 2)
        self.button_show_graph.grid(padx=10, pady=10, sticky="we")
        self.button_show_graph.place(x=193, y=420, width=160)

        # Clear Data Button
        self.button_clear_data = tk.Button(root_window, text="Clear Data", font=("Segoe UI", 16, "bold"), bg="#D9B777", fg="#4C7330", command=self.clear_data, pady = 2)
        self.button_clear_data.grid(row=10, column=1, padx=10, pady=(135,30), sticky="we")

        # Sort Users Button
        self.button_sort_users = tk.Button(root_window, text="Sort Users", font=("Segoe UI", 16, "bold"), bg="#D9B777", fg="#4C7330", command=self.sort_users_by_debt, pady=2, width=13)
        self.button_sort_users.grid(padx=(10, 90), pady=(10, 10), sticky="we")
        self.button_sort_users.place(x=374, y=420, width=160)

        # Create data structures
        self.users = []
        self.debts = pd.DataFrame(columns=["From", "To", "Amount"])
        self.total_debt = {}

        # Create directed graph
        self.graph = nx.DiGraph()



# SuiteShare Methods

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



    def add_user(self):
        self.load()
        # Get user name from user input
        user_name = self.user_entry.get()

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
        self.user_entry.delete(0, tk.END)



    def remove_user(self):
        self.load()
        # Get user name from user input
        user_name = self.user_entry.get()

        # Check if the user name doesn't exists
        if user_name not in self.users:
            tk.messagebox.showerror("Error", "User does not exist.")
            return

        # Remove the user from the users list
        self.users.remove(user_name)

        # Remove the user as a node from the graph
        self.graph.remove_node(user_name)

        # Display a message confirming that the user has been added
        tk.messagebox.showinfo("Success", f"User {user_name} has been removed.")
        self.save()
        self.user_entry.delete(0, tk.END)



    def add_debt(self):
        self.load()
        # Get debt details from user input
        from_user = self.debtor_entry.get()
        to_user = self.creditor_entry.get()
        amount = float(self.amount_entry.get())


        # Add debt to dataframe
        self.debts = self.debts.append({
            "From": from_user,
            "To": to_user,
            "Amount": amount
        }, ignore_index=True)

        # Check if the user name doesn't exists
        if from_user not in self.users:
            tk.messagebox.showerror("Error", "One or both users does not not exist.")
            return
        elif to_user not in self.users:
            tk.messagebox.showerror("Error", "One or both users does not not exist.")
            return

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
        amount = float(self.amount_entry.get())


        # Add debt to dataframe
        self.debts = self.debts.append({
            "From": from_user,
            "To": to_user,
            "Amount": -amount
        }, ignore_index=True)

        # Check if the user name doesn't exists
        if from_user not in self.users:
            tk.messagebox.showerror("Error", "One or both users does not not exist.")
            return
        elif to_user not in self.users:
            tk.messagebox.showerror("Error", "One or both users does not not exist.")
            return

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

        # Check if the user name doesn't exists
        if user not in self.users:
            tk.messagebox.showerror("Error", "User does not exist.")
            return

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



    def split_tax(self):
        self.load()

        split_users = []
        split_cost = []
        num_users = tk.simpledialog.askinteger("Total Users", "Enter the number of users to split amongst (excluding creditor)")
        creditor = tk.simpledialog.askstring("Creditor", "Enter the name of creditor")
        total_cost = tk.simpledialog.askfloat("Total Cost", "Enter the total cost of the order after taxes & fees.")
        total_tax = tk.simpledialog.askfloat("Total Tax", "Enter the total taxes/fees of the order.")
        for i in range(num_users):
            temp = tk.simpledialog.askstring("User", "Enter the name of the user to split:")
            partial_cost = tk.simpledialog.askfloat("Partial Cost", "Enter the partial cost for "  + temp)
            if partial_cost > total_cost:
                tk.messagebox.showerror("Error", "Partial cost is greater than the total cost of the order.")
                return
            split_users.append(temp)
            split_cost.append(partial_cost)

        for i in range(num_users):
            weighted_tax = (split_cost[i]/(total_cost-total_tax))*total_tax
            weighted_cost = split_cost[i]+weighted_tax

            #add debt to the graph

            # Get debt details from user input
            from_user = split_users[i]
            to_user = creditor
            amount = weighted_cost

            # Add debt to dataframe
            self.debts = self.debts.append({
                "From": from_user,
                "To": to_user,
                "Amount": amount
            }, ignore_index=True)

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


            tk.messagebox.showinfo("Success", f"The weighted cost with tax for {split_users[i]} is ${weighted_cost:.2f}")

        self.save()




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
        tree = ttk.Treeview(sorted_users_window, columns=("Debt",))

        # Set the headings for the columns
        tree.heading("#0", text="User")
        tree.heading("Debt", text="Debt")

        # Create a set to keep track of the displayed users
        displayed_users = set()

        # Insert the sorted users into the treeview
        while not max_heap.is_empty():
            debt, user = max_heap.extract_max()

            # Check if the user has already been displayed
            if user not in displayed_users:
                displayed_users.add(user)
                tree.insert("", "end", text=user, values=(f"${-debt:.2f}",))

        # Grid the treeview into the window
        tree.grid()

        # Set the window title
        sorted_users_window.title("Users Sorted by Debt")
