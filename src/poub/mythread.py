'''
Created on 8 juin 2011

@author: to07184
'''
import threading
import time

class Affiche(threading.Thread):
    def __init__(self, nom = ''):
        threading.Thread.__init__(self)
        self.nom = nom
        self._stopevent = threading.Event( )
        self._waitevent = threading.Event( )
        self.__lock=threading.Lock()
        print(dir(self.__lock),self.__lock.locked()))

    def run(self):
        i = 0
        while not self._stopevent.isSet():
            if self.__lock.locked():
                self._stopevent.wait(.5)
            else:
                print(self.nom, i)
                i += 1
                self._stopevent.wait(0.2)
                print(self.nom, i,'ok')
#        while not self._stopevent.isSet():
#            while self._waitevent.isSet():
#                self._waitevent.wait(1)
#            else:
#                print self.nom, i
#                i += 1
#                self._stopevent.wait(0.2)
#                print self.nom, i,'ok'
        print("le thread "+self.nom +" s'est termine proprement"))
    def stop(self):
        self._stopevent.set( )  
    def wait(self):
        self.__lock.acquire()
        #self._waitevent.set( )
    def rerun(self):
        self.__lock.release()
        #self._waitevent.clear( )
        
        
a = Affiche('Thread A')
a.start()
time.sleep(3)
v=0
print('wait')
a.wait()
print('debut calcul')
t=time.time()
for i in range(10000000):
    v+=i
print('fin calcul',time.time()-t))
a.rerun()
time.sleep(3)
    
a._Thread__stop()
