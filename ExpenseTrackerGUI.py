import tkinter as tk
from tkinter import simpledialog, messagebox
import pandas as pd
import networkx as nx
import csv
from tkinter import filedialog
from tkinter import ttk
from tkinter import PhotoImage
from maxheap import MaxHeap
from SuiteShareMethods import ssmethods
import datetime


class SuiteShareGUI:
    def __init__(self, root_window):
        self.methods = ssmethods()
        self.root_window = root_window
        root_window.title("SuiteShare")
        root_window.geometry("545x520")
        root_window.configure(bg="#4C7330")
        self.methods.load()

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
        self.button_clear_debts = tk.Button(root_window, text="Settle Debt", font=("Segoe UI", 16, "bold"), bg="#D9B777", fg="#4C7330", command=self.methods.clear_debt, pady = 2)
        self.button_clear_debts.grid(padx=10, pady=(40,10), sticky="we")
        self.button_clear_debts.place(x=12, y=370, width=160)

        self.button_split_tax = tk.Button(root_window, text="Split Tax", font=("Segoe UI", 16, "bold"), bg="#D9B777", fg="#4C7330", command=self.methods.split_tax, pady = 2, width=13)
        self.button_split_tax.grid(padx=10, pady=(40,10), sticky="we",columnspan=1)
        self.button_split_tax.place(x=193, y=370, width=160)

        # Debt Log and Debt Table Buttons
        self.button_show_debts = tk.Button(root_window, text="Debt Log", font=("Segoe UI", 16, "bold"), bg="#D9B777", fg="#4C7330", command=self.show_debts, pady = 2)
        self.button_show_debts.grid(padx=10, pady=10, sticky="we")
        self.button_show_debts.place(x=12, y=420, width=160)

        self.button_show_graph = tk.Button(root_window, text="Debt Table", font=("Segoe UI", 16, "bold"), bg="#D9B777", fg="#4C7330", command=self.show_graph, pady = 2)
        self.button_show_graph.grid(padx=10, pady=10, sticky="we")
        self.button_show_graph.place(x=193, y=420, width=160)

        # Clear Data Button
        self.button_clear_data = tk.Button(root_window, text="Clear Data", font=("Segoe UI", 16, "bold"), bg="#D9B777", fg="#4C7330", command=self.methods.clear_data, pady = 2)
        self.button_clear_data.grid(row=10, column=1, padx=10, pady=(135,30), sticky="we")

        # Sort Users Button
        self.button_sort_users = tk.Button(root_window, text="Sort Users", font=("Segoe UI", 16, "bold"), bg="#D9B777", fg="#4C7330", command=self.sort_users_by_debt, pady=2, width=13)
        self.button_sort_users.grid(padx=(10, 90), pady=(10, 10), sticky="we")
        self.button_sort_users.place(x=374, y=420, width=160)

        # Show Individual User Debt Button
        self.individual_debt_button = tk.Button(root_window, text="Individual Debt", font=("Segoe UI", 16, "bold"), bg="#D9B777", fg="#4C7330", command=self.individual_debts, pady = 2, width=13)
        self.individual_debt_button.grid(padx=(10, 90), pady=(10, 10), sticky="we")
        self.individual_debt_button.place(x=374, y=370, width=160)



        # Create data collecting tools
        self.users = []
        self.debts = pd.DataFrame(columns=["From", "To", "Amount"])
        self.total_debt = {}

        # Create directed graph
        self.graph = nx.DiGraph()



    def add_user(self):
        user_name = self.user_entry.get()
        self.methods.add_user(user_name) 
        self.user_entry.delete(0,tk.END)

    def remove_user(self):
        user_name = self.user_entry.get()

        self.methods.remove_user(user_name)
        self.user_entry.delete(0,tk.END)

    def add_debt(self):
        # Get debt details from user input
        from_user = self.debtor_entry.get()
        to_user = self.creditor_entry.get()
        amount = float(self.amount_entry.get())

        self.methods.add_debt(from_user,to_user,amount)
        self.debtor_entry.delete(0, tk.END)
        self.creditor_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
    
    def remove_debt(self):
        # Get debt details from user input
        from_user = self.debtor_entry.get()
        to_user = self.creditor_entry.get()
        amount = float(self.amount_entry.get())

        self.methods.remove_debt(from_user,to_user,amount)
        self.debtor_entry.delete(0, tk.END)
        self.creditor_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)

    def show_debts(self):
        self.methods.show_debts(self.root_window)

    def show_graph(self):
        self.methods.show_graph(self.root_window)
    
    def sort_users_by_debt(self):
        self.methods.sort_users_by_debt(self.root_window)

    def individual_debts(self):
        self.methods.individual_debts(self.root_window)
