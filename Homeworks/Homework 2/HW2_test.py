def extract_ekhagsvagen_data(data):
    ekhagsvagen_data = []
    for row in data:
        # Assuming address is in column 16 (index 16)
        address = row[16] if len(row) > 16 and row[16] != 'NA' else None
        if address and 'Ekhagsvägen' in address:
            ekhagsvagen_data.append(row)  # Append the entire row (data for the apartment)
    return ekhagsvagen_data

# Example data (with addresses in index 16)
data = [
    ['3995000', '4467', '73', '3', '2018-10-15', '1935', 'Lägenhet', '3263989', '2018-11-08', '3820000', 'bid', 'https://www.booli.se/annons/3263989', 'NA', 'NA', 'NA', 'Åminnevägen 19', '59.37103271', '18.0540565', 'NA', 'Stockholm', 'Stockholms län', '260', 'MOHV', '1901865', 'Broker', 'http://www.mohv.se/'],
    ['2300000', '2455', '50', '2', '2012-09-16', '1935', 'Lägenhet', '1272477', '2012-10-09', '2180000', 'bid', 'https://www.booli.se/annons/1272477', 'NA', 'NA', 'NA', 'Ekhagsvägen 12', '59.372272100000004', '18.0556589', 'TRUE', 'Stockholm', 'Stockholms län', '101', 'Notar', '1566', 'Broker', 'http://www.notar.se/'],
    ['3550000', '2807', '80', '3', '2012-11-23 11:52:27', '1935', 'Lägenhet', '1317745', '2012-12-07', '3730000', 'bid', 'https://www.booli.se/annons/1317745', '2', 'NA', 'NA', 'NA', 'Ekhagsvägen 2', '59.3709948', '18.0548886', 'TRUE', 'Stockholm', 'Stockholms län', '243', 'Notar', '1566', 'Broker', 'http://www.notar.se/'],
    ['3550000', '2807', '80', '3', '2012-11-23 11:52:27', '1935', 'Lägenhet', '1317745', '2012-12-07', '3730000', 'bid', 'https://www.booli.se/annons/1317745', '2', 'NA', 'NA', 'NA', 'Kungsholmsvägen 12', '59.3709948', '18.0548886', 'TRUE', 'Stockholm', 'Stockholms län', '243', 'Notar', '1566', 'Broker', 'http://www.notar.se/']
]

# Extract all data for addresses containing 'Ekhagsvägen'
ekhagsvagen_data = extract_ekhagsvagen_data(data)

# Print the extracted data (all rows for Ekhagsvägen)
for row in ekhagsvagen_data:
    print(row)
