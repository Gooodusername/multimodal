from flask import Flask, render_template, request
import socket

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    response = send_message(user_input)
    return render_template('index.html', user_input=user_input, response=response)

def send_message(message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 8888)

    try:
        client_socket.connect(server_address)
        client_socket.send(message.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        return response

    finally:
        client_socket.close()

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port='5000')
