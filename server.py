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
    return app.send_static_file('first.html')

@app.route('/him')
@app.route('/her')
def products_page():
    return app.send_static_file('index.html')

@app.route('/product', methods=['POST'])
def send_product():
    try:
        json_body = request.get_json(force=True)
        # "giftfor": "him/her"
        # "count": product number to send
        # "price": under price number
        # "received": products ids that already sent to client
        received = ''
        if json_body['received']:
            already_selected_ids = ','.join(map(str,json_body['received']))
            received = f'AND id NOT IN({already_selected_ids})'

        # if no max price use 1000 usd
        max_price = json_body.get("price", "1000")

        cursor = mysql.connection.cursor()
        query = f'SELECT id, title, price, image, url from giftfor_{json_body["giftfor"]} WHERE price < {max_price} {received} ORDER BY RAND() LIMIT {json_body["count"]};'
        print(query)
        cursor.execute(query)
        data = cursor.fetchall()
        return jsonify(data)
    except:
        return jsonify('')

@app.route('/feedback', methods=['POST'])
def update_likes():
    try:
        json_body = request.get_json(force=True)
        # "giftfor": "him/her"
        # "action": "liked/dislike"
        # "id": product id
        cursor = mysql.connection.cursor()
        cursor.execute(f'UPDATE giftfor_{json_body["giftfor"]} SET giftfor_{json_body["giftfor"]}.{json_body["action"]} = giftfor_{json_body["giftfor"]}.{json_body["action"]} + 1 WHERE id={json_body["id"]};')
        cursor = mysql.connection.commit()
        return jsonify(json_body["id"])
    except:
        return jsonify('-1')


if __name__ == '__main__':
    app.run(host="localhost", port=4000, debug=True)