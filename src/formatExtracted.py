import pandas as pd
from collections import Counter

# Load CSV into DataFrame
df = pd.read_csv('C:/Users/PangSunatcha/OneDrive - Chulalongkorn University/Documents/Y2S1 files/Data Sci/proj/Data-Sci-project/localresults/extracted_data.csv')

def findsa(list):
    
    count = Counter(list)
    max_count = 0
    most_frequent_item = None
    
    # Iterate through the list and find the item with the highest count
    for item in list:
        if count[item] > max_count:
            max_count = count[item]
            most_frequent_item = item
        # If there's a tie in count, no need to update since we return the first one
    return most_frequent_item
    
df['Subject Areas'] = df['Subject Areas'].str.split(', ').apply(findsa)

subject_map = {
    "AGRI": "Agricultural and Biological Sciences", "ARTS": "Arts and Humanities", "BIOC": "Biochemistry",
    "BUSI": "Business", "CENG": "Chemical Engineering",
    "CHEM": "Chemistry", "COMP": "Computer Science", "DECI": "Decision Sciences", "DENT": "Dentistry",
    "EART": "Earth and Planetary Sciences", "ECON": "Econometrics and Finance", "ENER": "Energy",
    "ENGI": "Engineering", "ENVI": "Environmental Science", "HEAL": "Health Professions",
    "IMMU": "Immunology and Microbiology", "MATE": "Materials science", "MATH": "Mathematics",
    "MEDI": "Medicine", "NEUR": "Neuroscience", "NURS": "Nursing",
    "PHAR": "Toxicology and Pharmaceutics", "PHYS": "Physics and Astronomy", "PSYC": "Psychology",
    "SOCI": "Social Sciences", "VETE": "Veterinary", "MULT": "Multidisciplinary"
}


df['Subject Areas'] = df['Subject Areas'].map(subject_map)

df.to_csv('C:/Users/PangSunatcha/OneDrive - Chulalongkorn University/Documents/Y2S1 files/Data Sci/proj/Data-Sci-project/results/formatted_subjectAreas.csv', index=False)
