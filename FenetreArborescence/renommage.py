# -*- coding: latin-1 -*-
import os,shutil,math,time,re
import os.path as osp
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from src import preferences as PREFERENCES
from Ihm.aide_renommage import Ui_Aide as FormClass
from PyQt5.QtWidgets import QWidget as BaseClass
    
class aideRenommage(BaseClass,FormClass):
    def __init__(self,geom):
        BaseClass.__init__(self, None)
        self.setupUi(self)
        self.move(geom.x()+geom.width(),25)
        self.show()

class dataRenommage():
    def __init__(self,ihm):
        self.album = None
        self.ihm = ihm
        self.liste_photos = None
        self.liste_renommage = None
        
    def setAlbum(self,alb):
        if alb and alb.estUnAlbum():
            self.album = alb
        else:
            self.album = None
        
    def majFenetre(self,alb):
        self.setAlbum(alb)
        self.auto()
                
    def afficherFichiers(self):
        self.liste={}
        if self.album:
            num=0
            bTriDate = self.ihm.cbRenTrierParDate.checkState() == QtCore.Qt.Checked
            if bTriDate:
                self.liste_photos = self.album.listeJPGTrieParDate(chemin=False)
            else:
                self.liste_photos = self.album.listeJPG(chemin=False)
            self.ihm.tableWidget.setRowCount(len(self.liste_photos))
            for f in self.liste_photos:
                self.ihm.tableWidget.setItem(num,0,QtWidgets.QTableWidgetItem(f))
                self.ihm.tableWidget.setItem(num,1,QtWidgets.QTableWidgetItem(''))
                num+=1
            self.ihm.tableWidget.resizeColumnToContents(0)
            self.ihm.tableWidget.setColumnWidth(0,self.ihm.tableWidget.columnWidth(0)+50)
            self.ihm.sbNbChiffres.setValue(int(math.log10(num)+1))
      
    def auto(self):
        self.ihm.edtAvant.setText("*.*")
        if self.album:
            self.ihm.edtApres.setText(osp.basename(self.album.repertoire()[:-1])+"_$num_$date.JPG")
            self.afficherFichiers()
            self.tester()
        
    def tester(self):
        if not self.liste_photos:return
        format_avant = str(self.ihm.edtAvant.text())
        format_apres = str(self.ihm.edtApres.text())
        num = self.ihm.sbValeurInit.value()
        nb_ch = self.ihm.sbNbChiffres.value()
        self.liste_renommage = []
        for nom in self.liste_photos:
            #print cle,self.transforme(cle,format_avant,format_apres)
            #res = self.transforme(nom,format_avant,self.motcle(nom,format_apres,num))
            if not chercheRe(format_avant,nom,['.*']*format_avant.count('*')):
                res = ''
            else:
                ht_exif = self.album.getExif(nom)
                ht_exif.update(getValeurDolar(nom,format_avant))
                ht_exif["num"] = ("%0"+str(nb_ch)+'i') % num
                res = transforme(format_apres,ht_exif)
            self.liste_renommage.append(res)
            if res: num += 1
        #print self.liste[0]
        for i in range(len(self.liste_renommage)):
            #cle = unicode(self.ihm.tableWidget.item(i,0).text())
            #print i,self.liste[cle]
            new = self.liste_renommage[i]
            item = QtWidgets.QTableWidgetItem(new)
            #plusieurs renommage identiques ou nom existant
            if self.liste_renommage.count(new)>1 or self.liste_photos.count(new)>0: 
                item.setForeground(QtWidgets.QBrush(QtWidgets.QColor('red')))
            self.ihm.tableWidget.setItem(i,1,item)
        self.ihm.tableWidget.resizeColumnToContents(1)
        self.ihm.tableWidget.setColumnWidth(1,self.ihm.tableWidget.columnWidth(1)+100)
        self.ihm.btValider.setEnabled(True)
    
    def valider(self):
        rep = self.album.repertoire()+'/'
        print('Renommage ...', end=' ')
        for (old,new) in zip(self.liste_photos,self.liste_renommage):
            if new != '':
            #print rep+cle,rep+val
                if osp.isfile(rep+new):
                    print('fichier existant :',new)
                else:
                    self.album.renommerPhoto(old,new)
                    #shutil.move(old,rep+new)
        print('Termin�')
        self.afficherFichiers()
        self.ihm.majMiniatures() 
       
    def detruireFichiers(self):
        msgBox = QMessageBox(self.ihm)
        ok = msgBox.addButton("Valider", QMessageBox.AcceptRole)
        ko = msgBox.addButton("Annuler",QMessageBox.RejectRole)
        msgBox.setText("T'es s�r de vouloir d�truire ?")
        ret = msgBox.exec_()
        if msgBox.clickedButton() == ok:
            for (old,new) in zip(self.liste_photos,self.liste_renommage):
                if new != '':
                    os.remove(self.album.repertoire()+old)
        self.ihm.majMiniatures() 
           
#     def tr(self,str):
#         return QtCore.QString(str)
# 
#     def motcle(self,f,val,num):
#         try:
#             exif = self.album.getExif(f)
#             nb_chiffres = self.ihm.sbNbChiffres.value()
#             format = "%0"+str(nb_chiffres)+"i"
#             val = val.replace('$num',format % num)
#             for c,v in PREFERENCES.DESCRIPTION_PHOTO.iteritems():
#                 if exif.has_key(c):
#                     val = val.replace('$'+c,str(exif[c]))
#                 else:
#                     val = val.replace('$'+c,'')
#             val = val.replace(' ','_')
#             val = val.replace(':','_')
#             val = val.replace('/','-')
#             return val
#         except:
#             return ""
#     
#     def transforme(self,chaine,av,ap):
#         l=cherche(av,chaine,{})
#         val_dolar = {}
#         #print 'l=',l
#         if l:
#             for c,v in l.items():
#                 #print '#1',c,v,ap
#                 ap=ap.replace(c,v)
#                 c1=c[0]+'('+c[1]
#                 #print 'c1=',c1
#                 if c1 in ap:
#                     #try:
#                     i=ap.index(c1)
#                     n=ap[i+2]
#                     f=ap.index(')',i)
#                     #print '#2',ap[i:f+1]
#                     op=ap[i+3]
#                     i1=ap.index(',',i+3)
#                     if i1:
#                         val=int(ap[i+4:i1])
#                         num_ch=int(ap[i1+1:f])
#                     else:
#                         val=int(ap[i+4:f])
#                     #print '#3',op,val,num_ch
#                     if op=='+':
#                         init=int(v)
#                         #print '#4',ap.replace(ap[i:f+1],str1(init+val,num_ch))
#                         ap=ap.replace(ap[i:f+1],str1(init+val,num_ch))
#                     if op=='-':
#                         init=int(v)
#                         #print '#5',ap.replace(ap[i:f+1],str(init-val))
#                         ap=ap.replace(ap[i:f+1],str1(init-val,num_ch))
#                     if op==':':
#                         #print ':::',val_dolar,val,c
#                         if val_dolar.has_key(c):
#                             value=val_dolar[c]+1
#                             #print '1',value
#                         else:
#                             value=val
#                         val_dolar[c]=value
#                         #print val_dolar
#                         #print '#6',ap.replace(ap[i:f+1],str1(value,num_ch))
#                         ap=ap.replace(ap[i:f+1],str1(value,num_ch))
#                     #except ValueError:
#                     #    print v,'n\'est pas un entier'
#             return ap
#         else:
#             return ''
#         
# def str1(val,n):
#     s='%.'+str(n)+'i'
#     return s % val
# 
# # recherche la correspondance du $ suivant de s1 dans s2 
# def cherche(s1,s2,l):
#     #print 'cherche',s1,s2,l
#     if s1 == s2:
#         return l
#     if s1 == '' and s2 == '':
#         return l
#     index=s1.find('$')
#     #print index,s1[0:index],s2[0:index]
#     if s1[0:index] == s2[0:index]:
#         #print index+2,len(s1)
#         if index+2<len(s1):
#             #print 's1='+s1
#             ch=s1[index+2]
#             #print 'ch='+ch
#             index2=s2.find(ch,index)
#             i=len(l)+1
#             l1=l
#             l1['$'+str(i)]=s2[index:index2]
#             #print l1
#             #print s1[index+2:],'%',s2[s2.find(ch,index):]
#             return cherche(s1[index+2:],s2[s2.find(ch,index):],l1)
#         else:
#             i=len(l)+1
#             l1=l
#             l1['$'+str(i)]=s2[index:]
#             return l1
#     else:
#         return False
#     
def getValeurDolar(nom,template_prec):
    chs=[nom]
    for ch_imp in template_prec.split('*'):
        if ch_imp:
            if ch_imp == '.': ch_imp = "\."
            res = []
            p = re.compile(ch_imp)
            for ch in chs:
                res += p.sub("@@",ch).split("@@")
            chs = res
    if '' in chs: chs.remove('')
    return dict(list(zip([str(i+1) for i in range(3)],chs)))
    
def cs(s):
    for c in ['$','(',')','[',']','.']:
        s = s.replace(c,'\\'+c)
    return s

def chercheRe(format_chaine,chaine,format_elem):
    # cherche des elements dans une chaine, dont le format g�n�ral est format_chaine
    # et le format de chaque element est donn� dans format_elem
    # exemple, on cherche � r�cup�rer les �l�ment a et 15 dans la chaine toto_a(15)-titi
    # format_chaine = *\(*\)
    # format_elem = ("[a-z]","[0-9]*")
    # retourne ["a","15"]
    try:
        i = 0
        format_chaine = cs(format_chaine)
        fsplit = format_chaine.split('*')
        res = []
        for e in format_elem:
            ssf = fsplit[i] + e + fsplit[i+1]
            res.append(re.search(ssf,chaine).group())
            deb = fsplit[i].replace('\\','')
            fin = fsplit[i+1].replace('\\','')
            res[i] = res[i].replace(deb,'').replace(fin,'')
            i += 1
        if '' in res: return False
        return res
    except:
        return False
    
def transforme(template_suiv,ht_motcle):
    try:
        for k,v in ht_motcle.items():
            if '$'+k in template_suiv:
                template_suiv = template_suiv.replace('$'+k,str(v))
            elif "$("+k in template_suiv:
                    car,dnum,nbch = chercheRe("$("+k+"**,*)",template_suiv,("[+-:]","[0-9]*","[0-9]*"))
                    ch_prec = '$('+k+car+dnum+','+nbch+')'
                    form_val = "%0"+nbch+'i'
                    if car == ':':
                        template_suiv = template_suiv.replace(ch_prec,form_val % (int(dnum)+int(ht_motcle['num'])-1))
                    if car == '+':
                        template_suiv = template_suiv.replace(ch_prec,form_val % (int(v)+int(dnum)))
                    if car == '-':
                        template_suiv = template_suiv.replace(ch_prec,form_val % (int(v)-int(dnum)))

        template_suiv = template_suiv.replace(' ','_').replace(':','_').replace('/','-')
        return template_suiv
    except:
        return ''
    
if __name__ == "__main__":
    s1 = "IMG_0115.JPG"
    temp_prec = "*_*.*"
    temp_suiv = "$2,$3.$1"

    print(getValeurDolar(s1,temp_prec))