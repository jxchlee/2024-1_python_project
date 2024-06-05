from flask import Flask, request, jsonify, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import base64
import os

# 애플리케이션 인스턴스 생성
app = Flask(__name__)

# MySQL 설정
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'ctf'
app.config['MYSQL_PASSWORD'] = 'asdf'
app.config['MYSQL_DB'] = 'CTK'
mysql = MySQL(app)

@app.route('/loginCheck', methods=['POST'])
def login_check():
    try:
        if request.method == 'POST':
            with app.app_context():
                email = request.form['email']
                password = request.form['password']

                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                query = 'SELECT * FROM CTK_USER WHERE email = %s AND password = %s'
                cursor.execute(query, (email, password))

                result = cursor.fetchone()
                if  result:
                    user_class = result['class']
                    return jsonify({'class': user_class})
                else:
                    flash('Invalid email or password')
                    result = -1
                    return jsonify({'class': result})

        else:
            flash('Error!')
            result = -1
            return jsonify({'class': result})

    except Exception as e:
        # 에러가 발생한 경우 False 반환
        return jsonify(success=False, error=str(e))

if __name__ == '__main__':
    app.run(host='192.168.219.170', port=8000)