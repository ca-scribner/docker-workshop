#!/usr/bin/env python3

# https://docs.faculty.ai/user-guide/apps/examples/dash_file_upload_download.html
# https://www.roytuts.com/python-flask-rest-api-file-upload/

import base64
import os
import requests
from urllib.parse import quote as urlquote
from flask import Flask, send_from_directory, request
#from flask_caching import Cache
import dash
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

UPLOAD_DIRECTORY = "/data/"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

IMAGES_DIRECTORY = UPLOAD_DIRECTORY+'images'
if not os.path.exists(IMAGES_DIRECTORY):
    os.makedirs(IMAGES_DIRECTORY)
    
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    './center.css'
]

# Normally, Dash creates its own Flask server internally. By creating our own,
# we can create a route for downloading files directly:
server = Flask(__name__, static_folder='/data/images') # use mienheld instead
app = dash.Dash(server=server, external_stylesheets=external_stylesheets)


colors = {
    "graphBackground": "#F5F5F5",
    "background": "#ffffff",
    "text": "#000000"
}


app.layout = html.Div([
    html.H1("ULTRA ADVANCED CAT V.S. DOG IDENTIFIER."),
    html.H2("Patent Pending."),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop images of cats or dogs, or ',
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
    dcc.Store(id='files-db', storage_type='session'),
    html.Ul(id="file-list"),
    dcc.Graph(id='cats-dogs'),
    html.Div(id='output-data-upload')
], style={'max-width': '1000px', 'margin' : '0 auto'})


@server.route("/data/images/<path:filename>")
def download(filename):
    """Serve a file from the upload directory."""
    return send_from_directory(directory='/data/images', filename=filename)
    #return send_from_directory(directory='/data/images', filename=filename, as_attachment=True)

def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(IMAGES_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))

def uploaded_files():
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(IMAGES_DIRECTORY):
        path = os.path.join(IMAGES_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files


def file_download_link(filename, label):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "{}/{}".format(IMAGES_DIRECTORY, urlquote(filename))
    return html.A(label + ' - ' + filename, href=location, target="_blank")


@app.callback(
    Output("files-db", "data"),
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
    [State('files-db', 'data')]
)
def update_db_disk(uploaded_filenames, uploaded_file_contents, data):
    """Save uploaded files and regenerate the file list."""

    if data is None:
        data = {}
    
    if not uploaded_filenames is None and not uploaded_file_contents is None:
        files = zip(uploaded_filenames, uploaded_file_contents)
    else:
        files = []
        
    messages = [
        {"filename" : name, "image" : str(data) }
        for name, data in files
    ]

    for m in messages:
        save_file(m['filename'], m['image'])

    api_calls = [
        requests.post(url="http://mlapi:8000/guess", json=m)
        for m in messages
    ]

    with open('/errors', 'w') as f:
        for c in api_calls:
            if c.status_code == 200:
                f.write(str(c) + '\n')

    labels = [
        call.json() if call.status_code == 200 else None
        for call in api_calls
    ]

    
    labels = list(filter(None, labels))

    for d in labels:
        data[d['filename']] = d['label']
    
    return data


@app.callback(
    Output("file-list", "children"),
    [Input("files-db", "data")],
)
def update_list(labels):
    """ File list. """

    if labels is None or len(labels) == 0:
        return [html.Li("No files yet!")]
    else:
        return [
            html.Li( file_download_link(f, labels[f]) )
            for f in labels
        ]


@app.callback(
    Output("cats-dogs", "figure"),
    [Input("files-db", "data")],
)
def update_graph(labels):
    """ Histogram of current files """
    if labels is None:
        labels = {}
    

    hist = go.Histogram(
        x = list(labels.values()),
        marker = {'colorscale': 'Viridis'},
        name = 'Cats v.s. Dogs'
    )

    return {
        'data': [hist],
        'layout': go.Layout(title='Cats v.s. Dogs'),
    }

 
    

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8888)
