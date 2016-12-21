import base64
#out = base64.b64decode(in)
from html.parser import HTMLParser
import codecs

def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]

class emoji_parser(HTMLParser):
    codepoint = 'XXXXX'
    image_count = 0
    def get_attr(self, attrs, name):
        attr = next((attr for attr in attrs if attr[0] == name), None)
        if attr is None:
            return attr
        else:
            return attr[1]

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            name = self.get_attr(attrs, 'name')
            if name is not None:
                self.image_count = 0
                self.codepoint = name
        elif tag == 'img':
            self.image_count += 1
            suffix = '_'
            if self.image_count == 1:
                suffix += 'chart'
            elif self.image_count == 2:
                suffix += 'apple'
            elif self.image_count == 3:
                suffix += 'google'
            elif self.image_count == 4:
                suffix += 'twitter'
            elif self.image_count == 5:
                suffix += 'emoji_one'
            elif self.image_count == 6:
                suffix += 'facebook'
            elif self.image_count == 7:
                suffix += 'fb_messenger'
            elif self.image_count == 8:
                suffix += 'samsung'
            elif self.image_count == 9:
                suffix += 'windows'
            elif self.image_count == 10:
                suffix += 'gmail'
            elif self.image_count == 11:
                suffix += 'softbank'
            elif self.image_count == 12:
                suffix += 'docomo'
            elif self.image_count == 13:
                suffix += 'kddi'
            suffix += '.png'
            base64data = self.get_attr(attrs, 'src')
            if base64data.startswith('data:image/png;base64,'):
                base64data = remove_prefix(base64data, 'data:image/png;base64,')
                print(self.codepoint)
                with open('./img/' + self.codepoint + suffix, 'wb') as out_file:
                    out_file.write(base64.b64decode(base64data))

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass

with codecs.open('data.html', encoding = 'utf-8', mode = 'r') as data_file:
    data = data_file.read()
    parser = emoji_parser()
    parser.feed(data)
