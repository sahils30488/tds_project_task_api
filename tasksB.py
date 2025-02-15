import os
import sqlite3
import subprocess

import duckdb
import markdown
import pandas as pd
import requests
import whisper
from flask import Flask, jsonify, request
from PIL import Image


def B12(filepath):
    """Security check: Allow access only to files inside /data directory."""
    if not filepath.startswith("/data"):
        raise PermissionError(f"Access denied: {filepath} (outside /data)")
    return True


def B3(url, save_path):
    """Fetch data from an API and save it to a file."""
    B12(save_path)
    response = requests.get(url)
    with open(save_path, "w") as file:
        file.write(response.text)


def B4(repo_url, commit_message):
    """Clone a Git repository and make a commit."""
    repo_path = "/data/repo"
    if os.path.exists(repo_path):
        subprocess.run(["rm", "-rf", repo_path], check=True)
    subprocess.run(["git", "clone", repo_url, repo_path], check=True)
    subprocess.run(["git", "-C", repo_path, "commit", "-m", commit_message], check=True)


def B5(db_path, query, output_filename):
    """Execute an SQL query on SQLite or DuckDB and save the result."""
    B12(db_path)
    conn = (
        sqlite3.connect(db_path) if db_path.endswith(".db") else duckdb.connect(db_path)
    )
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    conn.close()
    with open(output_filename, "w") as file:
        file.write(str(result))
    return result


def B6(url, output_filename):
    """Scrape a webpage and save its HTML content."""
    B12(output_filename)
    result = requests.get(url).text
    with open(output_filename, "w") as file:
        file.write(str(result))


def B7(image_path, output_path, resize=None):
    """Process an image (resize) and save it."""
    B12(image_path)
    B12(output_path)
    img = Image.open(image_path)
    if resize:
        img = img.resize(resize)
    img.save(output_path)


def B8(audio_path):
    """Transcribe an audio file using Whisper AI."""
    B12(audio_path)
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["text"]


def B9(md_path, output_path):
    """Convert a Markdown file to HTML."""
    B12(md_path)
    B12(output_path)
    with open(md_path, "r") as file:
        html = markdown.markdown(file.read())
    with open(output_path, "w") as file:
        file.write(html)


app = Flask(__name__)


@app.route("/filter_csv", methods=["POST"])
def filter_csv():
    """Filter rows in a CSV file based on a column value."""
    data = request.json
    csv_path = data["csv_path"]
    B12(csv_path)
    df = pd.read_csv(csv_path)
    filter_column, filter_value = data["filter_column"], data["filter_value"]
    filtered = df[df[filter_column] == filter_value]
    return jsonify(filtered.to_dict(orient="records"))
