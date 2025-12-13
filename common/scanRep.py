# -*- coding: latin-1
import os.path as osp
import os,time

def first(rep,suffixe=None):
    if not osp.isdir(rep): return None
    it=os.scandir(rep)
    if not suffixe:
        try:
            return next(it).name
        except StopIteration:
            return None
    suff1 = suffixe.lower()
    suff2 = suffixe.upper()
    try:
        while it:
            v = next(it).name
            vs = v[-len(suffixe):]
            if vs == suff1 or vs == suff2:
                return v
    except StopIteration:
        return None
        
def listeFichiers(rep,suf=None,bPath=True):
    #t0 = time.time()
    if not osp.isdir(rep): return []
    l=[]
    for e in os.scandir(rep):
        if not suf or e.name[-3:].upper() == suf:
            if bPath:
                l.append(osp.join(rep,e.name))
            else:
                l.append(e.name)
    #print 'dur�e scandir =',time.time()-t0
    return l
    
if __name__ == '__main__':
    import time,glob,os
    rep='C:/Users/marc/Documents/Dossiers personnel/Mes images/fghdgh'
#     for i in range(500):
#         print i
#         os.mkdir(rep+'/'+chr(97+i%26)+str(i)+'_rep')
#         open(rep+'/'+chr(97+i%26)+str(i)+'.JPG','w').close()
    t0=time.time()
    it=os.scandir(rep)
    try:
        while it:
            n = next(it).name
            if 'a0.JPG' == n:
                print('a0.JPG',time.time()-t0)
            if 'z4991.JPG' == n:
                print('z4991.JPG',time.time()-t0)
    except StopIteration:
        pass
    t1=time.time()
    print('scandir',t1-t0)#,[osp.basename(f) for f in l]
    t0=time.time()
    l= glob.glob(rep+'/*.*')
    print('a0.JPG' in l)
    print('z4991.JPG' in l)
    t1=time.time()
    print('glob',t1-t0)#,[osp.basename(f) for f in l]
    t0=time.time()
    l= os.listdir(rep)
    print('a0.JPG' in l)
    print('z4991.JPG' in l)
    t1=time.time()
    print('listdir',t1-t0)#,[osp.basename(f) for f in l]
    t0=time.time()
    print(first(rep,'JPG'))
    t1=time.time()
    print(t1-t0)
    rep='C:/Users/marc/Documents/Dossiers personnel/Mes images/fghdgh/a0_rep'
    print(first(rep))
    
    