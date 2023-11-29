from flask import Flask, render_template
app = Flask(__name__)
def get_data():
    data = ["Item1", "Item2", "Item3"]
    return data 
@app.route('/')
def index():
    data = get_data()
    return render_template('index.html', data=data)
if __name__ == '__main__':
    app.run(debug=True)
