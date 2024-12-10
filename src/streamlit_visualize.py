import streamlit as st
import pandas as pd
import plotly.express as px
import concurrent.futures
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import ast
import os
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
@st.cache_data
def load_data(file_path):
    """Load the CSV file and return a DataFrame."""
    return pd.read_csv(file_path)

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

# Category Popularity Page
def category_popularity_page():
    """Display the category popularity page."""
    # Load the data
    script_dir = os.path.dirname(__file__)  # Ensure correct directory
    file_path = os.path.join(script_dir, "../results/final_data.csv")
    df = load_data(file_path)

    # Bar Chart: Subject Areas Popularity (without date filter)
    st.markdown("### Subject Areas Popularity")
    category_counts = df['Subject Area'].value_counts().reset_index()
    category_counts.columns = ['Subject Areas', 'Count']
    fig_bar = px.bar(
        category_counts,
        x="Count",
        y="Subject Areas",
        orientation='h',  # Horizontal bar chart
        text="Count",
        title="Popular Subject Areas",
        labels={"Count": "Total Count", "Subject Areas": "Subject Areas"},
        template="plotly_white",
    )
    fig_bar.update_traces(texttemplate='%{text}', textposition='outside')
    fig_bar.update_layout(xaxis_title="Count", yaxis_title="Subject Areas", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_bar, use_container_width=True)

    # Load data
    file_path = "results/final_data.csv"
    data = load_data(file_path)

# Split the Subject Code values by commas and remove leading/trailing spaces
    data['Subject Area'] = data['Subject Area'].apply(lambda x: [code.strip() for code in x.split(',')])

# Sidebar to select the subject code
    selected_subject_code = st.sidebar.selectbox('Select Subject Area', sorted(set([code for sublist in data['Subject Area'] for code in sublist])))

# Filter the data where the selected subject code is in the 'Subject Code' list
    filtered_data = data[data['Subject Area'].apply(lambda x: selected_subject_code in x)]

# Remove duplicates in the 'Subject Code' column by converting the list into a set and back to a list
    filtered_data['Subject Area'] = filtered_data['Subject Area'].apply(lambda x: list(set(x)))

# Parse city names
    filtered_data['City'] = filtered_data['City'].apply(parse_city_column)

# Flatten the city lists into a single list
    city_list = [city for sublist in filtered_data['City'] for city in sublist]

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

# Create two columns: one for the map and one for the DataFrame
    col1, col2 = st.columns([4, 2])  # Adjust column sizes as necessary

# Map in col1
    with col1:
    # Set your Mapbox Access Token here (you can get it from your Mapbox account)
        mapbox_access_token = "pk.eyJ1IjoiZW1teXl5eXkiLCJhIjoiY200aDkweWZnMDFvaTJvb2k0OTExdm9teiJ9.ifiTHPt-stolY-F5zW-hWA"  # Replace with your actual Mapbox token

    # Create a Plotly map using city_counts (with counts for marker size)
        fig = px.scatter_mapbox(city_counts,
                            lat='latitude',
                            lon='longitude',
                            size='Count',  # Marker size based on the count
                            hover_name='City',
                            hover_data=['Count'],
                            mapbox_style="open-street-map",  # Use this if you don't have a Mapbox token
                            title=f"Map of {selected_subject_code}")

    # Add Mapbox Access Token
        fig.update_layout(mapbox_accesstoken=mapbox_access_token)

    # Display the map in Streamlit
        st.plotly_chart(fig)

# DataFrame in col2
    with col2:
    # Display the DataFrame of cities and counts in the second column, setting 'City' as the index
        city_counts = city_counts[['City', 'Count']]  # Select only City and Count columns
        city_counts.set_index('City', inplace=True)  # Set City as the index
    
        st.write(f"City Counts for Subject: {selected_subject_code}")
        st.dataframe(city_counts)  # Display the dataframe


# Citation Page
def citation_page():
    """Display the citation page."""
    script_dir = os.path.dirname(__file__)  # Ensure correct directory
    file_path = os.path.join(script_dir, "../results/final_data.csv")
    df = load_data(file_path)

    # Ensure 'cover_date' is in datetime format
    if 'Cover Date' in df.columns:
        df['Cover Date'] = pd.to_datetime(df['Cover Date'], errors='coerce')

        # Sidebar filters for date range
        st.sidebar.header("Filter Options")
        # Ensure the min and max dates are valid datetime.date objects
        start_date = st.sidebar.date_input("Start Date", df['Cover Date'].min().date())
        end_date = st.sidebar.date_input("End Date", df['Cover Date'].max().date())

        # Filter data based on the selected date range
        filtered_data = df[(df['Cover Date'] >= pd.to_datetime(start_date)) & 
                           (df['Cover Date'] <= pd.to_datetime(end_date))]
        total_entries = len(filtered_data)
        unique_categories = filtered_data['Subject Area'].nunique()
        total_citations = filtered_data['Citation Count'].sum() if 'Citation Count' in filtered_data.columns else 0

            # Display KPI Cards with a more visually appealing layout
        st.markdown("### Key Metrics")
        kpi_cols = st.columns(3)
        with kpi_cols[0]:
            st.metric("Total Entries", total_entries)
        with kpi_cols[1]:
            st.metric("Unique Categories", unique_categories)
        with kpi_cols[2]:
            st.metric("Total Citations", total_citations)
        # Citation Trends Over Time
        st.markdown("### Citation Trends Over Time")
        if 'Citation Count' in filtered_data.columns:
            citation_trend = filtered_data.groupby('Cover Date')['Citation Count'].sum().reset_index()
            fig_trend = px.line(
                citation_trend,
                x='Cover Date',
                y='Citation Count',
                title="Citation Trends Over Time",
                labels={"Cover Date": "Publication Date", "Citation Count": "Total Citations"},
                template="plotly_white",
            )
            fig_trend.update_layout(
                xaxis_title="Date",
                yaxis_title="Citations",
                hovermode="x unified",
                plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
            )
            st.plotly_chart(fig_trend, use_container_width=True)

        # Citations by Category
        st.markdown("### Average citations by Category")
        if 'Citation Count' in filtered_data.columns:
            # Calculate total citations by category
            citations_by_category = filtered_data.groupby('Subject Area')['Citation Count'].mean().reset_index()
            citations_by_category.columns = ['Subject Areas', 'Average Citations']
            citations_by_category['Average Citations'] = citations_by_category['Average Citations'].round(3)
            citations_by_category = citations_by_category.sort_values(by='Average Citations', ascending=False)

            fig_citations = px.bar(
                citations_by_category,
                x="Average Citations",
                y="Subject Areas",
                orientation='h',
                text="Average Citations",
                title="Citations by Category",
                labels={"Average Citations": "Average Citations", "Subject Areas": "Subject Areas"},
                template="plotly_white",
            )
            fig_citations.update_traces(texttemplate='%{text}', textposition='outside')
            fig_citations.update_layout(xaxis_title="Average Citations", yaxis_title="Subject Areas")
            st.plotly_chart(fig_citations, use_container_width=True)

# Main Function
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page:", ["Subject Areas Popularity", "Citation"])

    if page == "Subject Areas Popularity":
        category_popularity_page()
    elif page == "Citation":
        citation_page()

if __name__ == "__main__":
    main()
