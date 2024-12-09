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
    script_dir = os.path.dirname(__file__)  # Ensure correct directory
    file_path = os.path.join(script_dir, "../results/predicts.csv")
    df = load_data(file_path)

    # Ensure 'cover_date' column is in datetime format

    if 'cover_date' in df.columns and 'predicted subject areas' in df.columns:
            df['cover_date'] = pd.to_datetime(df['cover_date'], errors='coerce')

            # Sidebar filters for date range
            st.sidebar.header("Filter Options")
            start_date = st.sidebar.date_input("Start Date", df['cover_date'].min())
            end_date = st.sidebar.date_input("End Date", df['cover_date'].max())

            # Filter data based on date range
            filtered_data = df[(df['cover_date'] >= pd.to_datetime(start_date)) & 
                               (df['cover_date'] <= pd.to_datetime(end_date))]

            # Calculate KPI metrics
            total_entries = len(filtered_data)
            unique_categories = filtered_data['predicted subject areas'].nunique()
            total_citations = filtered_data['cited_by_count'].sum() if 'cited_by_count' in filtered_data.columns else 0

            # Display KPI Cards with a more visually appealing layout
            st.markdown("### Key Metrics")
            kpi_cols = st.columns(3)
            with kpi_cols[0]:
                st.metric("Total Entries", total_entries)
            with kpi_cols[1]:
                st.metric("Unique Categories", unique_categories)
            with kpi_cols[2]:
                st.metric("Total Citations", total_citations)

            # Bar Chart: Subject Areas Popularity
            st.markdown("### Subject Areas Popularity")
            category_counts = filtered_data['predicted subject areas'].value_counts().reset_index()
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

            # Time Series Chart: Citation Trends Over Time
            st.markdown("### Citation Trends Over Time")
            if 'cited_by_count' in filtered_data.columns:
                citation_trend = filtered_data.groupby('cover_date')['cited_by_count'].sum().reset_index()
                fig_trend = px.line(
                    citation_trend,
                    x='cover_date',
                    y='cited_by_count',
                    title="Citation Trends Over Time",
                    labels={"cover_date": "Publication Date", "cited_by_count": "Total Citations"},
                    template="plotly_white",
                )
                fig_trend.update_layout(
                    xaxis_title="Date",
                    yaxis_title="Citations",
                    hovermode="x unified",
                    plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
                )
                st.plotly_chart(fig_trend, use_container_width=True)

                # Add a new section for Citations by Category
                st.markdown("### Citations by Category")
                if 'cited_by_count' in filtered_data.columns:
                    # Calculate total citations by category
                    citations_by_category = filtered_data.groupby('predicted subject areas')['cited_by_count'].sum().reset_index()
                    citations_by_category.columns = ['Subject Areas', 'Total Citations']
                    citations_by_category = citations_by_category.sort_values(by='Total Citations', ascending=False)

                    # Horizontal bar chart
                    fig_citations = px.bar(
                        citations_by_category,
                        x="Total Citations",
                        y="Subject Areas",
                        orientation='h',
                        text="Total Citations",
                        title="Citations by Category",
                        labels={"Total Citations": "Total Citations", "Subject Areas": "Subject Areas"},
                        template="plotly_white",
                    )
                    fig_citations.update_traces(texttemplate='%{text}', textposition='outside')
                    fig_citations.update_layout(xaxis_title="Total Citations", yaxis_title="Subject Areas")
                    st.plotly_chart(fig_citations, use_container_width=True)

            else:
                st.error("The CSV file must contain 'cover_date' and 'predicted subject areas' columns.")
    else:
        st.warning("Please upload a CSV file to proceed.")

# Main Function
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page:", ["Subject Areas Popularity"])

    if page == "Subject Areas Popularity":
        category_popularity_page()

if __name__ == "__main__":
    main()
