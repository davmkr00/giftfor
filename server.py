from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
import time

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
    try:
        cursor = mysql.connection.cursor()
        analytics_query = f'INSERT INTO giftfor_analytics (address, agent, unix_time) VALUES (%s, %s, %s);'
        analytics_values = (request.remote_addr, request.headers.get('User-Agent'), int(time.time()))
        cursor.execute(analytics_query, analytics_values)
        cursor = mysql.connection.commit()
    except Exception as e:
        print('index:', e)
    return app.send_static_file('first.html')

@app.route('/him')
@app.route('/her')
def products_page():
    try:
        cursor = mysql.connection.cursor()
        analytics_query = f'INSERT INTO giftfor_analytics (address, session_id, agent, unix_time) VALUES (%s, %s, %s, %s);'
        analytics_values = (request.remote_addr, request.path, request.headers.get('User-Agent'), int(time.time()))
        cursor.execute(analytics_query, analytics_values)
        cursor = mysql.connection.commit()
    except Exception as e:
        print('products_page:', e)
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
        cursor.execute(query)
        data = cursor.fetchall()
        return jsonify(data)
    except Exception as e:
        print('send_product:', e)
        return jsonify('')

@app.route('/feedback', methods=['POST'])
def feedback():
    try:
        json_body = request.get_json(force=True)
        # "giftfor": "him/her"
        # "action": "liked/dislike"
        # "id": product id
        # "sid": session id
        # "sw": swiped true/false
        cursor = mysql.connection.cursor()
        cursor.execute(f'UPDATE giftfor_{json_body["giftfor"]} SET giftfor_{json_body["giftfor"]}.{json_body["action"]} = giftfor_{json_body["giftfor"]}.{json_body["action"]} + 1 WHERE id={json_body["id"]};')
        
        analytics_query = f'INSERT INTO giftfor_analytics (address, session_id, agent, swiped, product_id, unix_time) VALUES (%s, %s, %s, %s, %s, %s);'
        analytics_values = (request.remote_addr, json_body['sid'], request.headers.get('User-Agent'), json_body['sw'], json_body['id'], int(time.time()))
        cursor.execute(analytics_query, analytics_values)
        
        cursor = mysql.connection.commit()
        return jsonify(json_body["id"])
    except Exception as e:
        print('feedback:', e)
        return jsonify('-1')


if __name__ == '__main__':
    app.run(host="localhost", port=4000, debug=True)