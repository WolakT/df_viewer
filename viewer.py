from flask import Flask, render_template, request
import pandas as pd

class QuickIterator(object):
    def __init__(self):
        self.it = 0
    def next(self):
        out = self.it
        self.it += 1
        return out

QIT = QuickIterator()
app = Flask(__name__)
df = pd.read_pickle("data/data-frame.pickle")


@app.route('/', methods=['GET', 'POST'])
def index():
    it = QIT.next()
    name = None
    if request.method == 'POST':
        if 'Correct' in request.form.values():
            df.ix[it, 'validation'] = True
        else:
            df.ix[it, 'validation'] = False
        #it += 1
        next_row = get_row_as_dict(it)
    elif request.method == 'GET':
        next_row = get_row_as_dict(it)
    return render_template('index.html', name=name, desc_text=next_row['DESC_TEXT'], row_no=it, type=next_row['type'])


def get_row_as_dict(row_id):
    return df.ix[row_id].to_dict()


if __name__ == '__main__':
    app.run(debug=True)
