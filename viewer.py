from flask import Flask, render_template, request
import pandas as pd
import os.path
import csv
import argparse

class QuickIterator(object):
    def __init__(self):
        self.it = 0
    def next(self):
        self.it += 1
        return self.it 
    def previous(self):
        self.it -= 1
        return self.it
    
QIT = QuickIterator()
app = Flask(__name__)
df = None
csv_file_path = 'data/results.csv'  

@app.route('/', methods=['GET', 'POST'])
def index():
    it = get_rows_count() 
    if request.method == 'POST':
        if 'Correct' in request.form.values():
            df.ix[it, 'validation'] = True
        elif'Incorrect':
            df.ix[it, 'validation'] = False
        #it += 1
        write_csv(it)
        #QIT.next()
        row_no = it+1
        next_row = get_row_as_dict(row_no)
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
        df.loc[:row_no].to_csv(csv_file_path,sep=';',index=False)


def get_row_as_dict(row_id):
    return df.ix[row_id].to_dict()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("df_path", help="provide the path to the pickle file")
    args = parser.parse_args()
    df_file_path = args.df_path
    df = pd.read_pickle(df_file_path)
    app.run(debug=True)
