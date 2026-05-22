from models import RentalUnit, save_units, load_units

print("Loading existing data...")
my_portfolio = load_units()
print(f"Loaded {len(my_portfolio)} units from storage.\n")

if len(my_portfolio) == 0:
    print("Creating sample data because storage was empty...")
    unit1 = RentalUnit("10A", "Matt Franqui", "John Doe", "2026-05-22", "6 month")
    unit2 = RentalUnit("14B", "Sarah Jenkins", "Jane Smith", "2026-05-22", "1 year")
    
    my_portfolio.append(unit1)
    my_portfolio.append(unit2)
    
    print(f"Created Unit {unit1.unit_number}. Auto Move-Out: {unit1.move_out_date.strftime('%Y-%m-%d')}")
    print(f"Created Unit {unit2.unit_number}. Auto Move-Out: {unit2.move_out_date.strftime('%Y-%m-%d')}")
    
    print("\nSaving data to disk...")
    save_units(my_portfolio)
    print("Data saved! Run this test script a second time to see if it reads the file.")
else:
    print("Displaying loaded units...")
    for unit in my_portfolio:
        print(f"Unit: {unit.unit_number} | PM: {unit.property_manager} | Tenant: {unit.tenant_name} | Move-Out: {unit.move_out_date.strftime('%Y-%m-%d')}")