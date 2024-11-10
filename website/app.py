from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS  # Import CORS

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Configure MySQL
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Root12345'
app.config['MYSQL_HOST'] = 'localhost'  # MySQL host (localhost by default)
app.config['MYSQL_DB'] = 'hims'  # Database name

# Initialize MySQL
mysql = MySQL(app)

# Route to fetch data
@app.route('/users')
def get_users():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()

    # Convert the result to a list of dictionaries for JSON serialization
    user_list = [{"UserID": row[0], "Username": row[1], "Password": row[2], "Role": row[3], "DepartmentID": row[4]} for row in users]
    return jsonify(user_list)

@app.route('/inventory', methods=['GET'])
def get_inventory():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM inventoryitems")
        items = cursor.fetchall()
        cursor.close()

        # Format the result into a JSON-compatible format
        inventory_data = []
        for item in items:
            inventory_data.append({
                'item_id': item[0],
                'name': item[1],
                'quantity': item[2],
                'reorder_level': item[3],
                'department_id': item[4]
            })

        # Return the data as a JSON response
        return jsonify(inventory_data)
    except Exception as e:
        # Return error message if an exception occurs
        return str(e), 500

@app.route('/suppliers', methods=['GET'])
def get_supplier():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM suppliers")
        suppliers = cursor.fetchall()
        cursor.close()

        # Format the result into a JSON-compatible format
        supplier_data = []
        for supplier in suppliers:
            supplier_data.append({
                'supplier_id': supplier[0],
                'supplier_name': supplier[1],
                'contactperson': supplier[2],
                'contactnumber': supplier[3],
                'address': supplier[4]
            })

        # Return the data as a JSON response
        return jsonify(supplier_data)
    except Exception as e:
        # Return error message if an exception occurs
        return str(e), 500
    
@app.route('/departments', methods=['GET'])
def get_department():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM departments")
        departments = cursor.fetchall()
        cursor.close()

        # Format the result into a JSON-compatible format
        departments_data = []
        for department in departments:
            departments_data.append({
                'DepartmentID': department[0],
                'DepartmentName': department[1],
                'DepartmentHead': department[2],
                'ContactNumber': department[3],
                
            })

        # Return the data as a JSON response
        return jsonify(departments_data)
    except Exception as e:
        # Return error message if an exception occurs
        return str(e), 500

@app.route('/add_order_item', methods=['POST'])
def add_order_item():
    # Get data from the request
    data = request.get_json()
    orderID = data['orderID']
    itemID = data['itemID']
    quantity = data['quantity']
    unitPrice = data['unitPrice']
    totalPrice = data['totalPrice']

    # Create a cursor and execute the insert query
    cursor = mysql.connection.cursor()
    query = '''INSERT INTO orderitems (OrderID, ItemID, Quantity, UnitPrice, TotalPrice) 
               VALUES (%s, %s, %s, %s, %s)'''
    cursor.execute(query, (orderID, itemID, quantity, unitPrice, totalPrice))
    mysql.connection.commit()
    cursor.close()

    # Return a JSON response indicating success
    return jsonify({"success": True})

@app.route('/get-orders', methods=['GET'])
def get_orders():
    # Create a cursor object to interact with the database
    cursor = mysql.connection.cursor()
    
    # Query to fetch orders from the 'orders' table
    cursor.execute('SELECT OrderID, OrderDate, SupplierID, DepartmentID, TotalAmount FROM orders')
    
    # Fetch all the rows from the result of the query
    orders = cursor.fetchall()

    # Prepare the list of orders as JSON response
    order_list = []
    for order in orders:
        order_data = {
            'OrderID': order[0],
            'OrderDate': order[1],
            'SupplierID': order[2],
            'DepartmentID': order[3],
            'TotalAmount': order[4]
        }
        order_list.append(order_data)

    # Close the cursor and return the JSON response
    cursor.close()
    return jsonify(order_list)


if __name__ == '__main__':
    app.run(debug=True)
