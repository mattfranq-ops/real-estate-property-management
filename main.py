import tkinter as tk
from tkinter import ttk
from models import load_units, save_units, RentalUnit

# --- Root window ---

root = tk.Tk()
root.title("Real Estate Property Management Platform")
root.geometry("900x500")

# --- Containers ---

# Left frame.
form_frame = ttk.Frame(root, padding=20)
form_frame.grid(row=0, column=0, sticky="nsew")

# Right frame.
display_frame = ttk.Frame(root, padding = 20)
display_frame.grid(row=0, column=1, sticky="nsew")

# Window gid scaling.

root.columnconfigure(0, weight = 1)
root.columnconfigure(1, weight = 3)
root.rowconfigure(0, weight=1)

# Form inputs on the left side.
unit_label = ttk.Label(form_frame, text="Unit Number:")
unit_label.grid(row=0, column=0, pady=(0, 5), sticky="w")
unit_entry = ttk.Entry(form_frame)
unit_entry.grid(row=1, column=0, columnspan=2, pady=(0, 15), sticky="ew")

# Property Manager Input.
pm_label = ttk.Label(form_frame, text="Property Manager Assigned:")
pm_label.grid(row=2, column=0, pady=(0,5), sticky="w")
pm_entry = ttk.Entry(form_frame)
pm_entry.grid(row=3, column=0, columnspan=2, pady=(0, 15), sticky="ew")

# Tenant Name.
tenant_label = ttk.Label(form_frame, text="Tenant Name:")
tenant_label.grid(row=4, column=0, pady=(0, 5), sticky="w")
tenant_entry = ttk.Entry(form_frame)
tenant_entry.grid(row=5, column=0, columnspan=2, pady=(0,15), sticky="ew")

# Move-In Date.
move_in_label = ttk.Label(form_frame, text="Move-In  Date (YYYY-MM-DD):")
move_in_label.grid(row=6, column=0, pady=(0,5), sticky="w")
move_in_entry = ttk.Entry(form_frame)
move_in_entry.grid(row=7, column=0, columnspan=2, pady=(0,15), sticky="ew")

# Data read (Left Side)

# Auto-pop Move-In box.
from datetime import datetime
today_str = datetime.today().strftime("%Y-%m-%d")
move_in_entry.insert(0, today_str)

# Lease Timeframe Selection.
timeframe_label = ttk.Label(form_frame, text="Lease Duration:")
timeframe_label.grid(row=8, column=0, pady=(0, 5), sticky="w")
timeframe_dropdown = ttk.Combobox(form_frame, values=["6 month", "1 year", "custom"], state="readonly")
timeframe_dropdown.grid(row=9, column=0, columnspan=2, pady=(0, 15), sticky="ew")
timeframe_dropdown.set("1 year")

# Custom timeframe.
custom_days_label = ttk.Label(form_frame, text="Custom Duration (Days):")
custom_days_label.grid(row=10, column=0, pady=(0,5), sticky="w")
custom_days_entry = ttk.Entry(form_frame)
custom_days_entry.grid(row=11, column=0, columnspan=2, pady=(0, 20), sticky="ew")
custom_days_entry.insert(0, "0")

# --- Spreadsheet (Right Side) ---

# Columns.
columns = ("unit", "manager", "tenant", "move_in", "move_out")

# Treeview. 
tree = ttk.Treeview(display_frame, columns=columns, show="headings")

# Define header names for users
tree.heading("unit", text="Unit #")
tree.heading("manager", text="Property Manager")
tree.heading("tenant", text="Tenant Name")
tree.heading("move_in", text="Move-In Date")
tree.heading("move_out", text="Move-Out Date")

# Structural width rules for columns
tree.column("unit", width=70, anchor="center")
tree.column("manager", width=150, anchor="w")
tree.column("tenant", width=150, anchor="w")
tree.column("move_in", width=110, anchor="center")
tree.column("move_out", width=110, anchor="center")

# Treeview placer
tree.grid(row=0, column=0, sticky="nsew")

# Table stretchout
display_frame.columnconfigure(0, weight=1)
display_frame.rowconfigure(0, weight=1)

# --- Data Pipeline & Save ---

# Database load
all_units = load_units()

def update_table_display():
    # Visual treeview, renders all saved units.
    # Clear current visuals.
    for item in tree.get_children():
        tree.delete(item)

    # Re-pup rows.
    for unit in all_units:
        tree.insert(
            parent="",
            index=tk.END,
            values=(
                unit.unit_number,
                unit.property_manager,
                unit.tenant_name,
                unit.move_in_date.strftime("%Y-%m-%d"),
                unit.move_out_date.strftime("%Y-%m-%d")
            )
        )

def add_unit():
    # String entry from GUI input.
    unit_num = unit_entry.get()
    pm_assigned = pm_entry.get()
    tenant = tenant_entry.get()
    move_in = move_in_entry.get()
    duration = timeframe_dropdown.get()

    # Custom day conversion string -> integer.
    try:
        custom_days = int(custom_days_entry.get())
    except ValueError:
        custom_days = 0

    # Push new data to storage.
    new_unit = RentalUnit(
        unit_number=unit_num,
        property_manager=pm_assigned,
        tenant_name=tenant,
        move_in_str=move_in,
        timeframe_choice=duration,
        custom_days=custom_days
    )

    all_units.append(new_unit)
    save_units(all_units)

    update_table_display()

    # Confirmation splash screen.
    print(f"Succesfully added unit {unit_num}!\nAuto calculated move out: {new_unit.move_out_date.strftime('%Y-%m-%d')}")

    # Clean out text fields.
    unit_entry.delete(0, tk.END)
    tenant_entry.delete(0, tk.END)

# -- Initial Load & Startup ---
update_table_display()

# Action button.
submit_btn = ttk.Button(form_frame, text="Add Unit Portfolio", command=add_unit)
submit_btn.grid(row=12, column=0, columnspan=2, sticky="ew")

# Event loop start
root.mainloop()