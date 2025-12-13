# -*- coding: latin-1
'''
Created on 17 mai 2011

@author: to07184
'''

import copy

class chainElem:
    def __init__(self,val,p=None,n=None):
        self.previous = p
        self.next = n
        self.value = val
        self.select = False
        
    def __repr__(self):
        return '@'+self.value.__repr__()
            
class chainList:
    def __init__(self,val=None):
        self.liste = []
        self.selected = set()
        if val:
            if isinstance(val,chainList):
                self.liste = val.liste
            else:
                if not type(val) is list:
                    val = [val]
                prec = None
                for v in val:
                    e = chainElem(v,prec)
                    if prec:
                        prec.next = e
                    self.liste.append(e)
                    prec = e

    def __getitem__(self,n):
        if isinstance(n,slice):
            ret = chainList()
            ret.liste = self.liste[n]
            return ret
        else:
            return self.liste[n].value
    
    def __setitem__(self,n,val):
        if isinstance(val,chainElem):
            self.liste[n] = val
        else:
            self.liste[n].value = val
#        prec = self.liste[n].previous
#        suiv = self.liste[n].next
#        elem = chainElem(val,prec,suiv)
#        if prec:
#            prec.next = elem
#        if suiv:
#            suiv.previous = elem
#        self.liste[n] = elem
        
    def append(self,val):
        if len(self.liste) > 0:
            prec = self.liste[-1]
        else:
            prec = None
        e = chainElem(val,prec)
        if prec:
            prec.next = e
        self.liste.append(e)
        
    def __len__(self):
        return len(self.liste)
    
    def first(self):
        if self.liste:
            return self.liste[0].value
        else:
            return None
    
    def last(self):
        if self.liste:
            return self.liste[-1].value
        else:
            return None
    
    def firstPtr(self):
        if self.liste:
            return self.liste[0]
        else:
            return None
    
    def lastPtr(self):
        if self.liste:
            return self.liste[-1]
        else:
            return None
    
    def next(self,i): # indice dans la liste
        if i < len(self.liste):
            return self.liste[i].next.value
        else:
            return None
    
    def previous(self,i): # indice dans la liste
        if i > 0:
            return self.liste[i].previous.value
        else:
            return None
    
    def nextPtr(self,ptr):  # ptr vers un element
        if ptr != self.last():
            return ptr.__next__
        else:
            return None
        
    def previousPtr(self,ptr): # ptr vers un element
        if ptr != self.first():
            return ptr.previous
        else:
            return None
    
    def ptr(self,i):
        if self.liste:
            return self.liste[i]
        
    def index(self,val):
        ptr = self.firstPtr()
        i = 0
        while ptr:
            #print ptr.value, val,type(ptr.value),type( val), ptr.value == val
            if ptr.value == val:
                return i
            i += 1
            ptr = self.nextPtr(ptr)
        return None

    def select(self,i,b):
        if not isinstance(i,int):
            i = self.index(i)# chercher l'�lement par son nom
        if b:
            self.selected.add(i)
        else:
            self.selected.remove(i)
        self.liste[i].select = b
            
    def isSelected(self,i):
        if not isinstance(i,int):
            i = self.index(i)# chercher l'�lement par son nom
        return i in self.selected
    
    def getSelected(self):
        return self.selected
            
    def getFirstSelected(self):
        return min(self.selected)
            
    def insert(self,i,val):
        if self.liste:
            prec = self.liste[i].previous
            suiv = self.liste[i]
        else:
            prec,suiv = None,None
        if isinstance(val,chainList):
            e = val.ptr(0)
            f = val.ptr(-1)
            e.previous = prec
            f.next = suiv
            self.liste = self.liste[:i]+val.liste+self.liste[i:]
        else:
            e = chainElem(val,prec,suiv)
            f = e
            self.liste.insert(i,e)
        if prec:
            prec.next = e
        if suiv:
            suiv.previous = f
        
    def remove(self,i,j=None):
        e = self.liste[i]
        if j:
            f = self.liste[j]
        else:
            f = e
        if e.previous:
            e.previous.next = f.__next__
        if f.__next__:
            f.next.previous = e.previous
        if j:
            ret = self.liste[i:j+1]
            del self.liste[i:j+1]
            ret[0].previous = None
            ret[-1].next = None
            l = chainList()
            l.liste = ret
            return l
        else:
            return self.liste.pop(i).value
        
    def __repr__(self):
        ch = '-{'
        n = 0
        ptr = None
        ok = len(self.liste)
        if self.liste:
            ptr = self.liste[0]
        while ok:
            ch += ','*n + ptr.__repr__()+'\n'
            n = 1
            ok = ptr != self.liste[-1]
            ptr = ptr.__next__
        ch += '}-'
        if False:
            ch += ' reverse = -{'
            n = 0
            ok = len(self.liste)
            if self.liste:
                ptr = self.liste[-1]
            while ok:
                ch += ','*n + ptr.__repr__()
                n = 1
                ok = ptr != self.liste[0]
                ptr = ptr.previous
            ch += '}- ->' 
            ch += self.liste.__repr__()
        if True:
            ch += 'selection :'+self.selected.__repr__()
        return ch
    
    def apply(self,all,fct,*args):
        ret = []
        for ptr in self.liste:
            if all or ptr.select:
                r = fct(*(ptr.value,)+args)
                if r:
                    ret.append(r)
        if ret:
            return ret

class cl:
    def __init__(self,v):
        self.value = v
       
    def add(self,a):
        self.value += a
        
    def __repr__(self):
        return 'cl:'+str(self.value)
    
if __name__ == "__main__":
    liste = chainList([i for i in range(10)])
    print('1',liste)
    ptr = liste.firstPtr()
    print('first=',ptr)
    ptr=ptr.next.next.__next__
    print('4�me=',ptr)
    print('4�me=13')
    ptr.value = 13
    print('2',liste)
    print('7�me=15')
    liste[6] = 15
    print('3',liste)
    print('append 23')
    liste.append(23)
    print('4',liste)
    print('insert 113 en 5�me position')
    liste.insert(4,113)
    print('5',liste)
    print('detruit 9�me element')
    liste.remove(8)
    print('6',liste)
    print('detruit 1er element')
    liste.remove(0)
    print('7',liste)
    print('detruit dernier element')
    print(liste.remove(-1))
    print('8',liste)
    liste = chainList([1])
    print('9',liste)
    print('remove(0)',liste.remove(0))
    print('10',liste)
    liste.insert(0,5)
    print('11',liste)
    liste.insert(0,10)
    print('12',liste)
    liste.insert(0,liste.remove(-1))
    print('13',liste)
    liste = chainList([i for i in range(10)])
    print('14',liste)
    print('retire du 4�me au 7�me')
    l1 = liste.remove(3,6)
    print('15',liste)
    print(l1)
    liste = chainList([i+10 for i in range(10)])
    print('16',liste)
    print('insertion avant le 3�me')
    liste.insert(2,l1)
    print('17',liste)
    print(liste.liste)
    print(liste[4])
    l = chainList(liste)
    print(l)
    l = chainList()
    print(l)
    l.append(5)
    print(l)
    l.remove(0)
    liste = chainList([i for i in range(10)])
    print('18',liste)
    print('2',liste[2])
    print('2,3,4 = ',liste[2:5])
    print('19',liste)
    print('2,3,4 = ',liste.liste[2:5])
    l=liste[2:5]
    print(l[0])
    l[0]=100
    print(l[0])
    print('l[0:1]=',l[0:1])
    print('20',liste)
    print(l)
    print(l.next(0))
    print(l.previous(0))
    l = chainList([cl(i) for i in range(5)])
    print(l)
    l1 = copy.deepcopy(l[1:3])
    l1.apply(True,cl.add,10)
    print(l1)
    l[1:3].apply(True,cl.add,10)
    print('l[1:3].apply(cl.add,10)',l)
    l1 = l[1:4]
    print(l1.first(),l1.last())
    l1 = l.ptr(1)
    print(l1.value)
    l1 = l.nextPtr(l1)
    print(l1.value)
    l1 = l.nextPtr(l1)
    print(l1.value)
    l1 = l.nextPtr(l1)
    print(l1.value)
    l1 = l.nextPtr(l1)
    print(l1)
    l1 = l[1:2]
    print('#################')
    print('l',l)
    print('l1',l1)
    print('l[1:2]',l[1:2])
    print('l[1]',l[1])
    l[1]=122
    print('l[1]=122',l)
    l[1]=l[2]
    print('l[1]=l[2]',l)
    l1[0] = l.next(0)
    print('l1',l1)
    l1[0]=122
    print('l1[0]=122',l)
    print('l',l)
    l1 = l[0:1]
    print('l-l1',l,l1)
    l1[0] = l.nextPtr(l1.ptr(0))
    print('l-l1',l,l1)
    l1[0]=cl(-122)
    print('l1[0]=-122',l)
    print(l.index(-122))
    print('#################')
    print('l',l)
    l.select(1,True)
    print('l',l)
    l.select(4,True)
    l.select(1,False)
    print('l',l)
    l.apply(True,cl.add,10)
    print('l',l)
    l.apply(False,cl.add,10)
    print('l',l)
    