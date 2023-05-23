import duckdb
import pandas

con = duckdb.connect(database='../../data/foot-data-Transfermarkt.duckdb', read_only=False)
con.execute("DESCRIBE;")
for table in con.fetchall():
  for table_name in table:
    print("Element: {}".format(table_name))

df_competitions = con.execute("SELECT * FROM competitions;").fetchdf()
print(df_competitions)

belgian_competition = df_competitions.loc[df_competitions['competition_id'] == 'BE1']

print(belgian_competition)

belgian_competition_id = belgian_competition.iat[0,0]
belgian_competition_name = belgian_competition.iat[0,2]

print("We are looking for Belgian competition with ID: {} and Name: {}".format(belgian_competition_id,belgian_competition_name))

# get the list of Belgian Club games
df_belgian_club_games = con.execute("SELECT home_club_id, season, COUNT(*) cnt FROM games WHERE competition_id = '{}' GROUP BY home_club_id, season ORDER BY season ASC, cnt DESC".format(belgian_competition_id)).fetchdf()

print(df_belgian_club_games)
# get the list of red and yellow card by season in belgium pro league

df_belgian_cards = con.execute("SELECT season, player_id, player_name, yellow_cards, red_cards, goals, assists, minutes_played, home_club_id, club_home_name, away_club_id, club_away_name, player_club_id \
                               FROM appearances, games \
                               WHERE games.game_id=appearances.game_id \
                               AND games.competition_id = '{}'".format(belgian_competition_id)).fetchdf()

df_belgian_cards['home']=df_belgian_cards.apply(lambda x: True if x['home_club_id']==x['player_club_id'] else False, axis=1)

print(df_belgian_cards)

con.execute("CREATE TABLE player_actions_cards AS SELECT * FROM df_belgian_cards")
