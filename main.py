from flask import Flask, render_template, request, jsonify
import pymysql

app = Flask(__name__)

# MySQL Configuration
db = pymysql.connect(
    host="localhost",
    user="root",
    password="Suraaj0604$",
    database="fastfooddatadb"
)
cursor = db.cursor()

# Function to fetch data from the fast_food_restaurants table
def fetch_data(zip_code, user_location):
    try:
        # Modify the query to select data from fast_food_restaurants
        query = """
            SELECT name, address, city, latitude, longitude, zip_code, state
            FROM fast_food_restaurants
            WHERE zip_code = %s
        """
        cursor.execute(query, (zip_code,))
        results = cursor.fetchall()

        # Calculate distances and add them to the results
        data = []
        for row in results:
            restaurant = {
                'name': row[0],
                'address': row[1],
                'city': row[2],
                'latitude': row[3],
                'longitude': row[4],
                'zip_code': row[5],
                'state': row[6],
                'distance': calculate_distance(user_location, (row[3], row[4]))  # Implement this function
            }
            data.append(restaurant)

        return data
    except Exception as e:
        print("Database Error:", e)
        return []

# Placeholder function for calculating distance
def calculate_distance(user_location, restaurant_location):
    # Implement your distance calculation logic here
    # You can use libraries like geopy for this purpose
    return 0.0

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        zip_code = request.form["zip_code"]
        if zip_code:
            user_location = (0.0, 0.0)  # Replace with user's location (latitude, longitude)
            # Fetch data based on the zip code and user location
            data = fetch_data(zip_code, user_location)
            return render_template("output.html", data=data)  # Render the output template
    # Render the homepage.html template for GET requests
    return render_template("homepage.html")

if __name__ == "__main__":
    app.run(debug=True)
