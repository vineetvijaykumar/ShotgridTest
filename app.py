from flask import Flask, render_template
from query_utils import get_sequence_query_results
from pprint import pprint

app = Flask(__name__)


@app.route("/")
def index():
    project_id = 85
    sequence_data = get_sequence_query_results(project_id)
    pprint(sequence_data)
    return render_template("sequences.html", sequences=sequence_data)


if __name__ == "__main__":
    app.run(debug=True)
