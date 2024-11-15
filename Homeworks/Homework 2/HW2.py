import csv

def load_data(filename):
    my_list = []
    with open(filename, 'r') as h:
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
   # print(row)




