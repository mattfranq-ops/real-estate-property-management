import json
import os
from datetime import datetime, timedelta

class RentalUnit:
    def __init__(self, unit_number, property_manager, tenant_name, move_in_str, timeframe_choice, custom_days=0, move_out_str=None):
        # Unit constructor
        self.unit_number = unit_number
        self.property_manager = property_manager
        self.tenant_name = tenant_name
        self.move_in_date = datetime.strptime(move_in_str, "%Y-%m-%d")

        # Load pre-existing unit from file
        if move_out_str:
            self.move_out_date = datetime.strptime(move_out_str, "%Y-%m-%d")
        else:
            self.move_out_date = self.calculate_move_out(timeframe_choice, custom_days)
    
    # Calculating when the tenants move out will be
    def calculate_move_out(self, choice, custom_days):
        if choice == "6 month":
            return self.move_in_date + timedelta(days=182)
        elif choice == "1 year":
            return self.move_in_date + timedelta(days=365)
        elif choice == "custom":
            return self.move_in_date + timedelta(days = custom_days)
        else:
            return self.move_in_date
        
    def to_dict(self):
        # Object data needs to be converted into a standard dictionary so the JSON can save it.
        return{
            "unit_number": self.unit_number,
            "property_manager": self.property_manager,
            "tenant_name": self.tenant_name,
            "move_in_date": self.move_in_date.strftime("%Y-%m-%d"),
            "move_out_date": self.move_out_date.strftime("%Y-%m-%d")
        }
    
# Handling of File Storage Functions.

DB_FILE = "database.json"

def save_units(units_list):
    # Take the list of RentalUnit's and convert to dicts before saving to file.
    with open(DB_FILE, "w") as f:
        # Convert every object into a dict.
        json_compatible_list = [unit.to_dict() for unit in units_list]
        json.dump(json_compatible_list, f, indent=4)

def load_units():
    # Load data from the file, and reconstruct into objects for RentalUnit.
    if not os.path.exists(DB_FILE):
        return [] # Return empty list of no save file exists
    
    with open(DB_FILE, "r") as f:
        try:
            raw_data = json.load(f)
            units = []
            for item in raw_data:
                # With saved strings, rebuild RentalUnit objects list.
                unit = RentalUnit(
                    unit_number=item["unit_number"],
                    property_manager=item["property_manager"],
                    tenant_name=item["tenant_name"],
                    move_in_str=item["move_in_date"],
                    timeframe_choice="load",
                    move_out_str=item["move_out_date"]
                )
                units.append(unit)
            return units
        except json.JSONDecodeError:
            return[] # Catch for if file is corrupted or blank, telling to start a fresh file.