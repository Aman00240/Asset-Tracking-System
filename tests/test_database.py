import pytest
import os
import gc
from src.database import Database_manager, setup_database
from src.models import Asset, Employee, Assignment

TEST_DB = "test_inventory.db"


@pytest.fixture
def db():
    if os.path.exists(TEST_DB):
        try:
            os.remove(TEST_DB)
        except PermissionError:
            pass

    setup_database(TEST_DB)
    manager = Database_manager(TEST_DB)

    yield manager

    del manager
    gc.collect()

    if os.path.exists(TEST_DB):
        try:
            os.remove(TEST_DB)
        except PermissionError:
            print("Warning: Could not delete test DB (Windows lock). Skipping.")


def test_add_and_retrive_asset(db):
    laptop = Asset(name="dell", category="laptop")
    db.add_assets(laptop)

    assets = db.get_all_assets()

    assert len(assets) == 1
    assert assets[0][1] == "Dell"
    assert assets[0][3] == "AVAILABLE"


def test_add_employee(db):
    emp = Employee(name="pen tonic", department="it")
    db.add_employees(emp)

    employees = db.get_all_employees()

    assert len(employees) == 1
    row = employees[0]

    assert row[1] == "Pen Tonic"
    assert row[2] == "IT"
    assert row[3] == 1


def test_assign_asset(db):
    db.add_assets(Asset(name="Projector", category="Office"))
    db.add_employees(Employee(name="Bob", department="IT"))

    assign = Assignment(asset_id=1, employee_id=1, assigned_date="2025-01-01")
    db.assign_asset(assign)

    active_assignments = db.get_active_assignments()
    assert len(active_assignments) == 1

    row = active_assignments[0]

    assert row[0] == "Bob"
    assert row[1] == "Projector"


def test_assign_to_ghost_employee_fails(db):
    db.add_assets(Asset(name="Ghost Laptop", category="Tech"))

    assign = Assignment(asset_id=1, employee_id=999)

    with pytest.raises(ValueError):
        db.assign_asset(assign)


def test_assign_already_assigned_asset_fails(db):
    db.add_assets(Asset(name="Shared Laptop", category="Tech"))
    db.add_employees(Employee(name="Alice", department="it"))
    db.add_employees(Employee(name="Bob", department="it"))

    assign1 = Assignment(asset_id=1, employee_id=1)
    db.assign_asset(assign1)

    assign2 = Assignment(asset_id=1, employee_id=2)

    with pytest.raises(ValueError, match="Only AVAILABLE assets can be assigned"):
        db.assign_asset(assign2)
