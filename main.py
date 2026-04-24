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
        # Creditors: positive net, debtors: negative
        creditors = sorted([(name, net[name]) for name in net if net[name] > 0], key=lambda x: -x[1])
        debtors = sorted([(name, -net[name]) for name in net if net[name] < 0], key=lambda x: -x[1])
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

def main():
    group = None
    while True:
        print("\n1. Create group")
        print("2. Add person")
        print("3. Add payment")
        print("4. Show debts")
        print("5. Show optimal payments")
        print("6. Save results")
        print("7. Exit")
        choice = input("Choose an option: ").strip()
        if choice == '1':
            name = input("Enter group name: ").strip()
            group = Group(name)
            print(f"Group '{name}' created.")
        elif choice == '2':
            if not group:
                print("Please create a group first.")
                continue
            name = input("Enter person name: ").strip()
            if any(p.name == name for p in group.people):
                print("Person already exists.")
                continue
            person = Person(name)
            group.add_person(person)
            print(f"Person '{name}' added to group.")
        elif choice == '3':
            if not group:
                print("Please create a group first.")
                continue
            try:
                amount = float(input("Enter payment amount: ").strip())
            except ValueError:
                print("Invalid amount.")
                continue
            payer_name = input("Enter payer name: ").strip()
            payer = next((p for p in group.people if p.name == payer_name), None)
            if not payer:
                print("Payer not found in group.")
                continue
            involved_names = input("Enter involved names (comma separated): ").strip().split(',')
            involved = []
            for name in involved_names:
                name = name.strip()
                person = next((p for p in group.people if p.name == name), None)
                if person:
                    involved.append(person)
                else:
                    print(f"Person '{name}' not found in group.")
            if len(involved) == 0:
                print("No valid involved people.")
                continue
            payment = Payment(amount, payer, involved)
            group.add_payment(payment)
            print("Payment added.")
        elif choice == '4':
            if not group:
                print("Please create a group first.")
                continue
            pairwise = group.calculate_debts()
            print("\nDebts:")
            has_debts = False
            for debtor in pairwise:
                for creditor in pairwise[debtor]:
                    amt = pairwise[debtor][creditor]
                    if amt > 0:
                        print(f"{debtor} owes {creditor} {amt:.2f}")
                        has_debts = True
            if not has_debts:
                print("No debts.")
        elif choice == '5':
            if not group:
                print("Please create a group first.")
                continue
            transactions = group.calculate_optimal_payments()
            print("\nOptimal payments:")
            if transactions:
                for debtor, creditor, amt in transactions:
                    print(f"{debtor} pays {creditor} {amt:.2f}")
            else:
                print("No payments needed.")
        elif choice == '6':
            if not group:
                print("Please create a group first.")
                continue
            filename = f"{group.name}_results.txt"
            with open(filename, 'w') as f:
                f.write(f"Group: {group.name}\n\n")
                f.write("People:\n")
                for p in group.people:
                    f.write(f"- {p.name}\n")
                f.write("\nPayments:\n")
                for pay in group.payments:
                    involved_names = [p.name for p in pay.involved]
                    f.write(f"- {pay.amount:.2f} paid by {pay.payer.name} for {', '.join(involved_names)}\n")
                f.write("\nDebts:\n")
                pairwise = group.calculate_debts()
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
                transactions = group.calculate_optimal_payments()
                if transactions:
                    for debtor, creditor, amt in transactions:
                        f.write(f"{debtor} pays {creditor} {amt:.2f}\n")
                else:
                    f.write("No payments needed.\n")
            print(f"Results saved to {filename}")
        elif choice == '7':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()