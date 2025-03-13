import os
import csv
import codecs
import json
import scrapy
from scrapy.selector import Selector


with open('links.csv','rt') as fin:
    cin = csv.reader(fin)
    links = [row for row in cin]


def find_key_reference(data, target_key, path="json_data"):
    # If the current data is a dictionary, traverse its keys
    if isinstance(data, dict):
        for key, value in data.items():
            # Update the path in dictionary reference format
            new_path = f"{path}['{key}']"
            if key == target_key:
                # If we found the target key, return the path
                return new_path
            # Recursively search for the target key in the value
            found_path = find_key_reference(value, target_key, new_path)
            if found_path:
                return found_path
    # If the current data is a list, traverse its elements
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            # Update the path with the list index
            new_path = f"{path}[{idx}]"
            found_path = find_key_reference(item, target_key, new_path)
            if found_path:
                return found_path
    return None

files=[file for file in os.listdir('data') if file.endswith('.html')]

csvdata=[['Serial No.','Title','Purpose','Furnishing','Type',
          'Price(Currency)','Price','Price(Frequency)',
          'Bedrooms','Bathrooms','Area(Sqft)','Location',
          'Area','city','country', 'Amenities','Description',
          'DED', 'Reference ID', 'BLN','Agent Name',
          'Agent Email','Agent Phone Number', 
          'Agent Whatsapp No.','Agency Name','Agency Email',
          'Property Profile Link(Dubizzle)', 'Image Links']]

for num in range(len(files)):
    with codecs.open('data/'+files[num], 'r', 'utf-8') as fin:
        content=fin.read()
    if len(content)<200:
        continue
    response = Selector(text=content)
    try:
        #create json
        json_data=json.loads(response.css('script[type="application/json"]::text').get())
        output=[num]
        #output.append(response.css('h2[data-testid="listing-title"]::text').get())
        output.append(response.css('[data-testid="listing-title"]::text').get())
        output.append(response.css('div[data-testid="Purpose"]::text').get())
        output.append(response.css('div[data-testid="Furnishing"]::text').get())
        output.append(response.css('div[data-testid="Type"]::text').get())
        # price of the apartment
        output.append(response.css('p[class="MuiTypography-root MuiTypography-body1 mui-style-1gkv5mr"]::text').get())
        output.append(response.css('p[class="MuiTypography-root MuiTypography-body1 mui-style-1qcnehy"]::text').get())
        output.append(response.css('p[class="MuiTypography-root MuiTypography-body1 mui-style-d0oi9p"]::text').get())

        # number of bedrooms
        output.append(response.css('p[data-testid="bed_space"]::text').get())
        # number of bathrooms
        output.append(response.css('p[data-testid="bath"]::text').get())
        # area of the property
        output.append(response.css('p[data-testid="sqft"]::text').get())
        
        # location of the property
        location = response.css('p[data-testid="location-information"]::text').get()
        output.append(location if location else "N/A")
        locparts = [part.strip() for part in location.split(',')] if location else []
        locparts = locparts[::-1]

        location_list = json_data.get('location_list', [])

        if location_list and isinstance(location_list, list):
            # Ensure we have at least 3 elements for Area, City, Country
            locparts = [loc.strip() for loc in location_list if isinstance(loc, str)]
        else:
            locparts = [part.strip() for part in location.split(',')] if location else []

        # Assign area, city, and country correctly
        area = locparts[0] if len(locparts) > 0 else "N/A"
        city = locparts[1] if len(locparts) > 1 else "N/A"
        country = locparts[2] if len(locparts) > 2 else "N/A"

        output.append(area)
        output.append(city)
        output.append(country)

        #amenities
        output.append('|'.join(response.css('div[class="MuiGrid-root MuiGrid-item MuiGrid-grid-xs-4 MuiGrid-grid-md-2 mui-style-1vjae4a"] *::text').getall()))
        
        #description
        descriptionpath=find_key_reference(json_data,'description')
        # Initialize payload to avoid undefined variable issues
        
        payload = {}
        descriptionpath = find_key_reference(json_data, 'description')
        if descriptionpath:
            try:
                exec('payload=' + descriptionpath[:descriptionpath.rindex('[')])
            except Exception as e:
                print(f"Error extracting payload: {e}")

        try:
            output.append(payload['description']['en'])
        except:
            output.append(None)
        #DED
        output.append(response.css('div[data-testid="DED"]::text').get())
        #Reference ID
        output.append(response.css('div[data-testid="Reference ID"]::text').get())
        #BLN
        output.append(response.css('div[data-testid="BLN (ADREC)"]::text').get())
        #agent name
        output.append(response.css('p[data-testid="agent-name"]::text').get())
        #agent email
        try:
            output.append(payload['email'])
        except:
            try:
                output.append(payload['agent_profile']['email'])
            except:
                output.append(None)
        #agent phone number
        try:
            output.append(payload['phone_number'])
        except:
            try:
                output.append(payload['agent_profile']['phone_number'])
            except:
                output.append(None)
        #agent whatsapp
        try:
            output.append(payload['agent_profile']['whatsapp_number'])
        except:
            output.append(None)
        #agency
        try:
            output.append(payload['agency']['name'])
        except:
            output.append(response.css('p[class="MuiTypography-root MuiTypography-body1 mui-style-81j6cc"]::text').get())
        #agency email
        try:
            output.append(payload['agency']['email'])
        except:
            output.append(None)
        # link to the profile of the apartment
        output.append(response.css('link[hrefLang="en"]::attr(href)').getall()[0])
        
        #image links
        imglinks=[cell['main'] for cell in payload['photos']]
        output.append('    '.join(imglinks))
        
        #append to csv output
        csvdata.append(output)

    except Exception as e:
        print(f"Error processing {files}: {e}")


# Save results to CSV
with open('details.csv', 'wt', newline='', encoding='utf-8') as fout:
    writer = csv.writer(fout)
    writer.writerows(csvdata)

# Print final output for debugging
print("Final CSV Data:")
for row in csvdata:
    print(row)