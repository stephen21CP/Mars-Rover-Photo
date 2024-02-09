#travel_data_controller.py
from flask import Flask, render_template, request, redirect, url_for
import csv
import time
from pymongo import MongoClient


from travel_data_model import load_initial_data
from travel_data_model import TravelRecord



app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
if 'travel_records_db' in client.list_database_names():
    client.drop_database('travel_records_db')
db = client['travel_records_db']
collection = db['travel_records']


# Initialize an empty list to store TravelRecord objects
travel_records = []

# Call load_initial_data to load the original dataset when the application starts
travel_records = load_initial_data()

# Load initial data into MongoDB if the collection is empty
if collection.count_documents({}) == 0:
    initial_data = load_initial_data()
    for record in initial_data:
        collection.insert_one(record.__dict__)



# Route to display a list of TravelRecords
@app.route('/')
def list_records():
    
    travel_records = list(collection.find())
    # Add a timestamp to the URL to prevent caching
    timestamp = int(time.time())  # Get the current timestamp
    return render_template('list_records.html', records=travel_records, timestamp=timestamp)


# Route to add a new TravelRecord
@app.route('/add_record', methods=['GET', 'POST'])
def add_record():
    if request.method == 'POST':
        # Process the form data and create a new TravelRecord
        ref_number = request.form['ref_number']
        disclosure_group = request.form['disclosure_group']
        title_en = request.form['title_en']
        title_fr = request.form['title_fr']
        name = request.form['name']
        purpose_en = request.form['purpose_en']
        purpose_fr = request.form['purpose_fr']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        destination_en = request.form['destination_en']
        destination_fr = request.form['destination_fr']
        airfare = request.form['airfare']
        other_transport = request.form['other_transport']
        lodging = request.form['lodging']
        meals = request.form['meals']
        other_expenses = request.form['other_expenses']
        total = request.form['total']
        additional_comments_en = request.form['additional_comments_en']
        additional_comments_fr = request.form['additional_comments_fr']
        owner_org = request.form['owner_org']
        owner_org_title = request.form['owner_org_title']
        # Create a new TravelRecord object
        new_record = TravelRecord(
            ref_number, disclosure_group, title_en, title_fr, name,
            purpose_en, purpose_fr, start_date, end_date,
            destination_en, destination_fr, airfare, other_transport,
            lodging, meals, other_expenses, total,
            additional_comments_en, additional_comments_fr,
            owner_org, owner_org_title
        )
        # Insert the new record into MongoDB
        collection.insert_one(new_record.__dict__)
        # Redirect to the list of travel records
        return redirect(url_for('list_records'))
    return render_template('add_record.html')



# Route to view a single TravelRecord
@app.route('/view_record/<record_id>')
def view_record(record_id):
    # Fetch the record based on the ref_number
    return render_template('view_record.html', record=collection.find_one({'ref_number': record_id}))

# Route to edit a single TravelRecord
@app.route('/edit_record/<string:record_id>', methods=['GET', 'POST'])
def edit_record(record_id):
    if request.method == 'POST':
        # Process the form data and update the TravelRecord
        new_ref_number = request.form['ref_number']
        new_disclosure_group = request.form['disclosure_group']
        new_title_en = request.form['title_en']
        new_title_fr = request.form['title_fr']
        new_name = request.form['name']
        new_purpose_en = request.form['purpose_en']
        new_purpose_fr = request.form['purpose_fr']
        new_start_date = request.form['start_date']
        new_end_date = request.form['end_date']
        new_destination_en = request.form['destination_en']
        new_destination_fr = request.form['destination_fr']
        new_airfare = request.form['airfare']
        new_other_transport = request.form['other_transport']
        new_lodging = request.form['lodging']
        new_meals = request.form['meals']
        new_other_expenses = request.form['other_expenses']
        new_total = request.form['total']
        new_additional_comments_en = request.form['additional_comments_en']
        new_additional_comments_fr = request.form['additional_comments_fr']
        new_owner_org = request.form['owner_org']
        new_owner_org_title = request.form['owner_org_title']

        updated_record = TravelRecord(
            new_ref_number, new_disclosure_group, new_title_en, new_title_fr, new_name,
            new_purpose_en, new_purpose_fr, new_start_date, new_end_date,
            new_destination_en, new_destination_fr, new_airfare, new_other_transport,
            new_lodging, new_meals, new_other_expenses, new_total,
            new_additional_comments_en, new_additional_comments_fr,
            new_owner_org, new_owner_org_title
        )      
       # Update the existing record in MongoDB
        collection.update_one({"ref_number": record_id}, {"$set": updated_record.__dict__})
        
        return redirect(url_for('list_records', _update_cache=int(time.time())))

    return render_template('edit_record.html', record=collection.find_one({"ref_number": record_id}))


# Route to delete a single TravelRecord
@app.route('/delete_record/<string:record_id>')
def delete_record(record_id):

    result = collection.delete_one({"ref_number": record_id})

    if result.deleted_count > 0:

        # Redirect to the list_records page after deletion
        return redirect(url_for('list_records'))
    else:
        # Handle the case where the record_id is out of range
        return "Record not found"


# Route to search for records based on input
@app.route('/search_records', methods=['GET'])
def search_records():
    # Get the search term from the query parameters
    search_term = request.args.get('search')

    # If the search term is provided, perform the search using $text index
    if search_term:
        # Use the $text operator for searching
        query = {'$text': {'$search': search_term}}

        # Perform the search and get the results
        search_results = list(collection.find(query, {'score': {'$meta': 'textScore'}}))

        # Sort the results by text score (optional)
        search_results.sort(key=lambda x: x['score'], reverse=True)

        # Render the template with the search results
        return render_template('list_records.html', records=search_results, timestamp=int(time.time()))

    # If no search term is provided, redirect to the list_records page
    return redirect(url_for('list_records', _update_cache=int(time.time())))


if __name__ == '__main__':
    # Create a text index on all fields in the collection
    collection.create_index([('$**', 'text')])
    app.run(debug=True)
