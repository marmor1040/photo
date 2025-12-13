# -*- coding:utf-8 -*-
"""
Created on 19 juin 2011

@author: Bureau
"""
import matplotlib.pyplot as plt
plt.plot([1,2,3,6],[6,4,-2,7])
plt.ylabel('toto')
ap={}
ap['facecolor']='red'
ap['shrink']=0.05
plt.annotate('toto',xy=(2,1),xytext=(3,2),arrowprops=ap)
#plt.show()
plt.savefig('toto.pdf',format='pdf')
