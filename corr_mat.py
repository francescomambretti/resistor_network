# Created by Francesco Mambretti, 08/02/2021
# Modified 10/02/2021

import numpy as np
import string
import matplotlib.pyplot as plt
import sys

# input arguments

if (sys.argv[1]=='0' or sys.argv[1]=='1'):
	flag=sys.argv[1] # 0--> use 'A_t_cg.{}.txt' files ----- 1 --> use 'all_conductances.txt'
else:
	print("error!",sys.argv[1])
	sys.exit()

# parameters
CG=6 # number of CG (coarse-grained) pixels
start=9999 # start step
end=19999 # end step
increase=50 # spacing between consecutive steps
timesteps=int((end-start)/increase) # number of timeframes

time_series=np.empty([timesteps,CG])
corr_matrix=np.zeros([CG,CG])
tt=0

paths=('4_pre/', '15/', '4_post/')

if flag==0:
	for path in paths:
		tt=0
		print(path)
		for t in range(start,end,increase):
			for i in range(0,CG):
				for j in range (0,CG):
					r=np.loadtxt(path+'A_t_cg.{}.txt'.format(t),unpack=True,usecols=(0,))
				time_series[tt]=r
			tt+=1

else:
	for path in paths:
		tt=0
		print(path)
		for t in range(start,end,increase):
			for i in range(0,CG):
				for j in range (0,CG):
					r=np.loadtxt(path+'all_conductances.txt',unpack=True,usecols=(0,),skiprows=CG*tt*increase,max_rows=CG)
				time_series[tt]=r
			tt+=1

		A=np.corrcoef(time_series.T)
	
		#plot
		plt.clf()
		color_map = plt.cm.get_cmap('coolwarm')
		reversed_color_map = color_map.reversed()
		plt.xlabel("Pixels",fontsize=15)
		plt.ylabel("Pixels",fontsize=15)
		plt.imshow(A,cmap=reversed_color_map)
		plt.clim(-1,1)
		plt.colorbar()
		plt.savefig(path+'corr_mat.png',dpi=300)
