All the emoji from [the Unicode.org
charts](http://unicode.org/emoji/charts/full-emoji-list.html) as images, in one
place.

The actual images are in `img/...` and are in the form of
`<codepoint>_<name>_<vendor>.png`, and are generated with `process.py`, which
relies on `full-emoji-list.html` (which is just a direct copy of
[unicode.org/emoji/charts/full-emoji-list.html](http://unicode.org/emoji/charts/full-emoji-list.html)).

An example filename is
`1f61d_face_with_stuck-out_tongue_and_closed_eyes_facebook.png`.

Filenames may contain hyphens (`U+2d -`) underscores (`U+5f _`), and a variety
of diacritics (for flags such as Curaçao’s: `U+1f1e8 U+1f1fc`) but will not
contain spaces, ampersands, asterisks, pounds, commas, periods other than for
the file extension, colons, and quotes (`U+20  `, `U+26 &`, `U+23 #`, `U+2c ,`,
`U+2e .`, `U+3a :`, `U+201c “`, `U+201d ”`, and `U+2019 ’` respectively).
