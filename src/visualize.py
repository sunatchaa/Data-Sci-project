import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

@st.cache_data
def load_data(file_path):
    """Load the CSV file and return a DataFrame."""
    return pd.read_csv(file_path)

def category_popularity_page():
    """Display the category popularity page."""
    # Load the data
    file_path = "/Users/dear/Data Science/Project/Data-Sci-project/results/predicts.csv"  # Replace with your actual file path
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
        st.subheader("Subject areas Popularity")
        # fig, ax = plt.subplots(figsize=(8, 6))
        # sns.barplot(data=category_counts, x='Count', y='Subject Areas', ax=ax)
        # plt.title("Popular Subject Areas in Selected Date Range")
        # plt.xlabel("Count")
        # plt.ylabel("Subject Areas")
        # st.pyplot(fig)
        fig = px.bar(
            category_counts,
            x="Count",
            y="Subject Areas",
            orientation='h',  # Horizontal bar chart
            text="Count",  # Show the count on bars
            title="Popular Subject Areas in Selected Date Range",
            labels={"Count": "Total Count", "Subject Areas": "Subject Areas"},
            template="plotly_white",
        )
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        fig.update_layout(
            xaxis_title="Count",
            yaxis_title="Subject Areas",
            hovermode="closest",
        )
        st.plotly_chart(fig)
    else:
        st.error("The CSV file must contain 'cover_date' and 'categories' columns.")

# Example of how to integrate this into a larger app
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page:", ["Subject areas Popularity", "Other Feature"])

    if page == "Subject areas Popularity":
        category_popularity_page()
    elif page == "Other Feature":
        st.write("This is another feature page.")

if __name__ == "__main__":
    main()