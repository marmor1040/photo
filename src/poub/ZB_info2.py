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
    
#def mafunc(self, writer, indent="", addindent="", newl=""):
#    # indent = current indentation
#    # addindent = indentation to add to higher levels
#    # newl = newline string
#    writer.write(indent+"<" + self.tagName)
#    b_ass = self.tagName == 'ASSEMBLY'
#    attrs = self._get_attributes()
#    a_names = attrs.keys()
#    a_names.sort()
#
#    writer.write("\n")
#    for a_name in a_names:
#        writer.write("    %s=\"" % a_name)
#        if b_ass and a_name == 'value':
#            minidom._write_data(writer, attrs[a_name].value.replace(' ','\n    '))
#        else:
#            minidom._write_data(writer, attrs[a_name].value)
#        writer.write("\"\n")
#    if self.childNodes:
#        writer.write(">%s"%(newl))
#        for node in self.childNodes:
#            node.writexml(writer,indent+addindent,addindent,newl)
#        writer.write("%s</%s>%s" % (indent,self.tagName,newl))
#    else:
#        writer.write("/>%s"%(newl))
#
#minidom.Element.writexml = mafunc

from codecs import *
fich='C:\Documents and Settings\Bureau\Mes documents\Developpement logiciels\Workspace\Photo\photos\Thumbs/zb4meta.info'
cont=open(fich,'r','utf16').read()
print(cont)
f=open('res.dat','w')
f.write(cont)
f.close()
doc = minidom.parse('res.dat')
print('doc=',doc)


#from codecs import *
#parser=BaseHTMLProcessor()
#parser.feed(open(fich,'r','utf16').read())
#print parser.output()



