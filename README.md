# Welcome to the Plant Care Guide dataset!
This dataset provides a list of some common house plants, and how to take care of them.

## Data Collection
A list of house plants is scraped from the website https://www.realsimple.com/home-organizing/gardening/indoor/popular-house-plants, 
including:
- Plant common name
- Scientific Name
- Care list (Light, Soil, Water, Temperature, Humidity)

Then, that data is matched to the API, **Trefle API**, to get:
- Year of Discovery
- Family
- Genus

## Purpose of Data 
The purpose of this dataset is to match all this data to create a comprehensive guide for plant owners, who are 
interested in taking care of their plants as well as learning more about them and their origins. This particular website
was chosen because it showed common house plants, which are the plants that most people are usually interested in,
and provided care information about them. 

## Value of Dataset
This dataset will be valuable for users, as it simulates a "**one stop shop**" for house plant owners.
I myself have plants that I just don't really know how to take care of, so looking at this dataset 
will help me at least learn a little more about them. Users will not only be able to figure out how to take
care of their various plants, but they will also be able to learn more about the plant, including things such as their
family and scientific name. 

Such a dataset might not be publicly available yet due to the lack, in general, of datasets revolving 
around plants. From my research, most plant datasets involve the scientific name, or other facts,
but not really proper care information. 

## How to Run
1. Git clone this repo onto your local device.
```
git clone https://github.com/Sreya-Mandalika/plant-care-guide.git
cd random-boardgame
```
2. Go to the Trefle API website, and sign up to generate a free API key.
3. Install the required dependencies using the requirements.txt file.
   ```
   Pip install -r requirements.txt
   ```
4. Run the main.py file - it will generate the plant_data_and_care_tips.csv (the dataset). 

