#!/usr/bin/env python3

# https://docs.faculty.ai/user-guide/apps/examples/dash_file_upload_download.html
# https://www.roytuts.com/python-flask-rest-api-file-upload/

import base64
import os
import requests
from urllib.parse import quote as urlquote

from flask import Flask, send_from_directory, send_file, request
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

UPLOAD_DIRECTORY = "./data/"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

IMAGES_DIRECTORY = UPLOAD_DIRECTORY + 'images'
if not os.path.exists(IMAGES_DIRECTORY):
    os.makedirs(IMAGES_DIRECTORY)

IMAGES_ENDPOINT = "/images/"

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    './center.css'
]

# Normally, Dash creates its own Flask server internally. By creating our own,
# we can create a route for downloading files directly:
server = Flask(__name__)  # use mienheld instead
app = dash.Dash(server=server, external_stylesheets=external_stylesheets)

colors = {
    "graphBackground": "#F5F5F5",
    "background": "#ffffff",
    "text": "#000000"
}

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.H2("Files"),
    html.Ul(id="file-list"),
    html.H2("This graph could be a histogram of cats/dogs, if I knew Dash."),
    dcc.Graph(
        id='cats-dogs',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    ),
    html.Div(id='output-data-upload')
], style={'max-width': '1000px', 'margin': '0 auto'})


@server.route(f"{IMAGES_ENDPOINT}<path:filename>")
def download(filename):
    """Serve a file from the upload directory to user."""
    return send_file(f"{IMAGES_DIRECTORY}/{filename}")


def save_file(name, content):
    """Decode and store a file uploaded by user to app with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(IMAGES_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))


def list_uploaded_files():
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(IMAGES_DIRECTORY):
        path = os.path.join(IMAGES_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files


def file_download_link(filename, label):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "{}{}".format(IMAGES_ENDPOINT, filename)
    print(f"location = {location}")
    return html.A(label + ' - ' + filename, href=location, target="_blank")


@app.callback(
    Output("file-list", "children"),
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
)
def update_output(uploaded_filenames, uploaded_file_contents):
    """Save uploaded files, send files for classification, and regenerate the file list."""
    if uploaded_filenames is not None and uploaded_file_contents is not None:
        files = zip(uploaded_filenames, uploaded_file_contents)
    else:
        files = []

    messages = [
        {"filename": name, "image": str(data)}
        for name, data in files
    ]

    for m in messages:
        save_file(m['filename'], m['image'])

    api_calls = [
        requests.post(url="http://mlapi:8000/guess", json=m)
        for m in messages
    ]

    with open('./errors', 'w') as f:
        for c in api_calls:
            if c.status_code == 200:
                f.write(str(c) + '\n')

    labels = [
        call.json() if call.status_code == 200 else None
        for call in api_calls
    ]

    labels = list(filter(None, labels))

    if len(labels) == 0:
        return [html.Li("No files yet!")]
    else:
        return [
            html.Li(file_download_link(label['filename'], label['label']))
            for label in labels
        ]


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8888)
