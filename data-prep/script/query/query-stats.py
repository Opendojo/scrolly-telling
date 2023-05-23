import duckdb
import pandas

con = duckdb.connect(database='../../data/foot-data-Transfermarkt.duckdb', read_only=True)

df_season_overview = con.execute("SELECT season, home, SUM(yellow_cards), SUM(red_cards), SUM(goals), SUM(assists) \
            FROM  player_actions_cards\
            GROUP BY season, home \
            ORDER BY season ASC, home ASC").fetchdf()

print(df_season_overview)
