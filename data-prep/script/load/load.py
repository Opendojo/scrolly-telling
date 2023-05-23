import duckdb
import os
import glob

# Data Source: https://www.kaggle.com/datasets/davidcariboo/player-scores?resource=download

con = duckdb.connect(database='../../data/foot-data-Transfermarkt.duckdb', read_only=False)
for file in list(glob.glob('../../data/archive/*.csv')):
    (head, tail) = os.path.split(file)
    (filename, extension) = os.path.splitext(tail)
    con.execute("CREATE TABLE {} AS SELECT * FROM read_csv_auto('{}');".format(filename, file))
    print("Created: {}".format(filename))
