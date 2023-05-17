import tkinter as tk
from tkinter import simpledialog, messagebox
import pandas as pd
import networkx as nx
import csv
from tkinter import filedialog
from tkinter import ttk
from tkinter import PhotoImage
from maxheap import MaxHeap
import datetime

class ssmethods:

    def save(self, users_file = "users.csv", debts_file = "debts.csv", graph_file="graph.csv", user_debts_file="user_debts.txt"):
        # Save user names to users.csv
        pd.DataFrame(self.users, columns=["Name"]).to_csv(users_file, index=False)

        # Save debts to debts.csv
        self.debts.to_csv(debts_file, index=False)

        # Save graph to graph.csv
        nodes = sorted(list(self.graph.nodes()))
        adjacency_matrix = pd.DataFrame(0, index=nodes, columns=nodes)
        for edge in self.graph.edges():
            from_user, to_user = edge
            amount = self.graph.get_edge_data(*edge)["weight"]
            adjacency_matrix.at[from_user, to_user] = amount
        adjacency_matrix.to_csv(graph_file)

        # Save user debts to a file
        with open(user_debts_file, "w") as file:
            for user, debt in self.total_debt.items():
                file.write(f"{user},{debt}\n")

    def load(self, users_file = "users.csv", debts_file = "debts.csv", graph_file="graph.csv", user_debts_file="user_debts.txt"):
        self.total_debt = {}
        # Load users and debts data from CSV files
        self.users_df = pd.read_csv(users_file)
        self.users = list(self.users_df["Name"])

        self.debts = pd.read_csv(debts_file)

        # Load graph data from CSV file
        graph_df = pd.read_csv(graph_file, index_col=0, header=0)
        self.graph = nx.DiGraph(graph_df.values)
        self.graph = nx.relabel_nodes(self.graph, dict(enumerate(graph_df.columns)))

        # Load user debts from a file
        with open(user_debts_file, "r") as file:
            for line in file:
                user, debt = line.strip().split(",")
                self.total_debt[user] = float(debt)

    def add_user(self, user_name = None):
        self.load()
        
        # Error Checking
        if user_name == None:
            return False
        # Check if the user name already exists
        if user_name in self.users:
            tk.messagebox.showerror("Error", "User already exists.")
            return False
        
        # Add the user to the users list
        self.users.append(user_name)
    
        # Add the user as a node to the graph
        self.graph.add_node(user_name)
    
        # Display a message confirming that the user has been added
        tk.messagebox.showinfo("Success", f"User {user_name} has been added.")
        self.save()
        
    
    def remove_user(self, user_name = None):
        self.load()
        
        # Error Checking
        if user_name == None:
            return False
        # Check if the user name already exists
        if user_name not in self.users:
            tk.messagebox.showerror("Error", "User does not exist.")
            return False
        
    
        # Add the user to the users list
        self.users.remove(user_name)
    
        # Add the user as a node to the graph
        self.graph.remove_node(user_name)
    
        # Display a message confirming that the user has been added
        tk.messagebox.showinfo("Success", f"User {user_name} has been removed.")
        self.save()
    
    
    
    def add_debt(self, from_user = None, to_user = None, amount = None):
        self.load()
        
        # Add debt to dataframe
        now = datetime.datetime.now()
        timestamp= now.strftime("%Y-%m-%d %H:%M")
        self.debts = self.debts.append({
            "Timestamp": timestamp,
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
        
        
    
    def remove_debt(self, from_user = None, to_user = None, amount = None):
        self.load()
    
        # Add debt to dataframe
        now = datetime.datetime.now()
        timestamp= now.strftime("%Y-%m-%d %H:%M")
        self.debts = self.debts.append({
            "Timestamp": timestamp,
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
            # Check if the user name already exists
            while temp not in self.users:
                tk.messagebox.showerror("Error", "User does not exist.")
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
            amount = round(weighted_cost,2)

            # Add debt to dataframe
            self.add_debt(from_user, to_user, amount)

        self.save()
    
    
    
    
    def show_debts(self, root_window = None):
        self.load()
        # Create a new window to show the table
        table_window = tk.Toplevel(root_window)
    
        # Load the debts from the debts.csv file into a pandas dataframe
        debts_df = pd.read_csv("debts.csv")
    
        # Create a treeview widget to display the debts
        tree = ttk.Treeview(table_window, columns=("Timestamp","From", "To", "Amount"))
    
        # Set the headings for the columns
        tree.heading("Timestamp", text="Timestamp")
        tree.heading("From", text="From")
        tree.heading("To", text="To")
        tree.heading("Amount", text="Amount")
    
        # Insert the debts into the treeview
        for index, row in debts_df.iterrows():
            tree.insert("", "end", text=index, values=(row["Timestamp"], row["From"], row["To"], f"${row['Amount']:.2f}"))
    
        # grid the treeview into the window
        tree.grid()
    
        # Set the window title
        table_window.title("Debt Log")
    
    
    
    def show_graph(self, root_window = None):
        self.load()
        
        graph_window = tk.Toplevel(root_window)
    
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
            self.debts = pd.DataFrame(columns=["Timestamp","From", "To", "Amount"])
    
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
    
    
    
    def sort_users_by_debt(self, root_window = None):
    
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
        sorted_users_window = tk.Toplevel(root_window)
    
        # Create a treeview widget to display the sorted users
        tree = ttk.Treeview(sorted_users_window, columns=("Debt"))
    
        # Set the headings for the columns
        tree.heading("#0", text="User")
        tree.heading("Debt", text="Debt")

        # Create a set to keep track of the displayed users
        displayed_users = set()
    
        # Insert the sorted users into the treeview
        while not max_heap.is_empty():
            debt, user = max_heap.find_max()

            # Check if the user has already been displayed
            if user not in displayed_users:
                displayed_users.add(user)
                tree.insert("", "end", text=user, values=(f"${-debt:.2f}",))

        # Grid the treeview into the window
        tree.grid()

        # Set the window title
        sorted_users_window.title("Users Sorted by Debt")

    def individual_debts(self, root_window = None):
        self.load()
        user = tk.simpledialog.askstring("Individual Debts", "Who's debt information do you want to view:")

        # Check if the user name doesn't exists
        if user not in self.users:
            tk.messagebox.showerror("Error", "User does not exist.")
            return
        
        # Create a new window to show the table
        table_window = tk.Toplevel(root_window)

        # Load the debts from the debts.csv file into a pandas dataframe
        debts_df = pd.read_csv("debts.csv")

        # Subsets the debts file to just the specified user
        debts_df = debts_df.loc[(debts_df['From'] == user) | (debts_df['To'] == user)]

        # Create a treeview widget to display the debts
        tree = ttk.Treeview(table_window, columns=("Timestamp", "From", "To", "Amount"))

        # Set the headings for the columns
        tree.heading("Timestamp", text="Timestamp")
        tree.heading("From", text="From")
        tree.heading("To", text="To")
        tree.heading("Amount", text="Amount")

        # Insert the debts into the treeview
        total_amount = 0
        for index, row in debts_df.iterrows():
            if row["From"] == user:
                amount = -row["Amount"]
            else:
                amount = row["Amount"]
            tree.insert("", "end", text=index+1, values=(row["Timestamp"], row["From"], row["To"], f"${amount:.2f}"))
            total_amount += amount

        # Add the total amount owed by the individual to the bottom of the treeview
        tree.insert("", "end", text="Total", values=("", "", "", f"${total_amount:.2f}"))


        # grid the treeview into the window
        tree.grid()

        # Set the window title
        table_window.title("Individual Data")

        # Update the window to show the treeview
        table_window.update()
