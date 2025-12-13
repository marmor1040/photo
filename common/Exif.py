# -*- coding:utf-8 -*-
"""
Created on 10 juil. 2011

@author: Bureau
"""

#import pyexiv2
import piexif
from src import preferences

def loadExif(fn):
    return piexif.load(fn)

def saveExif(fn,exif):
    piexif.insert(piexif.dump(exif),fn)

def printExif(exif):
    for ifd in ("0th", "Exif", "GPS", "1st"):
        for tag in exif[ifd]:
            nom = piexif.TAGS[ifd][tag]["name"]
            if nom != "MakerNote":
                print(ifd,tag,nom,"=",exif[ifd][tag],type(exif[ifd][tag]))
                
# def copyExifFile(ch_photo,ch_thumbnail):
#     exif_photo = getExif(ch_photo)
#     exif_thumb = getExif(ch_thumbnail)
#     exif_photo.copy(exif_thumb)
#     exif_thumb.write()
#     
# def copyExif(exif_photo,ch_thumbnail):
#     exif_thumb = getExif(ch_thumbnail)
#     exif_photo.copy(exif_thumb)
#     exif_thumb.write()
#     
# def getExifData(file):
#     exif = getExif(file)
#     return getHt(exif)
    
def getHt(exif=None,image=None):
    if image:
        exif = loadExif(image)
    ht={}
    ht_exif={}
        
    for ifd in ("0th", "Exif", "GPS", "1st"):
        for tag in exif[ifd]:
            nom = piexif.TAGS[ifd][tag]["name"]
            if nom != "MakerNote":
                ht_exif[nom] =  exif[ifd][tag]
            if nom == "Orientation":
                ht["ifd_orientation"] = ifd
                ht["tag_orientation"] = tag
                ht["paysage"] = ht_exif[nom] == 1
    for (nom,tag) in list(preferences.DESCRIPTION_PHOTO.items()):
        
        if tag in list(ht_exif.keys()):
            val = ht_exif[tag]
            if nom == 'date':
                val = getDate(val)
            elif nom == 'heure':
                val = getHeure(val)
            elif nom == 'vitesse':
                val = '1/%.0fsec' % (float(val[1])/val[0])
            elif nom == 'focale':
                val = "%.0fmm" % (float(val[0])/val[1])
            elif nom == 'pivoter':
                val = getPivoter(val)
            elif nom == 'flash':
                val = getFlash(val)
            elif type(val) is tuple:
                val = "%.2f" % (float(val[0])/val[1])
            ht[nom] = val
        else:
            ht[nom] = "unknown"
    try:
        if ht["paysage"]:
            ht['taille']="%ix%i" % (ht['tailleX'],ht['tailleY'])
        else:
            ht['taille']="%ix%i" % (ht['tailleY'],ht['tailleX'])
        del ht['tailleY'] 
        del ht['tailleX']
    except: pass
    if ht['pivoter'] == "unknown": ht['pivoter'] = 0
    return ht

# def setHt(exif,ht):
#     printExif(exif)
#     for (nom,tag) in preferences.DESCRIPTION_PHOTO.iteritems():
#         if tag in exif.exif_keys:
#             val = exif[tag].raw_value
#             if nom == 'orientation':
#                 exif[tag].raw_value = ht[nom]
#     
#     printExif(exif)

# def changeOrientation(exif,ht_exif):
#     # pour ne plus pivoter
#     exif[ht_exif["ifd_orientation"]][ht_exif["tag_orientation"]] = 0
#     ht_exif["orientation"] = 0
#     ht_exif["paysage"] = 0

    
# def getExifValue(file,nom):
#     data = getExifData(file)
#     if nom == 'jour':
#         if not data.has_key('date'): return None
#         return data['date'].split()[0]
#     else:
#         if not data.has_key(nom): return None
#         return data[nom]

def getDate(ch):
    date = ch.split(' ')[0]
    d = date.strip().split(':')
    return d[2]+'/'+d[1]+'/'+d[0]
    
def getHeure(ch):
    return ch.split(' ')[1]

def getFlash(v):
    if v == 16:
        return 'Non'
    else:
        return 'Oui'
    
def getPivoter(ch):
    if ch == 6:
        return -90
    elif ch == 8:
        return 90
    else:
        return 0
    
def getChTriDate(exif):
    import datetime
    try:
        j,h = exif['date'],exif['heure']
        vj = j.split('/')
        vh = h.split(':')
        return datetime.datetime(int(vj[2]),int(vj[1]),int(vj[0]),int(vh[0]),int(vh[1]),int(vh[2]))
    except:
        return datetime.datetime.now()
    
# from PIL import Image
# def fairePivoterPhoto(photo,exif_ht,exif_im):
#     print '-> rotation de ',photo,exif_ht["orientation"]
#     image = Image.open(photo)
#     im_rot = image.rotate(exif_ht["orientation"])
#     nom_piv = photo[:-4]+"_piv.JPG"
#     im_rot.save(nom_piv,format="JPEG")
#     changeOrientation(exif_im,exif_ht)
#     saveExif(nom_piv,exif_im)
    
if __name__ == "__main__":
    import os.path as osp
    import glob
#     for f in glob.glob("../test/*.jpg"):
#         #f = '../test/photo3.jpg'
#         print f
#         exif_im = loadExif(f)
#         #printExif(exif_im)
#         ht = getHt(exif_im)
#         #print ht
#         print ht['appareil']
#         orient = ht['orientation']
#         print orient
#         ht['orientation']='0'
#         #setHt(exif_im,ht)
#         #print getHt(exif_im)
#          
    
    f = '../test/IMG_2497.JPG'
    print(f)
    exif=loadExif(f)
    ht = getHt(exif)
    #printExif(exif)
    print(ht)
    print(ht['orientation'])
    fairePivoterPhoto(f,ht,exif)
    exif=loadExif('../test/IMG_2497_piv.JPG')
    ht = getHt(exif)
    print(ht)