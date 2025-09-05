#Conserved dynamics (a.k.a. kawasaki dynamics)

import numpy as np
import matplotlib.pyplot as plt
import math as mt
import imageio
import os



L=16
J=1


ns=100000

s=np.zeros([L,L])
for i in range(L):
    
    for j in range(L):
       s[i][j]=np.random.choice([-1,1]) 
    


E=0
for i in range(-1,L-1):
    for j in range(-1,L-1):
        E=E-J*(s[i][j]*s[i+1][j]+s[i][j]*s[i-1][j]+s[i][j]*s[i][j+1]+s[i][j]*s[i][j-1]) 
    



def average(k ,s, E):

    i=np.random.randint(-1, high=L-1)
    j=np.random.randint(-1, high=L-1)
    
    i1=np.random.choice([i-1,i,i+1])
    
    if i1==i:
        j1=np.random.choice([j-1,j+1])
    else:
        j1=j
    
    if i1==L-1:
        i1=-1
    if j1==L-1:
        j1=-1
    
    
    E1=-J*(s[i][j]*s[i+1][j]+s[i][j]*s[i-1][j]+s[i][j]*s[i][j+1]+s[i][j]*s[i][j-1])
    E1f=-J*(s[i1][j1]*s[i+1][j]+s[i1][j1]*s[i-1][j]+s[i1][j1]*s[i][j+1]+s[i1][j1]*s[i][j-1])
    
    
    E2=-J*(s[i1][j1]*s[i1+1][j1]+s[i1][j1]*s[i1-1][j1]+s[i1][j1]*s[i1][j1+1]+s[i1][j1]*s[i1][j1-1])
    E2f=-J*(s[i][j]*s[i1+1][j1]+s[i][j]*s[i1-1][j1]+s[i][j]*s[i1][j1+1]+s[i][j]*s[i1][j1-1])
    
    dE=(E2f-E2) + (E1f-E1)
    
    pace=min(1,mt.exp(-k*dE))

    if np.random.random()<pace:
        s[i][j], s[i1][j1]=s[i1,j1], s[i][j]
        E=E+dE


    return E, s

k=0.8

plt.xlim(-2,L+1)
plt.ylim(-2,L+1)

plt.pcolormesh(np.arange(L), np.arange(L), s, cmap="gray", edgecolors="none")
plt.gca().set_aspect("equal")
plt.axis("off")  


plt.savefig('frame_{}.png'.format(0), dpi=100)

p=0
save=100
for t in range(1,ns+1):
    
    E, s =average(k,s,E)
    
    if t%save==0:
        p=p+1

        plt.clf()
        plt.xlim(-2,L+1)
        plt.ylim(-2,L+1)

        plt.pcolormesh(np.arange(L), np.arange(L), s, cmap="gray", edgecolors="none")
        plt.gca().set_aspect("equal")
        plt.axis("off")  
        #plt.show()
        
        plt.savefig('frame_' + str(int(p)) + '.png', dpi=100)
        
images=[]
n=p
for i in range(n+1):
    images.append(imageio.imread('frame_'+ str(i) + '.png'))

imageio.mimsave('kawasaki.gif', images, duration=1)

for i in range(n+1):
    os.remove('frame_' + str(i) + '.png')


print("GIF created successfully!")