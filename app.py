from flask import Flask, render_template
app = Flask(__name__)   
posts = [
    {
        'title': 'Book 1',
        'Writer': 'Author 1',
        'Content': 'Content1'
    },
    {
        'title': 'Book 2',
        'Writer': 'Author 2',
        'Content': 'Content 2'
    }
]
@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', posts=posts)
if __name__ == '__main__':
    app.run(debug=True)
