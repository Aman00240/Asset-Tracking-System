import sqlite3 as sql
from src.models import Asset, Employee, Assignment


def setup_database(db_name: str) -> None:
    with sql.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        cursor.execute("""CREATE TABLE IF NOT EXISTS assets(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT,
            status TEXT DEFAULT 'AVAILABLE'
            )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS employees(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            department TEXT,
            is_active INTEGER DEFAULT 1
            )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS assignments(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_id INTEGER,
            employee_id INTEGER,
            assigned_date TEXT,
            return_date TEXT,
            FOREIGN KEY (asset_id) REFERENCES assets(id),
            FOREIGN KEY (employee_id) REFERENCES employees(id)
            )""")


class Database_manager:
    def __init__(self, db_name: str) -> None:
        self.db_name = db_name

    def add_assets(self, asset: Asset) -> None:
        with sql.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO assets(name,category,status) VALUES(:name,:cat,:status)",
                {"name": asset.name, "cat": asset.category, "status": asset.status},
            )

    def add_employees(self, emp: Employee) -> None:
        with sql.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO employees(name,department) VALUES(:name,:dept)",
                {"name": emp.name, "dept": emp.department},
            )

    def assign_asset(self, assign: Assignment) -> None:
        with sql.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT is_active FROM employees WHERE id=:emp_id",
                {"emp_id": assign.employee_id},
            )
            result = cursor.fetchone()

            if result is None:
                raise ValueError(f"Employee ID {assign.employee_id} does not exist.")

            if result[0] == 0:
                raise ValueError(
                    f"Cannot assign asset to Employee {assign.employee_id} because they are offboarded/inactive."
                )

            cursor.execute(
                "SELECT status FROM assets WHERE id=:asset_id",
                {"asset_id": assign.asset_id},
            )
            asset_result = cursor.fetchone()

            if asset_result is None:
                raise ValueError(f"Asset ID {assign.asset_id} does not exist.")

            current_status = asset_result[0]

            if current_status != "AVAILABLE":
                raise ValueError(
                    f"Asset {assign.asset_id} is currently '{current_status}'. Only AVAILABLE assets can be assigned"
                )

            cursor.execute(
                "INSERT INTO assignments(asset_id,employee_id,assigned_date) VALUES(:asset,:emp,:assig)",
                {
                    "asset": assign.asset_id,
                    "emp": assign.employee_id,
                    "assig": assign.assigned_date,
                },
            )

            cursor.execute(
                "UPDATE assets SET status='ASSIGNED' WHERE id=:asset_id",
                {"asset_id": assign.asset_id},
            )

    def return_asset(self, asset_id: int, return_date: str) -> None:
        with sql.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute(
                """UPDATE assignments
                SET return_date=:re_dt 
                WHERE asset_id=:asset AND return_date IS NULL""",
                {"re_dt": return_date, "asset": asset_id},
            )

            cursor.execute(
                "UPDATE assets SET status='AVAILABLE' WHERE id=:asset_id ",
                {"asset_id": asset_id},
            )

            if cursor.rowcount == 0:
                raise ValueError(f"Asset {asset_id} does not exist.")

    def update_asset_status(self, asset_id: int, new_status: str) -> None:
        valid_statuses = ["AVAILABLE", "ASSIGNED", "MAINTENANCE", "RETIRED"]

        if new_status not in valid_statuses:
            raise ValueError(
                f"Invalid Status: '{new_status}'. Must be one of {valid_statuses}"
            )

        with sql.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT status FROM assets WHERE id=:asset_id", {"asset_id": asset_id}
            )
            result = cursor.fetchone()

            if result is None:
                raise ValueError(f"Asset ID {asset_id} not found.")

            current_status = result[0]

            if current_status == "ASSIGNED" and new_status != "ASSIGNED":
                raise ValueError(
                    f"Cannot change status to {new_status}. Asset {asset_id} is currently ASSIGNED. "
                    "Please return the asset from the employee first."
                )

            cursor.execute(
                "UPDATE assets SET status=:stat WHERE id=:asset_id",
                {"stat": new_status, "asset_id": asset_id},
            )

    def offboard_employee(self, employee_id: int) -> None:
        with sql.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE employees SET is_active=0 WHERE id=:id", {"id": employee_id}
            )
            if cursor.rowcount == 0:
                raise ValueError(f"Employee ID {employee_id} not found.")

    def get_all_assets(self) -> list:
        with sql.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM assets")
            return cursor.fetchall()

    def get_all_employees(self) -> list:
        with sql.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM employees")
            return cursor.fetchall()

    def get_active_assignments(self) -> list[tuple[str, str, str]]:
        with sql.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                           SELECT e.name,ase.name,assign.assigned_date
                           FROM assignments AS assign
                           JOIN assets AS ase ON ase.id=assign.asset_id
                           JOIN employees AS e ON e.id=assign.employee_id
                           WHERE assign.return_date IS NULL
                           """)

            return cursor.fetchall()
