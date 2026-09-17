"""
Modular Inventory Auditor 
INF1103 Lab 3
2605565 
"""

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
 
 
def generate_report(total_deliveries, total_units, failed_attempts):
    """Prints the final summary."""
    print("\n=== Final Report ===")
    print(f"Total Deliveries Processed: {total_deliveries}")
    print(f"Total Units Processed: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")

# 1. Initialize the inventory to zero at the start
inventory_total = 0
failed_entries = 0
deliveries_processed = 0

print("=== Modular Inventory Auditor ===")
print("Enter stock quantities one at a time. Type 'quit' to stop.\n")

# 2. Run in a continuous loop until the user types 'quit'

while True:
    result = get_valid_input()
 
    if result == "quit":
        break
 
    quantity = result  # a valid, non-negative integer
 
    # Check what the total WOULD be before committing this delivery,
    # so a rejected/overstocking delivery never gets added to
    # inventory_total (and never shows up in the final report)
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
        deliveries_processed += 1
        print(f"  Accepted. Quantity: {quantity} | Tax (10%): {tax:.2f}")
        print(f"  Current inventory total: {inventory_total}\n")

generate_report(deliveries_processed, inventory_total, failed_entries)