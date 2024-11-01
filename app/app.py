from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

def load_data():
    df = pd.read_csv('player_statistics_cleaned_final.csv')
    # Clean column names to match JavaScript expectations
    df.columns = [col.replace(' ', '') for col in df.columns]
    df.columns = [col.replace('@', '') for col in df.columns]
    df.columns = [col.replace('%', '') for col in df.columns]
    
    return df

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/players')
def get_players():
    df = load_data()
    search = request.args.get('search', '').lower()
    team_filter = request.args.get('team', '')
    
    if search:
        df = df[df['PlayerName'].str.lower().str.contains(search) | 
                df['TeamName'].str.lower().str.contains(search)]
    if team_filter:
        df = df[df['TeamName'] == team_filter]
    
    return jsonify(df.to_dict('records'))

@app.route('/api/teams')
def get_teams():
    df = load_data()
    teams = df['TeamName'].unique().tolist()
    return jsonify(teams)

if __name__ == '__main__':
    app.run(debug=True)