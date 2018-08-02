from flask import Flask, render_template, request
import pandas as pd
import os.path
import csv

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
csv_file_path = 'data/result.csv'
 

@app.route('/', methods=['GET', 'POST'])
def index():
    it = get_rows_count() 
    if request.method == 'POST':
        if 'Correct' in request.form.values():
            df.ix[it, 'validation'] = True
        else:
            df.ix[it, 'validation'] = False
        #it += 1
        write_csv(it)
        QIT.next()
        next_row = get_row_as_dict(it+1)
        row_no = it +1
    elif request.method == 'GET':
        next_row = get_row_as_dict(it)
        row_no = it
    return render_template('index.html', desc_text=next_row['DESC_TEXT'], row_no=row_no, type=next_row['type'])

def get_rows_count():
    if os.path.exists(csv_file_path):
        temp_df = pd.read_csv(csv_file_path)
        return len(temp_df)
    else:
        return 0
def write_csv(row_no):
    if os.path.exists(csv_file_path):
        with open(csv_file_path,'a',newline=''   ) as csv_file:
            field_names = df.columns.tolist()
            new_row_dict = df.loc[row_no].to_dict()
            writer = csv.DictWriter(csv_file, field_names,delimiter=';')
            writer.writerow(new_row_dict)
    else:
        df.loc[:QIT.it].to_csv(csv_file_path,sep=';',index=False)


def get_row_as_dict(row_id):
    return df.ix[row_id].to_dict()


if __name__ == '__main__':
    app.run(debug=True)
