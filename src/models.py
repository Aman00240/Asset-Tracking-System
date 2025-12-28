from dataclasses import dataclass, field
from datetime import datetime, date


def get_today():
    return date.today().strftime("%Y-%m-%d")


@dataclass
class Asset:
    name: str
    category: str
    status: str = "AVAILABLE"
    id: int | None = None

    def __post_init__(self):
        self.name = self.name.strip().title()
        self.category = self.category.strip().title()
        self.status = self.status.strip().upper()

        if not self.name:
            raise ValueError("Asset name cant be empty")

        if not self.category:
            raise ValueError("Category cannot be empty")

        if self.id is not None and not isinstance(self.id, int):
            raise ValueError(f"ID must be a number, got{type(self.id)}")

        if self.name.isdigit():
            raise ValueError(
                "Asset name cannot be just numbers (e.g. '23'). Try 'Laptop 23' instead."
            )

        if self.category.isdigit():
            raise ValueError("Category cannot be just numbers.")


@dataclass
class Employee:
    name: str
    department: str
    is_active: int = 1
    id: int | None = None

    def __post_init__(self):
        self.name = self.name.strip().title()
        self.department = self.department.strip().upper()

        if not self.name:
            raise ValueError("Employee name cant be empty")

        if not self.department:
            raise ValueError("Department name cant be empty")

        if self.id is not None and not isinstance(self.id, int):
            raise ValueError(f"ID must be a number, got{type(self.id)}")

        if any(char.isdigit() for char in self.name):
            raise ValueError(
                f"Employee name cannot contain numbers. You typed: '{self.name}'"
            )

        if self.department.isdigit():
            raise ValueError(
                f"Department cannot be just numbers (You typed: '{self.department}')"
            )

        if self.is_active not in (1, 0):
            raise ValueError(
                f"Invalid Active Status: {self.is_active}. Must be 1 (Active) or 0 (Inactive)"
            )


@dataclass
class Assignment:
    asset_id: int
    employee_id: int
    assigned_date: str = field(default_factory=get_today)
    return_date: str | None = None
    id: int | None = None

    def __post_init__(self):
        if self.id is not None and not isinstance(self.id, int):
            raise ValueError(f"ID must be a number, got{type(self.id)}")

        if not isinstance(self.asset_id, int):
            raise ValueError(f"Asset ID must be a number, got{type(self.asset_id)}")

        if not isinstance(self.employee_id, int):
            raise ValueError(
                f"Employee ID must be a number, got{type(self.employee_id)}"
            )

        try:
            datetime.strptime(self.assigned_date, "%Y-%m-%d")
            if self.return_date:
                datetime.strptime(self.return_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Dates must be in YYYY-MM-DD format (e.g., 2025-01-30)")


if __name__ == "__main__":
    try:
        laptop = Asset(name="dell 3", category="laptop", status="available")

        print(f"Created: {laptop.name} | Status: {laptop.status}")

        bad_asset = Asset(name="Phone", category="Mobile", status="Stolen")

        bad_date = Assignment(asset_id=1, employee_id=1, assigned_date="2025/01/01")

        ghost = Employee(name=" ", department="IT")

    except ValueError as e:
        print(f"BLOCKED:{e} ")

    try:
        good_date = Assignment(asset_id=1, employee_id=1, assigned_date="2025-01-01")
        print(f"date:{good_date.assigned_date}")
        bad_date = Assignment(asset_id=1, employee_id=1, assigned_date="01-01-2025")
    except ValueError as e:
        print(f"BLOCKED:{e} ")

    try:
        emp = Employee(name="Aman", department="IT")
        print(f"name:{emp.name}, dept:{emp.department}")
        ghost = Employee(name=" ", department="IT")
    except ValueError as e:
        print(f"BLOCKED:{e} ")
