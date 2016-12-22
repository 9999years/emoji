All the emoji from [the Unicode.org
charts](http://unicode.org/emoji/charts/full-emoji-list.html) as images, in one
place.

The actual images are in `img/...` and are in the form of
`<codepoint>_<vendor>.png`, and are generated with `process.py`, which relies on
`full-emoji-list.html` (which is just a direct copy of
[unicode.org/emoji/charts/full-emoji-list.html](http://unicode.org/emoji/charts/full-emoji-list.html)).

`img/` is a little bit messy, to say the least (18,000+ files), but I don’t
really feel like sorting it.
