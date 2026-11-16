"""
# ISM2411 Lab 12 — Read a Sales CSV, Write a Cleaned Report
# Author: Zuleykha Jafarzade
# Command to run: python3 csv_practice.py

REFLECTIONS:
1. Performing an ETL pipeline in Python offers immense reproducibility, scalability for large datasets, and automation compared to manual spreadsheet manipulation in Excel. While Excel excels at ad-hoc exploratory analysis and quick visual formatting, Python handles massive datasets and repeatable transformations flawlessly without human copy-paste errors.
2. A real business process that benefits from an append-mode log file is an automated e-commerce order processing or payment gateway transaction logger, where each incoming transaction must be securely recorded chronologically without overwriting previous historical logs.
"""

import csv
import os
from datetime import datetime

os.makedirs("data", exist_ok=True)
sales_data_path = "data/sales.csv"
if not os.path.exists(sales_data_path):
    with open(sales_data_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["product", "price", "quantity"])
        writer.writerow(["Widget A", "9.99", "50"])
        writer.writerow(["Widget B", "14.50", "30"])
        writer.writerow(["Gadget X", "29.99", "10"])
        writer.writerow(["Gadget Y", "49.99", "5"])
        writer.writerow(["SuperWidget", "5.99", "120"])
        writer.writerow(["Gizmo Pro", "99.99", "2"])
        writer.writerow(["Standard Gizmo", "24.50", "15"])
        writer.writerow(["Basic Tool", "12.00", "40"])
        writer.writerow(["Deluxe Tool", "85.00", "8"])
        writer.writerow(["Mini Widget", "3.50", "200"])
        writer.writerow(["Mega Gadget", "150.00", "3"])
        writer.writerow(["Eco Widget", "7.25", "60"])

print("=== EXERCISE 1 & 2 · Read and print raw rows ===")
with open(sales_data_path, mode="r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

print("\n=== EXERCISE 3 · Skip the header ===")
with open(sales_data_path, mode="r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    print(f"Header: {header}")
    print("Data Rows:")
    for row in reader:
        print(row)

print("\n=== EXERCISE 4 · Compute totals ===")
total_revenue = 0.0
with open(sales_data_path, mode="r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        product = row[0]
        price = float(row[1])
        quantity = int(row[2])
        line_total = price * quantity
        total_revenue += line_total
        print(f"{product}: {quantity} units × ${price:.2f} = ${line_total:.2f}")

print(f"\nOverall Total Revenue: ${total_revenue:.2f}")

print("\n=== EXERCISE 5 · Filter and write (cleaned.csv) ===")
cleaned_path = "data/cleaned.csv"
original_count = 0
written_count = 0

with open(sales_data_path, mode="r", encoding="utf-8") as infile, \
     open(cleaned_path, mode="w", newline="", encoding="utf-8") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    
    header = next(reader)
    writer.writerow(["Product", "Price", "Qty", "Total"])
    
    for row in reader:
        original_count += 1
        product = row[0]
        price = float(row[1])
        quantity = int(row[2])
        line_total = price * quantity
        
        if line_total > 100:
            writer.writerow([product, f"{price:.2f}", quantity, f"{line_total:.2f}"])
            written_count += 1

print(f"Original rows: {original_count} | Written to cleaned.csv (Total > $100): {written_count}")

print("\n=== EXERCISE 6 · csv.DictReader ===")
dict_total_revenue = 0.0
with open(sales_data_path, mode="r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        p = row["product"]
        pr = float(row["price"])
        qt = int(row["quantity"])
        dict_total_revenue += pr * qt

print(f"DictReader Computed Total Revenue: ${dict_total_revenue:.2f}")

print("\n=== EXERCISE 7 · Sales summary by product ===")
product_summary = {}
with open(sales_data_path, mode="r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        prod = row["product"]
        rev = float(row["price"]) * int(row["quantity"])
        product_summary[prod] = product_summary.get(prod, 0.0) + rev

print("Product Revenue Summary (Sorted):")
for prod in sorted(product_summary.keys()):
    print(f"{prod}: ${product_summary[prod]:.2f}")

print("\n=== EXERCISE 8 · Append mode log ===")
log_path = "data/run_log.txt"
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
log_entry = f"[{timestamp}] Run completed. Total Revenue: ${total_revenue:.2f}\n"

with open(log_path, mode="a", encoding="utf-8") as log_file:
    log_file.write(log_entry)

print(f"Appended log entry to {log_path}: {log_entry.strip()}")
