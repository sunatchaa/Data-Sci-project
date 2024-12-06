import pandas as pd
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

# Function to clean and split text
def clean_and_split_text(text, stop_words):
    # Split the text into words, filter out stop words
    cleaned_words = [word for word in text.lower().split() if word not in stop_words]
    return cleaned_words  # Return the list of words

# Read the CSV file
input_file = '/Users/pimmadaaphiwetsa/Downloads/data_formatted_subjectAreas.csv'  # Replace with your file path
data = pd.read_csv(input_file)

# Apply the function to the 'Publication Name' column
data['Cleaned and Split Publication Name'] = data['Publication Name'].apply(
    lambda x: clean_and_split_text(str(x), ENGLISH_STOP_WORDS)
)

# Save the processed DataFrame to a new CSV file
output_file = 'processed_subjectAreas.csv'  # Replace with your desired output file path
data.to_csv(output_file, index=False)

print(f"Processed data saved to {output_file}")
