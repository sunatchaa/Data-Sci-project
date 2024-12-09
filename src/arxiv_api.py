import requests
import xmltodict
import pandas as pd

# Function to fetch data from the ArXiv API
def fetch_arxiv_data(query, start_index, max_results):
    url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": query,
        "start": start_index,
        "max_results": max_results
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data_dict = xmltodict.parse(response.content)
        arxiv_data = data_dict.get('feed', {}).get('entry', [])
        return arxiv_data if isinstance(arxiv_data, list) else [arxiv_data]
    else:
        print(f"Error: {response.status_code}")
        return []

# Function to process ArXiv data into a structured format
def process_arxiv_data(entries):
    processed_data = []
    for entry in entries:
        # Handle multiple authors
        if isinstance(entry.get('author'), list):
            authors = ", ".join([author['name'] for author in entry['author']])
        else:
            authors = entry['author']['name'] if 'author' in entry else ""

        # Process entry
        processed_entry = {
            "ID": entry.get('id', ''),
            "Title": entry.get('title', '').replace('\n', '').strip(),
            "Abstract": entry.get('summary', '').replace('\n', '').strip(),
            "Authors": authors,
            "Published Date": entry.get('published', ''),
            "Updated Date": entry.get('updated', ''),
            "Comments": entry.get('arxiv:comment', {}).get('#text', '') if 'arxiv:comment' in entry else "",
            "Primary Category": entry.get('arxiv:primary_category', {}).get('@term', ''),
            "PDF Link": next(
                (link['@href'] for link in entry.get('link', []) if link.get('@title') == 'pdf'), None
            ),
            "Language": "eng"
        }
        processed_data.append(processed_entry)
    return processed_data

# Fetch and process 1000 entries
all_entries = []
batch_size = 100  # ArXiv API limits to 100 results per request
for start in range(0, 300, 100):
    batch_entries = fetch_arxiv_data("data science", start, batch_size)
    if not batch_entries:
        break  # Stop if no more data
    all_entries.extend(process_arxiv_data(batch_entries))

# Convert to pandas DataFrame
df = pd.DataFrame(all_entries)
print(df)
# Save to CSV
csv_file = "arxiv_data.csv"
df.to_csv(csv_file, index=False, encoding="utf-8")

print(f"Successfully saved {len(df)} entries to {csv_file}.")



