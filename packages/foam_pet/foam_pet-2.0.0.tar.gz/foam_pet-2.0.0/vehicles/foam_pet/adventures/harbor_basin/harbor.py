


from flask import Flask

def open_harbor ():
	app = Flask(__name__)

	@app.route('/')
	def home ():
		return "Hello, World!"

	app.run(host='0.0.0.0', port=5000)