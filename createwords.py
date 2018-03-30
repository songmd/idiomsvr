import sqlite3
import random

def sqlite3_to_words():
    sqlite3_conn = sqlite3.connect('idiom.db')
    sqlite3_cursor = sqlite3_conn.cursor()
    sqlite3_cursor.execute('SELECT chengyu FROM idiom')

    words = dict()
    for chengyu, in sqlite3_cursor:
        if len(chengyu) != 4:
            continue
        for w in chengyu:
            if w in words:
                words[w] += 1
            else:
                words[w] = 1
    ws = [key for key in words.keys() if words[key] > 3 ]
    print(len(ws))
    random.shuffle(ws)
    with open('words.js','w') as f:
        f.write(str(ws))
    # print(list(words))

sqlite3_to_words()
