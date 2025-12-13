'''
Created on 17 mai 2011

@author: to07184
'''
import os.path as osp
import time,glob,sys
from multiprocessing import Process, Pipe
import threading
import Image
from PIL.ImageQt import ImageQt
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon,QImage,QPixmap
from PyQt5.QtCore import QString,Qt

#FormClass, BaseClass = loadUiType(osp.join(osp.dirname(osp.realpath(__file__)),
#                                           '../Ihm/fen_photo.ui'))

#class FenetrePhoto(BaseClass, FormClass):    
#    def __init__(self):
#        BaseClass.__init__(self, None)
#        self.setupUi(self)
#        
#        #image = QImage(QString("../photos2/comp_Cuba_(19_04_2010)_0656.JPG"),'JPG')
#        t0=time.time()
#        image = Image.open("../photos2/comp_Cuba_(19_04_2010)_0656.JPG")
#        print time.time()-t0
#        pix = QPixmap.fromImage(ImageQt(image),Qt.DiffuseDither)
#        self.label.setPixmap(pix)
        
#im.rotate(45).show()

#im.thumbnail((256, 256), Image.ANTIALIAS)
#im.save("photo.thumbnail.jpg", "JPEG")

#import ImageDraw
#draw = ImageDraw.Draw(im)
#draw.line((0, 0) + im.size, fill=128)
#draw.line((0, im.size[1], im.size[0], 0), fill=128)
#del draw
#im.show()

#import ImageEnhance
#enhancer = ImageEnhance.Sharpness(im)
#im2 = enhancer.enhance(20.0)
#larg=im.size[0]
#long=im.size[1]
#im3=Image.new('RGB',(larg*2,long))
#im3.paste(im,(0,0))
#im3.paste(im2,(larg,0))
#
#im3.show()
#im3.save("photo2.jpg", "JPEG")

def creer_thumbnail(ch_photo,ch_thumbnail,size):
    im = Image.open(ch_photo)
    im.thumbnail(size, Image.ANTIALIAS)
    im.save(ch_thumbnail,"JPEG")

#for i in [11,12,13,14,15,16,17]:
#    nom = '../photos/Croatie00'+str(i)+'.JPG'
#    nom1 = '../photos/Croatie00'+str(i)+'_tn.JPG'
#    creer_thumbnail(nom,nom1,(256,256))


if __name__ == "__main__":
    nom = '../photos/Vietnam_20110426_0214.JPG'
    im = Image.open(nom)
    import ImageEnhance
    enhancer = ImageEnhance.Sharpness(im)
    for i in range(10):
        im2 = enhancer.enhance(i)
        im2.save('../photos/Vietnam_20110426_0214'+str(i)+'.JPG', "JPEG")