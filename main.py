import requests
import pandas as pd
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import re
import time

#load enviorment, fetch API and URLs, and define headers
load_dotenv()
api_key = os.getenv('TREFLE_KEY')
base_url = "https://trefle.io/api/v1/plants"

headers = {
    'Authorization': f'Bearer {api_key}' 
}

#scrape plant names (common and scientific) and care facts from the website
url = "https://www.realsimple.com/home-organizing/gardening/indoor/popular-house-plants"
response = requests.get(url)
plant_list = []

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    plant_spans = soup.find_all('span', class_='mntl-sc-block-heading__text')

    #plant names
    for plant in plant_spans:
        text = plant.get_text(strip=True)
        match = re.search(r'(.+?)\s\((.+?)\)', text)
        if match:
            common_name = match.group(1).strip().title()
            scientific_name = match.group(2).strip()
            plant_list.append((common_name, scientific_name))

    all_plant_data = []

    #care tips
    care_tips_section = soup.find_all('ul', class_='comp mntl-sc-block mntl-sc-block-html')
    for idx, (common_name, scientific_name) in enumerate(plant_list):
        care_tips_combined = 'Care tips not found'
        if idx < len(care_tips_section):
            care_tips = [li.text.strip() for li in care_tips_section[idx].find_all('li')]
            care_tips_combined = '; '.join(care_tips) if care_tips else 'Care tips not found'

        all_plant_data.append({
            'Common Name': common_name,
            'Scientific Name': scientific_name,
            'Care Tips': care_tips_combined
        })

#go through each plant in scraped list, by scientific name first then common name
for plant_info in all_plant_data:
    common_name = plant_info['Common Name']
    scientific_name = plant_info['Scientific Name']
    found = False

    params = {'filter[scientific_name]': scientific_name}
    response = requests.get(base_url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()['data']
        if data:
            for plant in data:
                plant_info.update({
                    'Family': plant.get('family', 'Unknown'),
                    'Genus': plant.get('genus', 'Unknown'),
                    'Year Discovered': int(plant['year']) if 'year' in plant and plant['year'] else 'Unknown'
                })
                found = True

    if not found:
        params = {'filter[common_name]': common_name}
        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()['data']
            if data:
                for plant in data:
                    plant_info.update({
                        'Family': plant.get('family', 'Unknown'),
                        'Genus': plant.get('genus', 'Unknown'),
                        'Year Discovered': plant.get('year', 'Unknown')
                    })
                    found = True

    #short delay to let API relax
    time.sleep(1)

#splitting care info into different columns 
def extract_care_info(care_tips):
    care_info = {
        'Light': 'Unknown',
        'Soil': 'Unknown',
        'Water': 'Unknown',
        'Temperature': 'Unknown',
        'Humidity': 'Unknown'
    }
    
    for tip in care_tips.split('; '):
        tip = tip.strip().lower()
        if 'light' in tip:
            care_info['Light'] = tip.split(':', 1)[-1].strip().capitalize()
        elif 'soil' in tip:
            care_info['Soil'] = tip.split(':', 1)[-1].strip().capitalize()
        elif 'water' in tip:
            care_info['Water'] = tip.split(':', 1)[-1].strip().capitalize()
        elif 'temperature' in tip:
            care_info['Temperature'] = tip.split(':', 1)[-1].strip().capitalize()
        elif 'humidity' in tip:
            care_info['Humidity'] = tip.split(':', 1)[-1].strip().capitalize()
    return care_info

#turning info into pandas dataframe
df = pd.DataFrame(all_plant_data)

care_columns = df['Care Tips'].apply(extract_care_info).apply(pd.Series)
df = pd.concat([df, care_columns], axis=1)

#dropping original care tips and rows w/o family or genus
df.drop(columns=['Care Tips'], inplace=True)
df = df.dropna(subset=['Family', 'Genus'])

df.to_csv('plant_data_and_care_tips.csv', index=False)
print(f"Filtered plant data with care info saved to plant_data_and_care_tips.csv with {len(df)} entries.")
