# GUI SERVER
# FLASK integration: https://github.com/shiffman/NOC-S17-2-Intelligence-Learning

# import everything we need
from flask import Flask, jsonify, request
import TAMA_main as tama

# Setup Flask app.
app = Flask(__name__)
# Extra debugging
app.debug = True

# Routes
# This is root path, use index.html in "static" folder
@app.route('/')
def root():
  return app.send_static_file('index.html')

# This is a nice way to just serve everything in the "static" folder
@app.route('/<path:path>')
def static_proxy(path):
  # send_static_file will guess the correct MIME type
  return app.send_static_file(path)

## Here is a new route to receive data from p5
@app.route('/upload', methods=['POST'])
def upload():
    # Get the "alg" value sent from p5, parsed as json
    alg = request.get_json()['alg']
    alg = str(alg) # lose the unicode
    # If nothing was sent
    if alg is None:
        return jsonify(status='no name');
    ## otherwise
    else:
        # Run TAMA with requested algorithm
        print("alg recived" , alg)
        # tama.makeMyTama(alg) # TODO run :)
        # Using "jsonify" makes it easy to read the data back in p5
        return jsonify(status='ran alg')

# Run app:
if __name__ == '__main__':
    # Localhost and port 8080
    app.run( host='0.0.0.0', port=8080, debug=True )
    # If you enable debugging, you'll get more info
    # server will restart automatically when code changes, etc.
    # app.run( host='0.0.0.0', port=8080, debug=True )
