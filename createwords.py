import sqlite3


def sqlite3_to_words():
    sqlite3_conn = sqlite3.connect('idiom.db')
    sqlite3_cursor = sqlite3_conn.cursor()
    sqlite3_cursor.execute('SELECT chengyu FROM idiom')

    words = set()
    for chengyu, in sqlite3_cursor:
        for w in chengyu:
            words.add(w)

    with open('words.js','w') as f:
        f.write(str(list(words)))
    # print(list(words))

sqlite3_to_words()
