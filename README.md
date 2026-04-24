# Group Payment Splitter

A simple command-line program to help split payments in a group.

## Features

- Create a group
- Add people to the group
- Add payments with amount, payer, and involved members
- Calculate and display personal debts (who owes whom how much)
- Calculate optimal payments to minimize transactions
- Save results to a text file

## How to Run

1. Ensure you have Python installed.
2. Run `python main.py` in the project directory.

## Usage

Follow the on-screen menu to:
1. Create a group
2. Add people
3. Add payments
4. View debts (pairwise)
5. View optimal payments
6. Save results to file
7. Exit

## Debt Calculation

The program calculates pairwise debts based on payments.
- Shows who owes whom and the amount.

## Optimal Payments

Calculates the minimal set of transactions to settle all debts.

## Saving Results

Saves group details, payments, debts, and optimal payments to a file named `{group_name}_results.txt`.
