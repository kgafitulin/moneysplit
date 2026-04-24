# Group Payment Splitter

A user-friendly GUI program to help split payments in a group.

## Features

- Create a group
- Add people to the group
- Add payments with amount, payer, and involved members
- Calculate and display personal debts (who owes whom how much)
- Calculate optimal payments to minimize transactions
- Save results to a text file

## How to Run

1. Ensure you have Python with Tkinter installed (usually built-in).
2. Run `python main.py` in the project directory.

## Usage

Use the buttons in the GUI:
- **Create Group**: Enter a group name.
- **Add Person**: Add a person to the group.
- **Add Payment**: Enter payment details (amount, payer, involved names).
- **Show Debts**: Display pairwise debts.
- **Show Optimal Payments**: Display minimal transactions to settle debts.
- **Save Results**: Save all data to a file.

Results are shown in the text area at the bottom.

## Debt Calculation

Calculates pairwise debts based on payments.
- Shows who owes whom and the amount.

## Optimal Payments

Calculates the minimal set of transactions to settle all debts.

## Saving Results

Saves group details, payments, debts, and optimal payments to `{group_name}_results.txt`.
