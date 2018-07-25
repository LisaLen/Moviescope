ratings = open('ratings.csv')
links = open('links.csv')
f = open('my_dataset.csv', 'w+')

ratings_dict={}
links_dict={}

for line in links:
        words= line.split(',')
        ratings_dict[words[0]] = words[1]

for line in ratings:
    words= line.split(',')
    my_str= ''.join(words[0]) + ',' + ''.join(ratings_dict[words[1]]) + ',' + ''.join(words[2])
    f.write(my_str + '\n')

f.close()
ratings.close()
links.close()



