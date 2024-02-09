#travel_data_model.py
import csv
import os  # Add this import for file existence check

# Define the TravelRecord class with attributes
# Define the TravelRecord class with attributes
class TravelRecord:
    def __init__(self, ref_number, disclosure_group, title_en, title_fr, name, purpose_en, purpose_fr,
                 start_date, end_date, destination_en, destination_fr, airfare, other_transport, lodging,
                 meals, other_expenses, total, additional_comments_en, additional_comments_fr,
                 owner_org, owner_org_title):
        self.ref_number = ref_number
        self.disclosure_group = disclosure_group
        self.title_en = title_en
        self.title_fr = title_fr
        self.name = name
        self.purpose_en = purpose_en
        self.purpose_fr = purpose_fr
        self.start_date = start_date
        self.end_date = end_date
        self.destination_en = destination_en
        self.destination_fr = destination_fr
        self.airfare = airfare
        self.other_transport = other_transport
        self.lodging = lodging
        self.meals = meals
        self.other_expenses = other_expenses
        self.total = total
        self.additional_comments_en = additional_comments_en
        self.additional_comments_fr = additional_comments_fr
        self.owner_org = owner_org
        self.owner_org_title = owner_org_title
    
    # Function to read data from CSV file and create TravelRecord objects
def read_data_from_csv(file_name, num_records=None):
    records = []
    try:
        with open(file_name, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            # Skip header row
            next(csv_reader)
            for i, row in enumerate(csv_reader):
                if num_records is not None and i >= num_records:
                    break
                if len(row) >= 20:  # Ensure all columns are present
                    record = TravelRecord(*row)
                    records.append(record)
    except FileNotFoundError:
        print("Error: File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return records



# Define the load_initial_data function to load the original
#  dataset 'travelq.csv' once at the beginning
def load_initial_data():
    # Initialize an empty list to store TravelRecord objects
    travel_records = []
    travel_records = read_data_from_csv('travelq.csv', num_records=100)
    return travel_records


#travel_data_model.py
# Define the load_data function to load data from a specified file
def load_data(file_name):
    
    # Initialize an empty list to store TravelRecord objects
    travel_records = []    

    # Check if the specified file exists
    if os.path.exists(file_name):
        travel_records = read_data_from_csv(file_name)
    else:
        # If the file does not exist, load from the original dataset 'travelq.csv'
        load_initial_data()
    return travel_records
