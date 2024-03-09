import streamlit as st
import pandas as pd

from pc_formater import PCFormatter

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
def main():
    st.title('PlaidComp - Prototype')

    # File uploader allows user to add their own CSV
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file is not None:
        # Read the CSV file into a pandas dataframe
        df = pd.read_csv(uploaded_file)

        # Display the original dataframe
        st.write("Original Data:")
        st.dataframe(df)

        # Button to clean data
        if st.button('Clean Data'):
            # Call the clean_dataframe function to clean and preprocess the dataframe
            cleaned_df = clean_dataframe(df)

            # Display the cleaned dataframe
            st.write("Cleaned Data:")
            st.dataframe(cleaned_df)
        else:
            # If the button is not clicked, display a message
            st.write("Click the 'Clean Data' button to clean the data.")

if __name__ == "__main__":
    main()
