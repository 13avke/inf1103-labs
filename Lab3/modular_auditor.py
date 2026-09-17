"""
Modular Smart Inventory Auditor 
INF1103 Lab 3
2605565 
"""

# --- Planned functions (signatures only for now) ---
# Mapping out the inputs/outputs before writing the logic
 
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
    pass
 
 
def calculate_tax(amount):
    """Returns 10% tax on the given delivery amount."""
    pass
 
 
def generate_report(total_units, failed_attempts):
    """Prints the final summary."""
    pass

# 1. Initialize the inventory to zero at the start
inventory_total = 0
failed_entries = 0

print("=== Smart Inventory Auditor ===")
print("Enter stock quantities one at a time. Type 'quit' to stop.\n")

# 2. Run in a continuous loop until the user types 'quit'

while True:
    result = get_valid_input()
 
    if result == "quit":
        break
 
    quantity = result  # a valid, non-negative integer
 
    # Manage state
    inventory_total += quantity
    # Trigger Overstock Alert if total exceeds 500 units
    if inventory_total > 500:
        print("ERROR: Overstock alert! Inventory exceeds 500 units.\n")
        break
    else:
        print(f"  Accepted. Current inventory total: {inventory_total}\n")


print("\n=== Final Report ===")
print(f"Total Units Processed: {inventory_total}")
print(f"Number of Failed/Rejected Entries: {failed_entries}")