import streamlit as st
import pandas as pd
import ast
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import concurrent.futures
import time

# Initialize geolocator
geolocator = Nominatim(user_agent="city_mapper")

# Function to geocode a city name
def geocode_city(city_name):
    try:
        location = geolocator.geocode(city_name, timeout=10)
        if location:
            return location.latitude, location.longitude
    except GeocoderTimedOut:
        time.sleep(1)  # Retry after a short delay in case of timeout
    except Exception:
        pass  # Handle other exceptions silently
    return None, None

# Load data
file_path = 'extracted_data.csv'  # Update with the actual file path
def load_and_process_data(file_path):
    return  pd.read_csv(file_path)


# Safely parse the City column to extract individual cities
def parse_city_column(city_value):
    try:
        return ast.literal_eval(city_value) if isinstance(city_value, str) else []
    except (ValueError, SyntaxError):
        return []


# Parallelize geocoding
def parallel_geocode(cities):
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(geocode_city, city): city for city in cities}
        for future in concurrent.futures.as_completed(futures):
            city = futures[future]
            try:
                result = future.result()
                results.append((city, *result))
            except Exception as e:
                results.append((city, None, None))  # Default to None if there's an error
    return results

data = load_and_process_data()
data['City'] = data['City'].apply(parse_city_column)

# Flatten the city lists into a single list
city_list = [city for sublist in data['City'] for city in sublist]

# Count occurrences of each city
city_counts = pd.DataFrame(city_list, columns=['City']).value_counts().reset_index()
city_counts.columns = ['City', 'Count']
# Geocode cities in parallel
geocoded_data = parallel_geocode(city_counts['City'].tolist())

# Convert geocoded data to DataFrame
geocoded_df = pd.DataFrame(geocoded_data, columns=['City', 'Latitude', 'Longitude'])

# Merge geocoded data with counts
city_counts = city_counts.merge(geocoded_df, on='City')

# Filter out cities that could not be geocoded
city_counts = city_counts.dropna(subset=['Latitude', 'Longitude'])
city_counts = city_counts.rename(columns={'Latitude': 'latitude', 'Longitude': 'longitude'})
# Streamlit app
st.title("City Locations and Counts")

# Use Streamlit to map the cities with marker size based on the count
st.map(city_counts[['Latitude', 'Longitude']].assign(size=city_counts['Count']))
