"""
Modular Inventory Auditor 
INF1103 Lab 4
2605565 
"""

import os

# inventory.txt always lives next to this script, no matter which
# folder the program is run from
INVENTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventory.txt")

# --- Functions ---

def get_valid_input():
    """Handles the prompt, validates input, and returns a valid integer
    or the string 'quit'."""
    global failed_entries
 
    while True:
        user_input = input("Enter stock quantity: ").strip()
 
        # Exit condition
        if user_input.lower() == "quit":
            return "quit"
 
        # Handle invalid input using try-except
        try:
            quantity = int(user_input)
        except ValueError:
            print(f"  ERROR: '{user_input}' is not a valid whole number. Entry rejected.\n")
            failed_entries += 1
            continue
 
        # Enforce business rules: reject negative numbers
        if quantity < 0:
            print(f"  ERROR: Negative quantity ({quantity}) is not allowed. Entry rejected.\n")
            failed_entries += 1
            continue
 
        return quantity
 
 
def process_delivery(current_total, new_value):
    """Calculates the new inventory total and returns it."""
    return current_total + new_value
 
 
def calculate_tax(amount):
    """Returns 10% tax on the given delivery amount."""
    return amount * 0.10
 
 
def generate_report(transaction_history, total_units, failed_attempts):
    """Prints the final summary."""
    print("\n=== Final Report ===")
    print(f"Total Deliveries Recorded: {len(transaction_history)}")
    print(f"Total Units in Inventory: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")
    print(f"Transaction History: {transaction_history}")


def load_inventory():
    #Reads the saved total and transaction history from inventory.txt.
    if not os.path.exists(INVENTORY_FILE):
        print("No inventory file found. Starting with an empty inventory.\n")
        return 0, []

    try:
        with open(INVENTORY_FILE, "r", encoding="utf-8-sig") as file:
            lines = [line.strip() for line in file.readlines() if line.strip() != ""]

        if not lines:
            return 0, []

        total = int(lines[0])
        history = [int(line) for line in lines[1:]]
        return total, history
    except ValueError:
        print("WARNING: inventory.txt is not in the expected format. Starting with an empty inventory.\n")
        return 0, []


def save_inventory(total, history):
    """Writes the final total and the transaction history to inventory.txt,
    in the same format load_inventory() reads."""
    with open(INVENTORY_FILE, "w", encoding="utf-8") as file:
        file.write(f"{total}\n")
        for amount in history:
            file.write(f"{amount}\n")
    print(f"\nInventory saved to {INVENTORY_FILE}")

# 1. Load the inventory saved from the previous run (or start empty)
inventory_total, transaction_history = load_inventory()
failed_entries = 0

print("=== Modular Inventory Auditor ===")
print(f"Starting inventory total: {inventory_total}")
print(f"Previous transactions: {transaction_history}")
print("Enter stock quantities one at a time. Type 'quit' to stop.\n")

# 2. Run in a continuous loop until the user types 'quit'

while True:
    result = get_valid_input()
 
    if result == "quit":
        break
 
    quantity = result  # a valid, non-negative integer
    prospective_total = process_delivery(inventory_total, quantity)
 
    # Trigger Overstock Alert if the delivery would push the total over 500 units
    if prospective_total > 500:
        print(f"  ERROR: Overstock alert! Adding {quantity} units would bring the total to "
              f"{prospective_total}, exceeding the 500-unit limit. Entry rejected.\n")
        failed_entries += 1
        break
    else:
        tax = calculate_tax(quantity)
        inventory_total = prospective_total
        transaction_history.append(quantity)
        print(f"  Accepted. Quantity: {quantity} | Tax (10%): {tax:.2f}")
        print(f"  Current inventory total: {inventory_total}\n")

generate_report(transaction_history, inventory_total, failed_entries)

# 3. Write-back: save the final total and history for the next run
save_inventory(inventory_total, transaction_history)