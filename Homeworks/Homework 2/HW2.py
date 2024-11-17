import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from tabulate import tabulate

#Task 1
def load_data(filename):
    my_list = []
    with open(filename, 'r', encoding='utf-8') as h:
        for i, line in enumerate(h):
            if i == 0:
                continue
            row = line.strip().split(',')
            my_list.append(row)
    return my_list


data = load_data("Booli_sold.csv")


def calculate_price_per_square(all_data):
    results = []
    for row in all_data:
            try:
                list_price = float(row[0])
                square_meters = float(row[2])
                sold_price = float(row[9])

                if square_meters > 0:
                    price_per_sqm = sold_price / square_meters
                else:
                    price_per_sqm = None  # Invalid data, no calculation
                
                # Append the result to the list for the current dataset
                results.append({
                    "List price": list_price,
                    "Square meters": square_meters,
                    "Sold price": sold_price,
                    "Price per square meters": price_per_sqm
                })

            except (ValueError, IndexError):
                # Handle cases where data is missing or invalid
                results.append({
                    "List price": None,
                    "Square meters": None,
                    "Sold price": None,
                    "Price per square meters": None
                })
        # Add the results of the current list to the overall results
    return results

results = calculate_price_per_square(data)


def most_expensive_apartment(data, top_n = 5):
    results = calculate_price_per_square(data)

    valid_results = [entry for entry in results if entry ['Price per square meters'] is not None]

    sorted_results = sorted(valid_results, key=lambda x: x['Price per square meters'], reverse= True)

    return sorted_results[:top_n]

top_apartments = most_expensive_apartment(data, top_n=5)

# Print the top 5 expensive apartments
#for apartment in top_apartments:
    #print(apartment)

def header_for_apartments(top_apartments):
    header = ['List Price', 'Square Meters', 'Sold Price', 'Price per Square Meters']

    apartments_as_lists = [
        [apartment['List price'], apartment['Square meters'], apartment['Sold price'], apartment['Price per square meters']]
        for apartment in top_apartments
    ]
    return [header] + apartments_as_lists

top_apartments_with_header = header_for_apartments(top_apartments)
#for row in top_apartments_with_header:
    #print(row)

def extract_ekhagsvagen_data(all_data):
    ekhagsvagen_data = []
    
    # Iterate through the list of data
    for row in all_data:
        # Extract the address (assuming it's in column 16, index 16)
        if len(row) > 16:
            address = row[16].strip()  # Remove any surrounding whitespace

            # Check if the address contains 'Ekhagsvägen'
            if 'Ekhagsvägen' in address:
                ekhagsvagen_data.append(row)  # Add the row to the list
    return ekhagsvagen_data


def calculate_avg_ppsqm(data):
    total_ppsqm = 0
    count = 0

    for row in data:
        try:
            list_price = float(row[0])  
            square_meters = float(row[2])  
            sold_price = float(row[9])  

            if square_meters > 0:  
                price_per_sqm = sold_price / square_meters
                total_ppsqm += price_per_sqm
                count += 1
        except (ValueError, IndexError):
            continue  # Skip rows with invalid data
    
    if count > 0:
        avg_ppsqm = total_ppsqm / count
    else:
        avg_ppsqm = None  
    
    return avg_ppsqm

ekhagsvagen_data = extract_ekhagsvagen_data(all_data=data)
avg_ppsqm_ekhagen = calculate_avg_ppsqm(ekhagsvagen_data)
#print(avg_ppsqm_ekhagen)

def prepare_ppsqm_by_year(data):
    processed_data = []
    for row in data:
        try:
            year = int(row[5])  # Assuming Construction Year is column index 5
            ppsqm = float(row[9]) / float(row[2]) if float(row[2]) > 0 else None  # Sold price/sqm
            if ppsqm and year > 1800:  # Only consider valid years
                processed_data.append({'Year': year, 'PPSQM': ppsqm})
        except (ValueError, IndexError):
            continue
    return processed_data

processed_data = prepare_ppsqm_by_year(data)
df = pd.DataFrame(processed_data)

average_ppsqm_per_year = df.groupby('Year')['PPSQM'].mean().reset_index()

df['Year Range'] = pd.cut(
    df['Year'],
    bins=[1900, 1930, 1960, 1990, 2000, 2010, 2020],
    labels=['1900–1930', '1931–1960', '1961–1990', '1991–2000', '2001–2010', '2011–2020']
)

bins = [1900, 1930, 1960, 1990, 2000, 2010, 2020]
labels = ['1900–1930', '1931–1960', '1961–1990', '1991–2000', '2001–2010', '2011–2020']

# Add 'Year Range' to the DataFrame using pd.cut
df['Year Range'] = pd.cut(df['Year'], bins=bins, labels=labels, include_lowest=True)

# Calculate average PPSQM for each year range
average_ppsqm_per_range = df.groupby('Year Range')['PPSQM'].mean().reset_index()

# Ensure all year ranges appear in the result, even if no data
average_ppsqm_per_range['PPSQM'] = average_ppsqm_per_range['PPSQM'].fillna(0)

# Plot the bar chart
plt.figure(figsize=(12, 6))
plt.bar(average_ppsqm_per_range['Year Range'], average_ppsqm_per_range['PPSQM'], color='skyblue', edgecolor='black')
plt.title('Average Price per Square Meter by Construction Year Range', fontsize=16)
plt.xlabel('Construction Year Range', fontsize=12)
plt.ylabel('Average Price per Square Meter (PPSQM)', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
#plt.show()

#Task 2
def load_data_2(filename):
    my_list_2 = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            row = line.strip().split(';')
            my_list_2.append(row)  
    return my_list_2

data_tk2 = load_data_2("2018_R_per_kommun.csv")

def extract_giltiga_for_stockholm(all_data2):
    """Extracts 'RÖSTER GILTIGA' values for 'Stockholms län'."""
    if not all_data2:
        return []

    # Extract the header row
    header = all_data2[0]
    
    # Get the indices of 'LÄNSNAMN' and 'RÖSTER GILTIGA'
    try:
        länsnamn_index = header.index('LÄNSNAMN')
        giltiga_index = header.index('RÖSTER GILTIGA')
    except ValueError as e:
        raise ValueError("One or more columns not found in the header.") from e

    # Filter rows for 'Stockholms län' and extract 'RÖSTER GILTIGA'
    stockholm_giltiga = [
        row[giltiga_index]
        for row in all_data2[1:]  # Skip the header row
        if len(row) > giltiga_index and row[länsnamn_index] == 'Stockholms län'
    ]

    return stockholm_giltiga

def count_roster(giltiga_values):
    try:
        return sum(int(value) for value in giltiga_values)
    except ValueError as l:
        raise ValueError("Non-numeric value encountered in 'RÖSTER GILTIGA'.") from l

giltiga_stockholm = extract_giltiga_for_stockholm(all_data2 = data_tk2)
print("Giltiga röster för 'Stockholms län':")
#for value in giltiga_stockholm:
    #print(value)

total_giltiga = count_roster(giltiga_stockholm)
print("Antalet giltiga röster för 'Stockholms län':", total_giltiga)

def majority_votes(all_data3):
    if not all_data3:
        return None, None
    header = all_data3[0]
    try:
        kommun_index = header.index('KOMMUNNAMN')
        x_index = header.index('S')
    except ValueError as t:
        raise ValueError("Saknas data") from t
    max_percentage = -1
    max_municipality = None

    for row in all_data3[1:]:
        if len(row) > x_index:
            try:
                municipality = row[kommun_index]
                percentage = float(row[x_index].replace(',', '.'))
                if percentage > max_percentage:
                    max_percentage = percentage
                    max_municipality = municipality
            except ValueError:
                continue
    return max_municipality, max_percentage

support_municipality, support_percentage = majority_votes(all_data3 = data_tk2)

if support_municipality:
    print(f"The municipality with the highest support for S is '{support_municipality}' with {support_percentage:.2f}%.")
else:
    print("No valid data found for Social Democratic Party support.")

# Integration of Top Participation Ranking
def rank_highest_participation(all_data, top_n=3):
    if not all_data:
        return []

    # Extract the header row
    header = all_data[0]
    
    # Get the indices of 'KOMMUNNAMN' and 'VALDELTAGANDE'
    try:
        kommun_index = header.index('KOMMUNNAMN')
        valdeltagande_index = header.index('VALDELTAGANDE')
    except ValueError as e:
        raise ValueError("One or more required columns not found in the header.") from e

    # Extract participation values and municipalities
    participation_data = []
    for row in all_data[1:]:  # Skip the header
        if len(row) > valdeltagande_index:
            try:
                municipality = row[kommun_index]
                participation = float(row[valdeltagande_index].replace(',', '.'))
                participation_data.append((municipality, participation))
            except ValueError:
                continue  # Skip rows with invalid participation values

    # Sort by participation in descending order
    sorted_participation = sorted(participation_data, key=lambda x: x[1], reverse=True)

    # Return the top N municipalities
    return sorted_participation[:top_n]

# Get the top 3 municipalities with highest participation
top_municipalities = rank_highest_participation(data_tk2, top_n=3)

# Display as a table
from tabulate import tabulate
print("\nTop 3 Municipalities by Participation:")
print(tabulate(top_municipalities, headers=["Municipality", "Participation (%)"], tablefmt="grid"))

#Task 3



