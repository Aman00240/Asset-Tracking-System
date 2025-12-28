import pytest
from src.models import Asset, Employee, Assignment


# Asset Tests
def test_create_valid_asset() -> None:
    a = Asset(name=" asus ", category="laptop")
    assert a.name == "Asus"
    assert a.category == "Laptop"
    assert a.status == "AVAILABLE"


def test_asset_status_normalization() -> None:
    a = Asset(name="dell", category="laptop", status="maintenance")
    assert a.status == "MAINTENANCE"


def test_asset_name_cant_be_empty() -> None:
    with pytest.raises(ValueError, match="Asset name cant be empty"):
        Asset(name=" ", category="laptop")


def test_category_name_cant_be_empty() -> None:
    with pytest.raises(ValueError, match="Category cannot be empty"):
        Asset(name="dell", category=" ")


def test_asset_name_cant_be_numbers() -> None:
    with pytest.raises(ValueError, match="Asset name cannot be just numbers"):
        Asset(name="34234", category="laptop")


def test_asset_category_cant_be_numbers() -> None:
    with pytest.raises(ValueError, match="Category cannot be just numbers"):
        Asset(name="Dell", category="3434")


# Employee Tests


def test_create_valid_emp() -> None:
    e = Employee(name=" bob dob ", department=" it ")

    assert e.name == "Bob Dob"
    assert e.department == "IT"
    assert e.is_active == 1


def test_emp_name_cant_be_empty() -> None:
    with pytest.raises(ValueError, match="Employee name cant be empty"):
        Employee(name=" ", department="it")


def test_emp_department_cant_be_empty() -> None:
    with pytest.raises(ValueError, match="Department name cant be empty"):
        Employee(name="Bob ", department=" ")


def test_emp_name_cant_be_numbers() -> None:
    with pytest.raises(ValueError, match="Employee name cannot contain numbers"):
        Employee(name="34234", department="it")


def test_emp_department_cant_just_be_numbers() -> None:
    with pytest.raises(ValueError, match="Department cannot be just numbers"):
        Employee(name="Bob", department="34234")


def test_emp_invalid_active_status():
    with pytest.raises(ValueError, match="Invalid Active Status"):
        Employee(name="John", department="IT", is_active=42)


# Assignment Tests


def test_create_valid_assignment() -> None:
    assign = Assignment(asset_id=1, employee_id=1)

    assert assign.asset_id == 1
    assert assign.employee_id == 1
    assert len(assign.assigned_date) == 10


def test_assign_valid_date_format() -> None:
    with pytest.raises(ValueError, match="Dates must be in YYYY-MM-DD format"):
        Assignment(asset_id=1, employee_id=1, assigned_date="2025/01/01")


def test_assign_return_valid_date_format() -> None:
    with pytest.raises(ValueError, match="Dates must be in YYYY-MM-DD"):
        Assignment(
            asset_id=1,
            employee_id=1,
            assigned_date="2025-01-01",
            return_date="01-01-2025",
        )
