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
pickle_file_path = 'data/results.pickle'
file_name = None

@app.route('/', methods=['GET', 'POST'])
def index():
    it = QIT.it 
    if request.method == 'POST':
        if 'Correct' in request.form.values():
            df.ix[it, 'validation'] = True
            it = QIT.next()   
        elif'Incorrect' in request.form.values():
            df.ix[it, 'validation'] = False
            it = QIT.next()
        elif'Previous' in request.form.values():
            it = QIT.previous()
        elif'Next'in request.form.values():
            it = QIT.next()
        elif'Write to csv'in request.form.values():
            write_csv()

        #it += 1
#        write_csv(it)
        #QIT.next()
        row_no = it
        next_row = get_row_as_dict(row_no)
    elif request.method == 'GET':
        
        next_row = get_row_as_dict(it)
        row_no = it
    first = it > 0
    return render_template('index.html', desc_text=next_row['DESC_TEXT'], row_no=row_no, type=next_row['type'], first=first, file_name=file_name)

def get_rows_count():
    if os.path.exists(csv_file_path):
        temp_df = pd.read_csv(csv_file_path)
        return len(temp_df)
    else:
        return 0
def write_csv():
    if os.path.exists(csv_file_path):
        os.remove(csv_file_path)

    df.to_csv(csv_file_path,sep=';',index=False)
    df.to_pickle(pickle_file_path)


def get_row_as_dict(row_id):
    return df.ix[row_id].to_dict()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("df_path", help="provide the path to the pickle file")
    args = parser.parse_args()
    df_file_path = args.df_path
    df = pd.read_pickle(df_file_path)
    file_name = os.path.splitext(df_file_path)[0]
    if os.path.exists(pickle_file_path):
        os.remove(pickle_file_path)
    if os.path.exists(csv_file_path):
        os.remove(csv_file_path)
    if not 'validation' in df:
        df['validation'] = 'NaN'
    app.run(debug=True)

