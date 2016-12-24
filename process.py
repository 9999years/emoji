import base64
from html.parser import HTMLParser
import codecs

# one-liner to remove a prefix from a string
# eg turn 'file_100.jpg' into '100.jpg' by removing 'file_'
def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]

class emoji_parser(HTMLParser):
    # placeholder values
    codepoint = 'XXXXX'
    # if the next td.name qualifies to be the codepoint name
    next_qualifies = True
    # if the next td.name *is* the codepoint name
    # these two are necessary to figure out which td.name is the cp name
    next_is_name = False
    # number of images encountered in the row
    # for mapping from columns to vendor names
    image_count = 0
    # uh, this is like a list? of image data
    # the codepoint name comes *after* all the images and this parser
    # works linear-ly
    # so we store the image data in this array, get the filenames from the
    # name after we're done parsing a row, and then output each row at once
    image_data = []

    def get_attr(self, attrs, name):
        # get an attribute from a list of attrs
        # the parser is kinda weird about this so we've gotta do some magic to
        # get actual values
        attr = next((attr for attr in attrs if attr[0] == name), None)
        if attr is None:
            return attr
        else:
            return attr[1]

    def write_images(self, prefix):
        # go through image_data and do the actual outputting
        # strip out potentially problematic characters
        # i AM keeping a lot of diacritics in for things like "São Tomé"
        prefix = prefix.replace(' ', '_').replace('&', 'and').replace(',', '').replace(':', '').replace('*', 'asterisk').replace('#', 'pound').replace('“', '').replace('”', '').replace('.', '')
        filename_base = './img/' + self.codepoint + '_' + prefix
        # go through the images
        for image in self.image_data:
            # open the file for writing
            # this might bug if an /img/ directory doesn't exist!
            filename = filename_base + image['suffix']
            with open(filename, 'wb') as out_file:
                out_file.write(image['data'])
        # clear out the list
        self.image_data = []
        return

    def handle_data(self, data):
        #if we have the codepoint name, write the images with it
        if self.next_is_name is True:
            self.write_images(data)
            self.next_is_name = False
            self.next_qualifies = False
        return

    def handle_starttag(self, tag, attrs):
        # we entered an opening tag, figure out what to do with it
        if tag == 'tr':
            #next td.name is the codepoint name
            self.next_qualifies = True
        elif tag == 'a':
            name = self.get_attr(attrs, 'name')
            if name is not None:
                # if an <a> has a 'name' attribute, it denotes the codepoint
                # reset the image counter and use the codepoint for filenames
                self.image_count = 0
                self.codepoint = name
        if tag == 'td':
            classes = self.get_attr(attrs, 'class')
            if 'miss' in classes:
                # a missing image in the table (shown as an underscore)
                # increment the image counter
                # otherwise filenames get messed up for the rest of the row
                self.image_count += 1
            elif 'name' in classes:
                # if the next td.name is the codepoint, it is the codepoint
                if self.next_qualifies is True:
                    self.next_is_name = True
                    # but the one AFTER that isn't
                    self.next_qualifies = False
        elif tag == 'img':
            # if we have an image, figure out the filename
            # add the vendor based on its column in the row
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
            # get the image's raw data and convert it from base64 to binary
            base64data = self.get_attr(attrs, 'src')
            if base64data.startswith('data:image/png;base64,'):
                # ignore non b64 images
                # just to make sure the script is doing what we want
                # print(self.codepoint)
                # strip out header
                base64data = remove_prefix(base64data, 'data:image/png;base64,')
                # put the image vendor and image data in the array for later
                self.image_data.append({
                    'suffix': suffix,
                    'data': base64.b64decode(base64data)
                    })
        return

# read file and feed it to the parser
# full-emoji-list.html should be a direct copy of this page:
# http://unicode.org/emoji/charts/full-emoji-list.html
# since there are no externally loaded images, don't bother saving a "complete"
# page or whatever; html only is fine
with codecs.open('full-emoji-list.html', encoding = 'utf-8', mode = 'r') as data_file:
    # get contents of data.html
    data = data_file.read()
    # create a parser
    parser = emoji_parser()
    # put the contents into the parser
    parser.feed(data)
