import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Path relative to the script's directory
script_dir = os.getcwd()
print(script_dir)
@st.cache_data
def load_data(file_path):
    """Load the CSV file and return a DataFrame."""
    return pd.read_csv(file_path)

def category_popularity_page():
    """Display the category popularity page."""
    # Load the data
    file_path = os.path.join(script_dir, "results/predicts.csv")
    #file_path = "results/predicts.csv"  # Replace with your actual file path
    df = load_data(file_path)

    # Ensure 'cover_date' column is in datetime format
    if 'cover_date' in df.columns and 'predicted subject areas' in df.columns:
        df['cover_date'] = pd.to_datetime(df['cover_date'])
        
        # Sidebar filters for date range
        st.sidebar.header("Filter Options")
        start_date = st.sidebar.date_input("Start Date", df['cover_date'].min())
        end_date = st.sidebar.date_input("End Date", df['cover_date'].max())

        # Filter data based on date range
        filtered_data = df[(df['cover_date'] >= pd.to_datetime(start_date)) & 
                           (df['cover_date'] <= pd.to_datetime(end_date))]

        # Group by categories and count occurrences
        category_counts = filtered_data['predicted subject areas'].value_counts().reset_index()
        category_counts.columns = ['Subject Areas', 'Count']

        # Display the filtered data and summary
        st.header("Popular Subject Areas")
        st.write(f"Date Range: {start_date} to {end_date}")
        st.write(filtered_data)

        # Plot the data
        st.subheader("Subject Areas Popularity")
        fig_bar = px.bar(
            category_counts,
            x="Count",
            y="Subject Areas",
            orientation='h',  # Horizontal bar chart
            text="Count",  # Show the count on bars
            title="Popular Subject Areas in Selected Date Range",
            labels={"Count": "Total Count", "Subject Areas": "Subject Areas"},
            template="plotly_white",
        )
        fig_bar.update_traces(texttemplate='%{text}', textposition='outside')
        fig_bar.update_layout(
            xaxis_title="Count",
            yaxis_title="Subject Areas",
            hovermode="closest",
        )
        st.plotly_chart(fig_bar)


        # Time series for citation trends
        st.subheader("Citation Trend Over Time")
        if 'cited_by_count' in df.columns:
            # Group by 'cover_date' and calculate the sum of 'cited_by_count'
            citation_trend = filtered_data.groupby('cover_date')['cited_by_count'].sum().reset_index()

            # Plot the time series
            fig_line = px.line(
                citation_trend,
                x='cover_date',
                y='cited_by_count',
                title="Citation Trend Over Time",
                labels={"cover_date": "Publication Date", "cited_by_count": "Total Citations"},
                template="plotly_white"
            )
            fig_line.update_layout(
                xaxis_title="Date",
                yaxis_title="Citations",
                hovermode="x unified",
            )
            st.plotly_chart(fig_line)
        
       
            
    else:
        st.error("The CSV file must contain 'cover_date' and 'predicted subject areas' columns.")

# Main Function
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page:", ["Subject Areas Popularity"])

    if page == "Subject Areas Popularity":
        category_popularity_page()

if __name__ == "__main__":
    main()
