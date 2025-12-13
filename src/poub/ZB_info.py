from xml.dom import minidom
from sgmllib import SGMLParser
import html.entities
#xmldoc=minidom.parse('E:/Documents Marc/Mes Images/2007/08_07_Italie/zb4meta.info')
#print xmldoc.toxml()

class photo:
    def __init__(self,nom):
        self.nom=nom
        self.note=0
        self.theme=[]
        
    def __repr__(self):
        return self.nom
    
class BaseHTMLProcessor(SGMLParser):
    def reset(self):
        # extend (called by SGMLParser.__init__)
        self.pieces = []
        SGMLParser.reset(self)

    def unknown_starttag(self, tag, attrs):
# called for each start tag
# attrs is a list of (attr, value) tuples
# e.g. for <pre class="screen">, tag="pre", attrs=[("class", "screen")]
# Ideally we would like to reconstruct original tag and attributes, but
# we may end up quoting attribute values that weren't quoted in the source
# document, or we may change the type of quotes around the attribute value
# (single to double quotes).
# Note that improperly embedded non?HTML code (like client?side Javascript)
# may be parsed incorrectly by the ancestor, causing runtime script errors.
# All non?HTML code must be enclosed in HTML comment tags (<!?? code ??>)
# to ensure that it will pass through this parser unaltered (in handle_comment).
        print(tag,attrs)
        
        strattrs = "".join([' %s="%s"' % (key, value) for key, value in attrs])
        self.pieces.append("<%(tag)s%(strattrs)s>" % locals())

    def unknown_endtag(self, tag):
# called for each end tag, e.g. for </pre>, tag will be "pre"
# Reconstruct the original end tag.
        #print tag
        self.pieces.append("</%(tag)s>" % locals())

    def handle_charref(self, ref):
# called for each character reference, e.g. for "&#160;", ref will be "160"
# Reconstruct the original character reference.
        self.pieces.append("&#%(ref)s;" % locals())

    def handle_entityref(self, ref):
# called for each entity reference, e.g. for "&copy;", ref will be "copy"
# Reconstruct the original entity reference.
        self.pieces.append("&%(ref)s" % locals())
# standard HTML entities are closed with a semicolon; other entities are not
        if ref in html.entities.entitydefs:
            self.pieces.append(";")

    def handle_data(self, text):
# called for each block of plain text, i.e. outside of any tag and
# not containing any character or entity references
# Store the original text verbatim.
        #print text
        self.pieces.append(text)

    def handle_comment(self, text):
# called for each HTML comment, e.g. <!?? insert Javascript code here ??>
# Reconstruct the original comment.
# It is especially important that the source document enclose client?side
# code (like Javascript) within comments so it can pass through this
# processor undisturbed; see comments in unknown_starttag for details.
        self.pieces.append("<!??%(text)s??>" % locals())

    def handle_pi(self, text):
# called for each processing instruction, e.g. <?instruction>
# Reconstruct original processing instruction.
        self.pieces.append("<?%(text)s>" % locals())

    def handle_decl(self, text):
# called for the DOCTYPE, if present, e.g.
# <!DOCTYPE html PUBLIC "?//W3C//DTD HTML 4.01 Transitional//EN"
# "http://www.w3.org/TR/html4/loose.dtd">
# Reconstruct original DOCTYPE
        self.pieces.append("<!%(text)s>" % locals())

    def output(self):
        """Return processed HTML as a single string"""
        return "".join(self.pieces)


#parser=BaseHTMLProcessor()
#parser.feed(open('E:/Documents Marc/Mes Images/2007/08_07_Italie/zb4meta.info').read())
#print parser.output()

#from unicodedata import *
from codecs import *

fich=open('C:\Documents and Settings\Bureau\Mes documents\Developpement logiciels\Workspace\Photo\photos\Thumbs/zb4meta.info','r','utf16')
#fich=open('E:/Documents Marc/Mes Images/2007/04_07_Jordanie/selection_jordanie.fotos','r')
print(fich.encoding)

liste_photos=[]
while 1:
    ligne=fich.readline()
    print(ligne)
    if not(ligne):
        break
    if '<item:' in ligne:
        p=photo(ligne[7:-1])
        liste_photos.append(p)
    #print ligne
fich.close()
print(liste_photos)
