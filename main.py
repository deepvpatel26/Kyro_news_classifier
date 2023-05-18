from flask import Flask, render_template, request
from flask import redirect, url_for
import datetime
import sqlite3
from scrap import *
from model import *

app = Flask(__name__)

import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('predictions.db')
cursor = conn.cursor()

# Create the table for storing predictions
cursor.execute('''
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        submission_time TIMESTAMP,
        url TEXT,
        category TEXT
    )
''')

def get_submission_history():
    conn = sqlite3.connect('predictions.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM predictions')
    submission_history = cursor.fetchall()
    conn.close()
    return submission_history

def delete_submission(submission_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM submissions WHERE rowid=?', (submission_id,))
    conn.commit()
    conn.close()

# Commit the changes and close the connection
conn.commit()
conn.close()



@app.route('/', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        url = request.form['url']
        if 'indianexpress.com' not in url:
            error_message = 'Please enter a valid article URL from Indian Express.'
            return render_template('index.html', error_message=error_message)

        new_text = scrape_article(url)
        if new_text:
            predicted_category = predict_category(new_text)
            submission_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            submission_data = (submission_time, url, predicted_category)
            add_submission_to_history(submission_data)
            return render_template('result.html', url=url, category=predicted_category)
        else:
            error_message = 'Failed to scrape the article. Please try again with a different URL.'
            return render_template('index.html', error_message=error_message)

    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    url = request.form['url']
    new_text = scrape_article(url)
    category = predict_category(new_text)
    submission_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect('predictions.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO predictions (submission_time, url, category) VALUES (?, ?, ?)',
                   (submission_time, url, category))
    conn.commit()
    conn.close()

    return redirect(url_for('history'))

@app.route('/history', methods=['GET', 'POST'])
def history():
    if request.method == 'POST':
        submission_id = request.form['submission_id']
        delete_submission(submission_id)

    submission_history = get_submission_history()
    return render_template('history.html', submission_history=submission_history)


if __name__ == '__main__':
    app.run(debug=True)

