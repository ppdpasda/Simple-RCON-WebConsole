from flask import Flask, render_template, request
from mcrcon import MCRcon
import argparse

app = Flask(__name__)

def send_rcon_command(command):
    try:
        with MCRcon(args.host, args.password, port=args.port) as mcr:
            response = mcr.command(command)
    except ConnectionRefusedError:
        print("ConnectionRefusedError")
    except Exception as e:
        print("Unhandled exception: ", str(e))
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_command', methods=['POST'])
def send_command():
    try:

        command = request.form.get('command')

        if not command:
            return render_template('index.html', error='Command is required')

        response = send_rcon_command(command)

        return render_template('index.html', response=response)
    except Exception as e:
        return render_template('500.html', error=str(e))

def args_parser():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--host', default='localhost', type=str, help='Your host which you specified in server.properties')
    parser.add_argument('--port', default=25575, type=int, help='Your rcon port which you specified in server.properties')
    parser.add_argument('--password', default="12345", type=str, help='Your rcon password which you specified in server.properties')
    return parser.parse_args()

args = args_parser()

if __name__ == '__main__':
    app.run(debug=False)
