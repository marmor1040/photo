# -*- coding: latin-1 -*-
import sys,pickle,os
import os.path as osp
import shutil
from PyQt5 import QtCore, QtWidgets
from src import preferences as PREFERENCES
from IhmRenommerImage import Ui_MainWindow as FormClass
from PyQt5.QtWidgets import QMainWindow as BaseClass

class IhmRenommage(BaseClass,FormClass):
    def __init__(self,repertoire,num_ecran):
        BaseClass.__init__(self)
        self.setupUi(self)
        print(repertoire)
        self.repertoire=repertoire
        if self.repertoire:
            self.modifierRepertoire(self.repertoire)
        self.liste={}
        self.init()
        self.ok=False
        self.setGeometry(*PREFERENCES.RENOMMAGE_GEOMETRY[num_ecran-1])
        self.show()
        
    def init(self):
        QtCore.QObject.connect(self.pb_repertoire,QtCore.SIGNAL("clicked()"),self.selectionRepertoire)
        QtCore.QObject.connect(self.pb_quitter,QtCore.SIGNAL("clicked()"),self.fermer)
        QtCore.QObject.connect(self.pb_tester,QtCore.SIGNAL("clicked()"),self.tester)
        QtCore.QObject.connect(self.pb_valider,QtCore.SIGNAL("clicked()"),self.valider)
        QtCore.QObject.connect(self.ed_avant,QtCore.SIGNAL("textChanged(QString)"),self.modifText)
        QtCore.QObject.connect(self.ed_apres,QtCore.SIGNAL("textChanged(QString)"),self.modifText)
        self.tableWidget.setAlternatingRowColors(True)
        self.pb_valider.setEnabled(False)
        self.ed_avant.setText('Norvege_$1---$3.$4')
        self.ed_apres.setText('Norvege_$3---$1.$4')
        self.tableWidget.clearContents()
        if self.repertoire:
            self.afficherfichier(self.repertoire)

    def getRepertoireDefaut(self):
        rep = None
        if osp.isfile('rep_defaut.dat'):
            f = open('rep_defaut.dat')
            rep = str(pickle.load(f))
            f.close()
        return rep
        
    def setRepertoireDefaut(self,rep):
        f = open('rep_defaut.dat','w')
        pickle.dump(rep,f)
        f.close()
    
    def modifText(self,text):
        self.pb_valider.setEnabled(False)
        
    def selectionRepertoire(self):
        self.splitter.setSizes([340,150])
        if not self.repertoire:
            self.repertoire = 'c:'
        rep = str(QtWidgets.QFileDialog.getExistingDirectory (self.window,self.tr("Selection d'un r�pertoire"),
                                                 self.repertoire,
                                                 QtWidgets.QFileDialog.ShowDirsOnly))
        if not rep == '':
            self.modifierRepertoire(rep)
            
    def modifierRepertoire(self,rep):
        self.ed_repertoire.setText(rep)
        self.tableWidget.clearContents()
        self.afficherfichier(rep)
        self.setRepertoireDefaut(rep)
 
    def afficherfichier(self,rep):
        self.liste={}
        if rep:
            self.repertoire=rep
            num=0
            try:
                l=os.listdir(rep)
            except:
                l=[]
            self.tableWidget.setRowCount(len(l))
            ldate=[]
            for i in l:
                ldate.append((os.stat(rep+'/'+i).st_ctime,i))
            for i in sorted(ldate):
                self.liste[i[1]]=''
                self.tableWidget.setItem(num,0,QtWidgets.QTableWidgetItem(i[1]))
                self.tableWidget.setItem(num,1,QtWidgets.QTableWidgetItem(''))
                num+=1
        self.tableWidget.resizeColumnToContents(0)

    def tester(self):
        format_avant=str(self.ed_avant.text())
        format_apres=str(self.ed_apres.text())
        self.val_dolar={}
        for cle in sorted(self.liste.keys()):
            #print cle,self.transforme(cle,format_avant,format_apres)
            self.liste[cle]=self.transforme(cle,format_avant,format_apres)
        #print self.liste[0]
        for i in range(self.tableWidget.rowCount()):
            cle = str(self.tableWidget.item(i,0).text())
            #print i,self.liste[cle]
            item=QtWidgets.QTableWidgetItem(self.liste[cle])
            if list(self.liste.values()).count(self.liste[cle])>1 or list(self.liste.keys()).count(self.liste[cle])>0:
                item.setForeground(QtWidgets.QBrush(QtWidgets.QColor('red')))
            self.tableWidget.setItem(i,1,item)
        self.tableWidget.resizeColumnToContents(1)        
        self.pb_valider.setEnabled(True)
  
    def valider(self):
        rep=self.repertoire+'/'
        print('Renommage ...', end=' ')
        for (cle,val) in list(self.liste.items()):
            if val != '':
            #print rep+cle,rep+val
                if osp.isfile(rep+val):
                    print('fichier existant')
                else:
                    shutil.move(rep+cle,rep+val)
        print('Termin�')
        self.afficherfichier(self.repertoire)
            
  
    def fermer(self):
        self.window().close()
        
    def tr(self,str):
        return QtCore.QString(str)

    def transforme(self,chaine,av,ap):
        l=cherche(av,chaine,{})
        #print 'l=',l
        if l:
            for c,v in list(l.items()):
                #print '#1',c,v,ap
                ap=ap.replace(c,v)
                c1=c[0]+'('+c[1]
                #print 'c1=',c1
                if c1 in ap:
                    #try:
                    i=ap.index(c1)
                    n=ap[i+2]
                    f=ap.index(')',i)
                    #print '#2',ap[i:f+1]
                    op=ap[i+3]
                    i1=ap.index(',',i+3)
                    if i1:
                        val=int(ap[i+4:i1])
                        num_ch=int(ap[i1+1:f])
                    else:
                        val=int(ap[i+4:f])
                    #print '#3',op,val,num_ch
                    if op=='+':
                        init=int(v)
                        #print '#4',ap.replace(ap[i:f+1],str1(init+val,num_ch))
                        ap=ap.replace(ap[i:f+1],str1(init+val,num_ch))
                    if op=='-':
                        init=int(v)
                        #print '#5',ap.replace(ap[i:f+1],str(init-val))
                        ap=ap.replace(ap[i:f+1],str1(init-val,num_ch))
                    if op==':':
                        #print ':::',self.val_dolar,val,c
                        if c in self.val_dolar:
                            value=self.val_dolar[c]+1
                            #print '1',value
                        else:
                            value=val
                        self.val_dolar[c]=value
                        #print self.val_dolar
                        #print '#6',ap.replace(ap[i:f+1],str1(value,num_ch))
                        ap=ap.replace(ap[i:f+1],str1(value,num_ch))
                    #except ValueError:
                    #    print v,'n\'est pas un entier'
            return ap
        else:
            return ''
        
def str1(val,n):
    s='%.'+str(n)+'i'
    return s % val

# recherche la correspondance du $ suivant de s1 dans s2 
def cherche(s1,s2,l):
    #print 'cherche',s1,s2,l
    if s1 == s2:
        return l
    if s1 == '' and s2 == '':
        return l
    index=s1.find('$')
    #print index,s1[0:index],s2[0:index]
    if s1[0:index] == s2[0:index]:
        #print index+2,len(s1)
        if index+2<len(s1):
            #print 's1='+s1
            ch=s1[index+2]
            #print 'ch='+ch
            index2=s2.find(ch,index)
            i=len(l)+1
            l1=l
            l1['$'+str(i)]=s2[index:index2]
            #print l1
            #print s1[index+2:],'%',s2[s2.find(ch,index):]
            return cherche(s1[index+2:],s2[s2.find(ch,index):],l1)
        else:
            i=len(l)+1
            l1=l
            l1['$'+str(i)]=s2[index:]
            return l1
    else:
        return False
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("plastique")
    window = QtWidgets.QMainWindow()
    ui=IhmRenommage(window)
    window.show()
    sys.exit(app.exec_())
    
    
    
    
    

    
