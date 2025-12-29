from src.models import Asset, Employee, Assignment, get_today
from src.database import Database_manager, setup_database

DB_NAME = "data.db"


def handle_add_asset(db: Database_manager) -> None:
    print("-- Add New Asset --\n")

    name_input = input("Asset Name: ")
    cat_input = input("Category: ")

    try:
        new_asset = Asset(name=name_input, category=cat_input)
        db.add_assets(new_asset)
        print("-- Asset Added Sucessfully --\n")

    except ValueError as e:
        print(f"ERROR: {e}")


def handle_update_status(db: Database_manager) -> None:
    print("\n--- Update Asset Status ---\n")
    asset_id_input = input("Asset ID: ")

    print("Options: MAINTENANCE, RETIRED")
    new_status = input("New Status: ").strip().upper()

    try:
        asset_id = int(asset_id_input)
        db.update_asset_status(asset_id, new_status)

        print(f"Asset {asset_id} updated to {new_status}")

    except ValueError as e:
        print(f"ERROR: {e}")


def handle_add_employee(db: Database_manager) -> None:
    print("-- Add New Employee --\n")

    name_input = input("Employee Name: ")
    dept_input = input("Department Name: ")

    try:
        new_employee = Employee(name=name_input, department=dept_input)
        db.add_employees(new_employee)

        print("-- Employee Added Sucessfully --\n")

    except ValueError as e:
        print(f"ERROR: {e}")


def handle_assign_asset(db: Database_manager) -> None:
    print("-- Assign Asset --\n")

    asset_id_input = input("Asset ID: ")
    emp_id_input = input("Employee ID: ")
    date_input = input("Date (YYYY-MM-DD) [Press Enter for Today]: ")

    if not asset_id_input.isdigit() or not emp_id_input.isdigit():
        print("Error: Asset ID and Employee ID must be valid numbers.")
        return

    try:
        asset_id = int(asset_id_input)
        emp_id = int(emp_id_input)

        if date_input.strip() == "":
            new_assign = Assignment(asset_id=asset_id, employee_id=emp_id)
        else:
            new_assign = Assignment(
                asset_id=asset_id, employee_id=emp_id, assigned_date=date_input
            )

        db.assign_asset(new_assign)
        print("-- Asset Assigned Sucessfully --\n")

    except ValueError as e:
        print(f"ERROR: {e}")


def handle_return_asset(db: Database_manager) -> None:
    print("-- Return Asset --\n")

    asset_id_input = input("Asset ID: ")

    today = get_today()

    if not asset_id_input.isdigit():
        print("Error: Asset ID must be a valid number (e.g., 1, 5).")
        return

    try:
        asset_id = int(asset_id_input)
        db.return_asset(asset_id, today)

        print("-- Asset Returned --\n")

    except ValueError as e:
        print(f"ERROR: {e}")


def handle_offboard_employee(db: Database_manager) -> None:
    print("--Offboard Employee --\n")

    emp_id_input = input("Employee ID:")

    if not emp_id_input.isdigit():
        print("Error: Employee ID must be a number.")
        return

    try:
        emp_id = int(emp_id_input)

        db.offboard_employee(emp_id)
        print("-- Employee offboarded --\n")

    except ValueError as e:
        print(f"ERROR: {e}")


def handle_list_assets(db: Database_manager) -> None:
    print("\n--- All Assets ---\n")
    assets = db.get_all_assets()

    print(f"{'ID':<5} | {'NAME':<20} | {'CATEGORY':<15} | {'STATUS':<12}")
    print("-" * 60)

    for asset in assets:
        print(f"{asset[0]:<5} | {asset[1]:<20} | {asset[2]:<15} | {asset[3]:<12}")


def handle_list_employees(db: Database_manager) -> None:
    print("\n--- All Employees ---\n")
    emps = db.get_all_employees()

    print(f"{'ID':<5} | {'NAME':<20} | {'DEPT':<15} | {'ACTIVE':<12}")
    print("-" * 60)

    for emp in emps:
        status = "Yes" if emp[3] == 1 else "No"
        print(f"{emp[0]:<5} | {emp[1]:<20} | {emp[2]:<15} | {status:<12}")


def get_assignments(db: Database_manager) -> None:
    print("\n--- All ASSIGNMENTS ---\n")
    rows = db.get_active_assignments()

    print(f"{'EMPLOYEE':<20} | {'ASSET':<20} | {'DATE':12}")
    print("-" * 60)

    for row in rows:
        print(f"{row[0]:<20} | {row[1]:<20} | {row[2]:<12}")


def print_menu() -> None:
    print("\n" + "=" * 40)
    print(" ASSET MANAGEMENT SYSTEM")
    print("=" * 60)
    print("1. Add New Asset")
    print("2. Add New Employee")
    print("3. Assign Asset")
    print("4. Return Asset")
    print("5. Set Asset Status (Maintenance/Retired)")
    print("6. Offboard Employee")
    print("7. View Active Assignments")
    print("8. View All Assets")
    print("9. View All Employees")
    print("0. Exit")
    print("=" * 40)


def main() -> None:
    setup_database(DB_NAME)
    db = Database_manager(DB_NAME)

    print_menu()

    while True:
        choice = input("Select Option (m for Menu):").lower()

        match choice:
            case "m":
                print_menu()
            case "1":
                handle_add_asset(db)
            case "2":
                handle_add_employee(db)
            case "3":
                handle_assign_asset(db)
            case "4":
                handle_return_asset(db)
            case "5":
                handle_update_status(db)
            case "6":
                handle_offboard_employee(db)
            case "7":
                get_assignments(db)
            case "8":
                handle_list_assets(db)
            case "9":
                handle_list_employees(db)
            case "0":
                print("Exiting....")
                break
            case _:
                print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
