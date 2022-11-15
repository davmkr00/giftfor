from flask import Flask, jsonify, request
from flask_mysqldb import MySQL


app = Flask(__name__,
            static_url_path='', 
            static_folder='static')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'giftfor'
 
mysql = MySQL(app)


@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/product', methods=['POST'])
def send_product():
    json_body = request.get_json(force=True)
    # "giftfor": "him/her"
    # "count": product number to send
    # "price": under price number
    # "received": random ids that already sent to client
    already_selected_ids = ','.join(map(str,json_body['received']))
    cursor = mysql.connection.cursor()
    cursor.execute(f'SELECT id, title, price, image, url from giftfor_{json_body["giftfor"]} WHERE price < {json_body["price"]} AND id NOT IN({already_selected_ids}) ORDER BY RAND() LIMIT {json_body["count"]};')
    data = cursor.fetchall()
    return jsonify(data)

@app.route('/feedback', methods=['POST'])
def update_likes():
    json_body = request.get_json(force=True)
    # "giftfor": "him/her"
    # "action": "liked/dislike"
    # "id": product id
    cursor = mysql.connection.cursor()
    cursor.execute(f'UPDATE giftfor_{json_body["giftfor"]} SET giftfor_{json_body["giftfor"]}.{json_body["action"]} = giftfor_{json_body["giftfor"]}.{json_body["action"]} + 1 WHERE id={json_body["id"]};')
    cursor = mysql.connection.commit()
    return jsonify(json_body["id"])

if __name__ == '__main__':
    app.run(host="localhost", port=4000, debug=True)