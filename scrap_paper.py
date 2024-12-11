import json

with open('populated_shows_since_2022.json') as f:
    shows = json.load(f)
    print(len(shows))

with open('articles.json') as f:
    articles = json.load(f)
    print(len(articles))

print(1169 + 1279)

# 2448 vectors
# each 67537 hot

print(2447 * 67537)

''' 
weighing happens on two fronts:
+ compute inverse scores for rarer terms
    e.g more significant to search Car Seat Headrest than Album

+ depending on where in the object the string stored, give more weight
    e.g "The Jazz Hour" should have a higher jazz:weight than
    a show that has a song off an album called The Best Jazz of the 40s    
'''