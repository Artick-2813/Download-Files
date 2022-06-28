CREATE TABLE IF NOT EXISTS image(

id INTEGER PRIMARY KEY,

title TEXT NOT NULL,

resolution TEXT NOT NULL,

name_file TEXT NOT NULL,

datetime INTEGER NOT NULL,

UNIQUE ("title") ON CONFLICT IGNORE

);