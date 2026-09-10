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


if user_input.lower() == "quit":
    print("\n=== Final Report ===")
    print(f"Total Units Processed: {inventory_total}")
    print(f"Number of Failed/Rejected Entries: {failed_entries}")