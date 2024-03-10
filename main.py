import os

import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt

from pc_formater import PCFormatter
from realestateanalystics import RealEstateAnalytics
INTERNAL_TO_EXTERNAL_COLUMN_MAPPING = {
    'ID': 'Centris No.',
    'Address': 'Address',
    'Asking Price': 'Asked/Sold Price',
    'Bathrooms': 'Bathrooms (number)',
    'Bedrooms': 'Bedrooms (number)',
    'DOM': 'DOM',
    'Living Area': 'Living Area (Imperial)',
    'Garage': 'Garage (number)',
    'Lot Area': 'Lot Area (Imperial)',
    'Municipality': 'Mun./Bor.',
    'Rooms': 'Rms',
    'Sold Price': 'Sold / Rented Price',
    'Status': 'ST',
}


def get_pdf_file():
    """
    Generate or retrieve a PDF file and return the file path.
    This is a placeholder function. You should implement the logic to generate
    or retrieve your PDF file and return its path.
    """
    # Placeholder for PDF generation/retrieval logic
    pdf_file_path = 'path/to/your/pdf_file.pdf'
    return pdf_file_path

def map_columns_to_index(df):
    # Create a dictionary to hold the mapping of your column names to the external index or None
    column_index_mapping = {}

    # Iterate through the internal column names and their corresponding external names
    for internal_name, external_name in INTERNAL_TO_EXTERNAL_COLUMN_MAPPING.items():
        # Use the get_loc method to find the index, if the column doesn't exist, set to None
        column_index_mapping[internal_name] = df.columns.get_loc(external_name) if external_name in df.columns else None

    return column_index_mapping

# Function to clean the dataframe could go here
def clean_dataframe(df):
    column_mapping = map_columns_to_index(df)
    formatter = PCFormatter(column_mapping)
    formatted_frame = formatter.create_pc_format_frame(df)
    cleaned_frame = formatter.clean_numeric_columns(formatted_frame,
                                                    ['Bathrooms', 'Bedrooms', 'DOM', 'Living Area', 'Garage',
                                                     'Lot Area', 'Rooms', 'Sold Price'])
    return cleaned_frame

def get_pdf_file():
    """
    Generate or retrieve a PDF file and return the file path.
    This is a placeholder function. You should implement the logic to generate
    or retrieve your PDF file and return its path.
    """
    # Placeholder for PDF generation/retrieval logic
    pdf_file_path = 'files/response-10.pdf'
    return pdf_file_path



def main():
    st.title('PlaidComp - Prototype')

    if 'action' not in st.session_state:
        st.session_state.action = 'upload'

    if 'previous_action' not in st.session_state:
        st.session_state.previous_action = None

    if st.session_state.action == 'upload':
        uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.session_state.df = df
            st.subheader('Original Data')
            st.dataframe(df)

            if st.button('Clean Data'):
                cleaned_df = clean_dataframe(df)  # Assume this function exists
                st.session_state.df = cleaned_df  # Store cleaned DataFrame in session state
                st.session_state.previous_action = 'upload'
                st.session_state.action = 'cleaned'
                st.experimental_rerun()

    elif st.session_state.action == 'cleaned':
        st.subheader('Cleaned Data')
        st.dataframe(st.session_state.df)

        if st.button('Generate Comp'):
            analytics = RealEstateAnalytics()  # Assume this class is defined
            statistics = analytics.calculate_statistics(st.session_state.df)  # Assume this method exists
            st.session_state.statistics = statistics
            st.session_state.previous_action = 'cleaned'
            st.session_state.action = 'stats'
            st.experimental_rerun()

        if st.button('Go Back'):
            st.session_state.action = st.session_state.previous_action
            st.experimental_rerun()

    elif st.session_state.action == 'stats':
        # Remove scatter plot data from statistics before displaying as JSON
        plot_keys = ['Graph - Sqft/Price X', 'Graph - Sqft/Price Y', 'Graph - Sold Price/DOM X',
                     'Graph - Sold Price/DOM Y']
        statistics_no_plots = {key: val for key, val in st.session_state.statistics.items() if key not in plot_keys}
        st.json(statistics_no_plots)

        if 'Graph - Sqft/Price X' in st.session_state.statistics and 'Graph - Sqft/Price Y' in st.session_state.statistics:
            plt.figure()
            plt.scatter(st.session_state.statistics['Graph - Sqft/Price X'],
                        st.session_state.statistics['Graph - Sqft/Price Y'])
            plt.title('Sqft vs Price')
            plt.xlabel('Sqft')
            plt.ylabel('Price')
            st.pyplot(plt)

        if 'Graph - Sold Price/DOM X' in st.session_state.statistics and 'Graph - Sold Price/DOM Y' in st.session_state.statistics:
            plt.figure()
            plt.scatter(st.session_state.statistics['Graph - Sold Price/DOM X'],
                        st.session_state.statistics['Graph - Sold Price/DOM Y'])
            plt.title('Sold Price vs DOM')
            plt.xlabel('DOM')
            plt.ylabel('Sold Price')
            st.pyplot(plt)

        if st.button('Generate PDF'):
            st.session_state.previous_action = 'stats'
            st.session_state.action = 'generate_pdf'
            st.experimental_rerun()

        if st.button('Go Back'):
            st.session_state.action = st.session_state.previous_action
            st.experimental_rerun()





    elif st.session_state.action == 'generate_pdf':
        pdf_file_path = get_pdf_file()  # Get the PDF file path
        if os.path.exists(pdf_file_path):
            with open(pdf_file_path, "rb") as pdf_file:
                st.download_button(
                    label="Download PDF",
                    data=pdf_file,
                    file_name="generated_report.pdf",
                    mime="application/octet-stream"
                )

        if st.button('Go Back'):
            st.session_state.action = st.session_state.previous_action
            st.experimental_rerun()
    else:
        st.error("PDF file not found.")

        if st.button('Go Back to Stats'):
            st.session_state.action = 'stats'
            st.experimental_rerun()

        # Display scatter plots after displaying the rest of the statistics



if __name__ == "__main__":
    main()