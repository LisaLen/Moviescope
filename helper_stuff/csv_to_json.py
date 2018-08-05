import csv
import json


csvfile = open('movie_user_ratings.csv', 'r')
jsonfile = open('movie_user_ratings.json', 'w+')

fieldnames = ("userid","imdbid","rating")
reader = csv.DictReader(csvfile, fieldnames)
for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write(',\n')
csvfile.close()
jsonfile.close()