"""
Smart Inventory Auditor 
INF1103 Lab 2
2605565 
"""

# 1. Initialize the inventory to zero at the start
inventory_total = 0
failed_entries = 0

print("=== Smart Inventory Auditor ===")
print("Enter stock quantities one at a time. Type 'quit' to stop.\n")

# 2. Run in a continuous loop until the user types 'quit'

while True:
    user_input = input("Enter stock quantity: ").strip()

    # Exit condition
    if user_input.lower() == "quit":
        break

    # 4. Handle invalid input using try-except
    try:
    # 3. Accept stock values as integers
        quantity = int(user_input)
    except ValueError:
        print(f"  ERROR: '{user_input}' is not a valid whole number. Entry rejected.\n")
        failed_entries += 1
        continue

    # 5. Enforce business rules: reject negative numbers
    if quantity < 0:
        print(f"  ERROR: Negative quantity ({quantity}) is not allowed. Entry rejected.\n")
        failed_entries += 1
        continue
    
    # 6. Manage state
    inventory_total += quantity
    print(f"  Accepted. Current inventory total: {inventory_total}\n")

    # 7. Trigger Overstock Alert if total exceeds 500 units
    if inventory_total > 500:
        print("ERROR: Overstock alert! Inventory exceeds 500 units.\n")
        break


if user_input.lower() == "quit":
    print("\n=== Final Report ===")
    print(f"Total Units Processed: {inventory_total}")
    print(f"Number of Failed/Rejected Entries: {failed_entries}")