import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from st_aggrid import AgGrid, GridOptionsBuilder

# Page configuration
st.set_page_config(layout="wide")

# Title
st.title("Mortal's Data Analyzer")

# Current date
current_date = datetime.today()
current_month_year = current_date.strftime('%Y-%m')

# Load data
@st.cache_data
def load_data():
    ranked_df = pd.read_csv("./data/ranked_games.csv")
    public_df = pd.read_csv("./data/public_games.csv")
    return ranked_df, public_df

ranked_df, public_df = load_data()

# Function to convert UTC Timestamp to datetime
def convert_timestamp(df):
    # If 'UTC Timestamp' is a string, convert it directly to datetime
    if df['UTC Timestamp'].dtype == 'object':
        df['UTC Timestamp'] = pd.to_datetime(df['UTC Timestamp'])
    return df

ranked_df = convert_timestamp(ranked_df)
public_df = convert_timestamp(public_df)

# Plot the evolution of Skill for the ranked DataFrame with Y-axis limits
fig_ranked = px.line(ranked_df, x='UTC Timestamp', y='Skill', title='Rankeds')
fig_ranked.update_layout(yaxis=dict(range=[0, 500]))  # Set Y-axis range
# Display the ranked plot
st.plotly_chart(fig_ranked, use_container_width=True)

# Display the ranked DataFrame with filtering capability
st.subheader("Ranked Games Data")
# Build grid options for filtering
gb_ranked = GridOptionsBuilder.from_dataframe(ranked_df)
gb_ranked.configure_pagination(paginationPageSize=10)  # Pagination
gb_ranked.configure_default_column(filterable=True)  # Enable filtering on all columns
grid_options_ranked = gb_ranked.build()

# Show the AgGrid with the ranked data
AgGrid(ranked_df, gridOptions=grid_options_ranked, enable_enterprise_modules=True)

# Plot the evolution of Skill for the public DataFrame with Y-axis limits
fig_public = px.line(public_df, x='UTC Timestamp', y='Skill', title='Public Games')
fig_public.update_layout(yaxis=dict(range=[0, 530]))  # Set Y-axis range
# Display the public plot
st.plotly_chart(fig_public, use_container_width=True)

# Display the public DataFrame with filtering capability
st.subheader("Public Games Data")
# Build grid options for filtering
gb_public = GridOptionsBuilder.from_dataframe(public_df)
gb_public.configure_pagination(paginationPageSize=10)  # Pagination
gb_public.configure_default_column(filterable=True)  # Enable filtering on all columns
grid_options_public = gb_public.build()

# Show the AgGrid with the public data
AgGrid(public_df, gridOptions=grid_options_public, enable_enterprise_modules=True)
