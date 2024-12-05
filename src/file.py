
import os
import glob
import json
import pandas as pd

# Base directory containing year folders
base_dir = "data_science"  # Change to your actual directory

# Function to process a single JSON file using provided functions
def process_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)  # Load JSON data
    # Extract data using the provided functions
    return {
        "Cited By Count": citedByCount(data),
        "Title": title(data),
        "Description": description(data),
        "Cover Date": coverDate(data),
        "Aggregation Type": aggregationType(data),
        "Authors": ", ".join(author(data)) if author(data) else None,
        "Subject Areas": ", ".join(subjectArea(data)) if subjectArea(data) else None,
        "Author Keywords": ", ".join(authKeyword(data)) if authKeyword(data) else None,
        "Abstract": abstract(data),
        "Reference Count": refCount(data),
        "Source ID": sourceID(data)
    }

# Function to process all files in a folder for a specific year
def process_year_folder(folder_path, year):
    rows = []
    for file_path in glob.glob(os.path.join(folder_path, "*.json")):  # Assuming JSON files
        row = process_file(file_path)
        row['Year'] = year  # Add the year to the row
        rows.append(row)
    return rows

# Function to process all year folders and create a DataFrame
def create_dataframe_from_folders(base_dir):
    all_rows = []
    for year_folder in sorted(os.listdir(base_dir)):  # Iterate over year folders
        year_path = os.path.join(base_dir, year_folder)
        if os.path.isdir(year_path) and year_folder.isdigit():  # Check if it's a valid year folder
            year_rows = process_year_folder(year_path, year_folder)
            all_rows.extend(year_rows)
    return pd.DataFrame(all_rows)


def citedByCount(data):
    if 'citedby-count' not in data['abstracts-retrieval-response']['coredata'].keys():
        return None
    else:
        return data['abstracts-retrieval-response']['coredata']['citedby-count'] 

def title(data):
    if 'dc:title' not in data['abstracts-retrieval-response']['coredata'].keys():
        return None
    else:
        return data['abstracts-retrieval-response']['coredata']['dc:title']

def description(data):
    if 'dc:description' not in data['abstracts-retrieval-response']['coredata'].keys():
        return None
    else:
        return data['abstracts-retrieval-response']['coredata']['dc:description']

def coverDate(data):
    if 'prism:coverDate' not in data['abstracts-retrieval-response']['coredata'].keys():
        return None
    else:
        return data['abstracts-retrieval-response']['coredata']['prism:coverDate']

def aggregationType(data):
    if 'prism:aggregationType' not in data['abstracts-retrieval-response']['coredata'].keys():
        return None
    else:
        return data['abstracts-retrieval-response']['coredata']['prism:aggregationType']

def author(data):
    authors = data['abstracts-retrieval-response']['authors']['author']
    authors_name = []
    for a in authors:
        name = a["ce:given-name"]
        surname = a["ce:surname"]
        authors_name.append(name+' '+surname)
    return authors_name

def subjectArea(data):
    if 'subject-area' not in data['abstracts-retrieval-response']['subject-areas'].keys():
        return None
    else:
        subjects = data['abstracts-retrieval-response']['subject-areas']['subject-area']
        subject = []
        for s in subjects:
            subject.append(s['$'])
        return subject

def authKeyword(data):
    if (data['abstracts-retrieval-response']['authkeywords'] is None):
        return None
    else:
        keywords = data['abstracts-retrieval-response']['authkeywords']['author-keyword']
        keyword = []
        for k in keywords:
            keyword.append(k['$'])
        return keyword

def abstract(data):
    if 'abstracts' not in data['abstracts-retrieval-response']['item']['bibrecord']['head'].keys():
        return None
    else:
        return data['abstracts-retrieval-response']['item']['bibrecord']['head']['abstracts'] 

def refCount(data):
    if '@refcount' not in data['abstracts-retrieval-response']['item']['bibrecord']['tail']['bibliography'].keys():
        return None
    else:
        return data['abstracts-retrieval-response']['item']['bibrecord']['tail']['bibliography']['@refcount']

def sourceID(data):
    if 'source-id' not in data['abstracts-retrieval-response']['coredata'].keys():
        return None
    else:
        return data['abstracts-retrieval-response']['coredata']['source-id']

# Main execution
df = create_dataframe_from_folders(base_dir)

# Display the DataFrame
print(df)
<<<<<<< HEAD
print(data_rows)
=======
>>>>>>> 946098c78d2bab8c0263251a05f127389b0de6fd
