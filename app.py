from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the CSV data
df = pd.read_csv('students_depression_clean.csv')

# Map depression numeric to text labels
def depression_text(val):
    return "Moderate/High" if val == 1 else "No/Low"

df['DEPRESSION_STATUS'] = df['Depression'].apply(depression_text)

# Medicines and recommendations
medicines = [
    "Fluoxetine (Prozac)",
    "Sertraline (Zoloft)",
    "Citalopram (Celexa)",
    "Duloxetine (Cymbalta)",
    "Bupropion (Wellbutrin XL)"
]

recommendations = [
    "Engage in moderate exercise regularly.",
    "Get enough sleep each night.",
    "Eat a well-balanced diet.",
    "Talk to supportive friends or family.",
    "Practice relaxation and mindfulness.",
    "Seek help from a counselor or healthcare provider if symptoms persist."
]

@app.route('/', methods=['GET', 'POST'])
def index():
    students = []
    search_name = None
    if request.method == 'POST':
        search_name = request.form['name'].strip().lower()
        # Filter students by name case-insensitive match
        students = df[df['names'].str.lower().str.contains(search_name)].to_dict(orient='records')
    return render_template('index.html',
                           students=students,
                           search_name=search_name,
                           medicines=medicines,
                           recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
