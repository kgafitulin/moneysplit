import tkinter as tk
from tkinter import simpledialog, messagebox

class Person:
    def __init__(self, name):
        self.name = name

class Payment:
    def __init__(self, amount, payer, involved):
        self.amount = amount
        self.payer = payer
        self.involved = involved

class Group:
    def __init__(self, name):
        self.name = name
        self.people = []
        self.payments = []

    def add_person(self, person):
        self.people.append(person)

    def add_payment(self, payment):
        self.payments.append(payment)

    def calculate_debts(self):
        debts = {p.name: {q.name: 0 for q in self.people} for p in self.people}
        for payment in self.payments:
            share = payment.amount / len(payment.involved)
            for person in payment.involved:
                if person != payment.payer:
                    debts[person.name][payment.payer.name] += share
        return debts

    def calculate_optimal_payments(self):
        pairwise = self.calculate_debts()
        # Compute net balances
        net = {}
        for name in pairwise:
            net[name] = sum(pairwise[name].values())  # what they owe
            for other in pairwise:
                if other != name:
                    net[name] -= pairwise[other][name]  # subtract what is owed to them
        # Debtors: positive net (owe money), Creditors: negative net (owed money)
        debtors = sorted([(name, net[name]) for name in net if net[name] > 0], key=lambda x: -x[1])
        creditors = sorted([(name, -net[name]) for name in net if net[name] < 0], key=lambda x: -x[1])
        transactions = []
        i = 0
        j = 0
        while i < len(debtors) and j < len(creditors):
            debtor, debt = debtors[i]
            creditor, credit = creditors[j]
            transfer = min(debt, credit)
            if transfer > 0.01:  # avoid tiny amounts
                transactions.append((debtor, creditor, transfer))
            debtors[i] = (debtor, debt - transfer)
            creditors[j] = (creditor, credit - transfer)
            if debtors[i][1] < 0.01:
                i += 1
            if creditors[j][1] < 0.01:
                j += 1
        return transactions

class GroupPaymentGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Group Payment Splitter")
        self.geometry("600x400")
        self.group = None
        self.create_widgets()

    def create_widgets(self):
        # Frame for buttons
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.TOP, fill=tk.X)

        self.btn_create_group = tk.Button(button_frame, text="Create Group", command=self.create_group)
        self.btn_create_group.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_add_person = tk.Button(button_frame, text="Add Person", command=self.add_person)
        self.btn_add_person.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_add_payment = tk.Button(button_frame, text="Add Payment", command=self.add_payment)
        self.btn_add_payment.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_show_debts = tk.Button(button_frame, text="Show Debts", command=self.show_debts)
        self.btn_show_debts.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_show_optimal = tk.Button(button_frame, text="Show Optimal Payments", command=self.show_optimal)
        self.btn_show_optimal.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_save = tk.Button(button_frame, text="Save Results", command=self.save_results)
        self.btn_save.pack(side=tk.LEFT, padx=5, pady=5)

        # Text area for output
        self.text_output = tk.Text(self, height=20, width=70, wrap=tk.WORD)
        self.text_output.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Scrollbar for text
        scrollbar = tk.Scrollbar(self.text_output)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_output.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text_output.yview)

    def create_group(self):
        name = simpledialog.askstring("Create Group", "Enter group name:", parent=self)
        if name:
            self.group = Group(name)
            self.text_output.insert(tk.END, f"Group '{name}' created.\n")
            self.text_output.see(tk.END)

    def add_person(self):
        if not self.group:
            messagebox.showerror("Error", "Create a group first.", parent=self)
            return
        name = simpledialog.askstring("Add Person", "Enter person name:", parent=self)
        if name:
            if any(p.name == name for p in self.group.people):
                messagebox.showerror("Error", "Person already exists.", parent=self)
                return
            person = Person(name)
            self.group.add_person(person)
            self.text_output.insert(tk.END, f"Person '{name}' added.\n")
            self.text_output.see(tk.END)

    def add_payment(self):
        if not self.group:
            messagebox.showerror("Error", "Create a group first.", parent=self)
            return
        if len(self.group.people) == 0:
            messagebox.showerror("Error", "Add people to the group first.", parent=self)
            return
        amount_str = simpledialog.askstring("Add Payment", "Enter amount:", parent=self)
        if not amount_str:
            return
        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Error", "Invalid amount.", parent=self)
            return
        
        # Select payer from list
        payer_name = self.select_person("Select Payer")
        if not payer_name:
            return
        payer = next((p for p in self.group.people if p.name == payer_name), None)
        
        # Select involved people from list
        involved_names = self.select_multiple_people("Select Involved People")
        if not involved_names or len(involved_names) == 0:
            messagebox.showerror("Error", "Select at least one person.", parent=self)
            return
        
        involved = [next((p for p in self.group.people if p.name == name)) for name in involved_names]
        
        payment = Payment(amount, payer, involved)
        self.group.add_payment(payment)
        self.text_output.insert(tk.END, "Payment added.\n")
        self.text_output.see(tk.END)

    def select_person(self, title):
        """Show dialog to select a single person from the group."""
        if not self.group or len(self.group.people) == 0:
            return None
        
        dialog = tk.Toplevel(self)
        dialog.title(title)
        dialog.geometry("300x250")
        dialog.resizable(False, False)
        
        tk.Label(dialog, text=title, font=("Arial", 12, "bold")).pack(pady=10)
        
        selected_name = tk.StringVar()
        
        # Create frame for listbox and scrollbar
        frame = tk.Frame(dialog)
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(frame, height=10, yscrollcommand=scrollbar.set)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        for person in self.group.people:
            listbox.insert(tk.END, person.name)
        
        # Set first item as selected by default
        if listbox.size() > 0:
            listbox.selection_set(0)
        
        def confirm():
            selection = listbox.curselection()
            if selection:
                selected_name.set(self.group.people[selection[0]].name)
            dialog.destroy()
        
        def on_double_click(event):
            confirm()
        
        listbox.bind("<Double-Button-1>", on_double_click)
        
        tk.Button(dialog, text="Confirm", command=confirm, bg="lightblue").pack(pady=10, padx=10, fill=tk.X)
        
        dialog.transient(self)
        dialog.grab_set()
        self.wait_window(dialog)
        
        return selected_name.get() if selected_name.get() else None

    def select_multiple_people(self, title):
        """Show dialog to select multiple people from the group."""
        if not self.group or len(self.group.people) == 0:
            return []
        
        dialog = tk.Toplevel(self)
        dialog.title(title)
        dialog.geometry("350x400")
        dialog.resizable(False, False)
        
        tk.Label(dialog, text=title, font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(dialog, text="(Click to select/deselect)", font=("Arial", 9)).pack()
        
        # Use Listbox with MULTIPLE selection mode
        frame = tk.Frame(dialog)
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(frame, height=15, selectmode=tk.MULTIPLE, yscrollcommand=scrollbar.set)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        for person in self.group.people:
            listbox.insert(tk.END, person.name)
        
        # Select first item by default
        if listbox.size() > 0:
            listbox.selection_set(0)
        
        selected_people = []
        
        def confirm():
            nonlocal selected_people
            selections = listbox.curselection()
            selected_people = [self.group.people[i].name for i in selections]
            dialog.destroy()
        
        tk.Button(dialog, text="Confirm", command=confirm, bg="lightgreen", font=("Arial", 11)).pack(pady=10, padx=10, fill=tk.X)
        
        dialog.transient(self)
        dialog.grab_set()
        self.wait_window(dialog)
        
        return selected_people

    def show_debts(self):
        if not self.group:
            messagebox.showerror("Error", "Create a group first.", parent=self)
            return
        pairwise = self.group.calculate_debts()
        self.text_output.insert(tk.END, "\nDebts:\n")
        has_debts = False
        for debtor in pairwise:
            for creditor in pairwise[debtor]:
                amt = pairwise[debtor][creditor]
                if amt > 0:
                    self.text_output.insert(tk.END, f"{debtor} owes {creditor} {amt:.2f}\n")
                    has_debts = True
        if not has_debts:
            self.text_output.insert(tk.END, "No debts.\n")
        self.text_output.see(tk.END)

    def show_optimal(self):
        if not self.group:
            messagebox.showerror("Error", "Create a group first.", parent=self)
            return
        transactions = self.group.calculate_optimal_payments()
        self.text_output.insert(tk.END, "\nOptimal payments:\n")
        if transactions:
            for debtor, creditor, amt in transactions:
                self.text_output.insert(tk.END, f"{debtor} pays {creditor} {amt:.2f}\n")
        else:
            self.text_output.insert(tk.END, "No payments needed.\n")
        self.text_output.see(tk.END)

    def save_results(self):
        if not self.group:
            messagebox.showerror("Error", "Create a group first.", parent=self)
            return
        filename = f"{self.group.name}_results.txt"
        with open(filename, 'w') as f:
            f.write(f"Group: {self.group.name}\n\n")
            f.write("People:\n")
            for p in self.group.people:
                f.write(f"- {p.name}\n")
            f.write("\nPayments:\n")
            for pay in self.group.payments:
                involved_names = [p.name for p in pay.involved]
                f.write(f"- {pay.amount:.2f} paid by {pay.payer.name} for {', '.join(involved_names)}\n")
            f.write("\nDebts:\n")
            pairwise = self.group.calculate_debts()
            has_debts = False
            for debtor in pairwise:
                for creditor in pairwise[debtor]:
                    amt = pairwise[debtor][creditor]
                    if amt > 0:
                        f.write(f"{debtor} owes {creditor} {amt:.2f}\n")
                        has_debts = True
            if not has_debts:
                f.write("No debts.\n")
            f.write("\nOptimal payments:\n")
            transactions = self.group.calculate_optimal_payments()
            if transactions:
                for debtor, creditor, amt in transactions:
                    f.write(f"{debtor} pays {creditor} {amt:.2f}\n")
            else:
                f.write("No payments needed.\n")
        messagebox.showinfo("Saved", f"Results saved to {filename}", parent=self)

def main():
    app = GroupPaymentGUI()
    app.mainloop()

if __name__ == "__main__":
    main()