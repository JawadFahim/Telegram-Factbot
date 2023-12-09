from flask import Flask, render_template
from threading import Thread
import os

app = Flask(__name__)

@app.route('/')
def index():
		# Get the Replit project URL
		replit_url = f'https://{os.environ["REPL_SLUG"]}.{os.environ["REPL_OWNER"]}.replit.co'
		return f"Alive! Replit Project URL: {replit_url}"

def run():
		app.run(host='0.0.0.0', port=8080)

def keep_alive():
		t = Thread(target=run)
		t.start()

# Start the Flask app with keep_alive()
keep_alive()

