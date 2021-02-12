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
CG=7 # number of CG (coarse-grained) pixels
start=9999 # start step
end=19999 # end step
increase=50 # spacing between consecutive steps - this is related to what originally done with A_t_cg.{}.txt and all_conductances.txt. I cannot sample more frequently than every "increase" MC steps
skip=1 #in case you want to read only every "skip" steps (i.e. every skip*increase) within all_conductances.txt. Default value: skip=1.
timesteps=int((end-start)/(increase*skip)) # total number of available timeframes

time_series=np.empty([timesteps,CG])
corr_matrix=np.zeros([CG,CG])
tt=0

paths=('1_pre/', '15/', '1_post/')

if flag==0:
	for path in paths:
		tt=0
		print(path)
		for t in range(start,end,int(increase*skip)):
			for i in range(0,CG):
				for j in range (0,CG):
					r=np.loadtxt(path+'A_t_cg.{}.txt'.format(t),unpack=True,usecols=(0,))
				time_series[tt]=r
			tt+=1

else:
	for path in paths:
		tt=0
		print(path)
		for t in range(start,end,int(increase*skip)):
			for i in range(0,CG):
				for j in range (0,CG):
					r=np.loadtxt(path+'all_conductances.txt',unpack=True,usecols=(0,),skiprows=CG*tt*skip,max_rows=CG)
				time_series[tt]=r
			tt+=1

		A=np.corrcoef(time_series.T)
	
		#plot
		plt.clf()
		plt.rcParams['xtick.labelsize']=18
		plt.rcParams['ytick.labelsize']=18
		color_map = plt.cm.get_cmap('coolwarm')
		reversed_color_map = color_map.reversed()
		plt.xlabel("Pixels",fontsize=15)
		plt.ylabel("Pixels",fontsize=15)
		plt.imshow(A,cmap=reversed_color_map)
		plt.clim(-1,1)
		cbar = plt.colorbar()
		for t in cbar.ax.get_yticklabels():
     			t.set_fontsize(20)
		plt.savefig(path+'corr_mat.png',dpi=300)
