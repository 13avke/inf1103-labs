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

    # 5. Enforce business rules: reject negative numbers and quantities greater than 500
    if quantity < 0:
        print(f"  ERROR: Negative quantity ({quantity}) is not allowed. Entry rejected.\n")
        failed_entries += 1
        continue
    # elif quantity > 500:
    #     print(f"  ERROR: Quantity ({quantity}) exceeds maximum limit of 500. Entry rejected.\n")
    #     failed_entries += 1
    #     continue

    # 6. Manage state
    inventory_total += quantity
    # 7. Trigger Overstock Alert if total exceeds 500 units
    if inventory_total > 500:
        print("ERROR: Overstock alert! Inventory exceeds 500 units.\n")
        break
    else:
        print(f"  Accepted. Current inventory total: {inventory_total}\n")


if user_input.lower() == "quit":
    print("\n=== Final Report ===")
    print(f"Total Units Processed: {inventory_total}")
    print(f"Number of Failed/Rejected Entries: {failed_entries}")