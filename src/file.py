import os
import glob
import json
import pandas as pd

# Initialize a list to store titles
titles = []

# List of folders to process
folders = ['data_science/2018', 'data_science/2019', 'data_science/2020', 'data_science/2021', 'data_science/2022', 'data_science/2023']  # Add more folders as needed

# Iterate through each folder
for folder_path in folders:
    print(f"Processing folder: {folder_path}")
    
    # Iterate through files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        
data_rows = []

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
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
    except KeyError as e:
        print(f"KeyError for file {file_path}: {e}")
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError for file {file_path}: {e}")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
    return None


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


df = pd.DataFrame(data_rows)

# Display the DataFrame
print(df)
print(data_rows)