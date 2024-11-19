import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from tabulate import tabulate

def load_data_2(filename):
    my_list_2 = []
    with open(filename, 'r', encoding='utf-8') as f:
        # Read the file line by line
        for line in f:
            # Split each line using the semicolon delimiter
            row = line.strip().split(';')
            my_list_2.append(row)  
    return my_list_2

df = load_data_2("Booli_sold.csv")

def calculate_price_per_square(all_data):
    results = []
    # Skip the first row if it's a header
    for row in all_data[1:]:  # Start from the second row to skip header
        try:
            # Debugging: print the row to see the data you're working with
            print(row)  # This will print every row being processed
            
            # Assuming the correct columns based on your data structure
            list_price = float(row[0])  # Assuming listPrice is at index 0
            square_meters = float(row[2])  # Assuming livingArea is at index 2
            sold_price = float(row[9])  # Assuming soldPrice is at index 9

            if square_meters > 0:
                price_per_sqm = sold_price / square_meters
            else:
                price_per_sqm = None  # Invalid data, no calculation

            # Append the result to the list
            results.append({
                "List price": list_price,
                "Square meters": square_meters,
                "Sold price": sold_price,
                "Price per square meters": price_per_sqm
            })
        except (ValueError, IndexError) as e:
            # Handle cases where data is missing or invalid
            print(f"Skipping row due to error: {e}")  # Print error for debugging
            results.append({
                "List price": None,
                "Square meters": None,
                "Sold price": None,
                "Price per square meters": None
            })
    return results

# Now calculate the price per square meter for the loaded data
results = calculate_price_per_square(df)

# If you want to print the results:
from tabulate import tabulate

# Get the header
header = ['List Price', 'Square Meters', 'Sold Price', 'Price per Square Meters']

# Prepare the data rows
rows = [
    [entry['List price'], entry['Square meters'], entry['Sold price'], entry['Price per square meters']]
    for entry in results
]

# Print the table using tabulate
print(tabulate(rows, headers=header, tablefmt="grid"))

# Print the table using tabulate
#print(tabulate(rows, headers=header, tablefmt="grid"))