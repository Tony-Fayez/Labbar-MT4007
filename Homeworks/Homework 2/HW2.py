import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

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
    print(ekhagsvagen_data)
    return ekhagsvagen_data


def calculate_avg_ppsqm(data):
    total_ppsqm = 0
    count = 0

    for row in data:
        try:
            list_price = float(row[0])  
            square_meters = float(row[2])  
            sold_price = float(row[9])  

            if square_meters > 0:  # Avoid division by zero
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
print(avg_ppsqm_ekhagen)

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
plt.show()