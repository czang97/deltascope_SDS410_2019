import os
import numpy as np
import h5py
import skimage.io as io
import matplotlib.pyplot as plt
import time
import itertools as it
import matplotlib as mpl
import multiprocessing as mp
from functools import partial
import statsmodels.formula.api as smf
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

class brain:

	def __init__(self,filepath):
		'''Read raw data'''

		self.raw_data = self.read_data(filepath)

	def read_data(self,filepath):
		'''Reads 3D data from file and selects appropriate channel'''

		#Read h5 file and extract probability data
		f = h5py.File(filepath,'r')
		c1 = np.array(f.get('exported_data')[:,:,:,0])
		c2 = np.array(f.get('exported_data')[:,:,:,1])

		#Figure out which channels has more zeros and therefore is background
		if np.count_nonzero(c1<0.1) > np.count_nonzero(c1>0.9):
			return(c1)
		else:
			return(c2)

	def show_plane(dimension,plane):
		'''Shows specified plane'''

		if dimension=='x':
			data = sample.raw_data[:,:,plane]
		elif dimension=='y':
			data = sample.raw_data[:,plane,:]
		elif dimension=='z':
			data = sample.raw_data[plane,:,:]
		else:
			print('Invalid dimension specified, try "x","y","z"')

		fig,ax = plt.subplots()
		cax = ax.imshow(sample.raw_data[:,:,300],cmap='plasma')
		fig.colorbar(cax)

	def create_dataframe(self):
		'''Creates a pandas dataframe containing the x,y,z and signal/probability value 
		for each point in the :py:attr:`brain.raw_data` array'''

		dim = self.raw_data.shape
		xyz = np.zeros((dim[0],dim[1],dim[2],4))

		#Generate array with xyz values for each point
		for x in range(dim[2]):

			xyz[:,:,x,2] = x
			xyz[:,:,x,3] = self.raw_data[:,:,x]

			zindex = np.arange(0,dim[0],1)
			yindex = np.arange(0,dim[1],1)
			gy,gz = np.meshgrid(yindex,zindex)

			xyz[:,:,x,0] = gz
			xyz[:,:,x,1] = gy

		flat = np.reshape(xyz,(-1,4))

		#Create dataframe of points
		self.df = pd.DataFrame({'x':flat[:,2],'y':flat[:,1],'z':flat[:,0],'value':flat[:,3]})

	def fit_model(self,threshold):
		'''Calculates the mathematical model of the data'''

		self.threshold = threshold
		self.df_thresh = self.df[self.df.value > self.threshold]

		#Create xyz arrays for range of data
		x = np.linspace(self.df_thresh.x.min(),self.df_thresh.x.max())
		y = np.linspace(self.df_thresh.y.min(),self.df_thresh.y.max())
		z = np.linspace(self.df_thresh.z.min(),self.df_thresh.z.max())

		#Identify flat plane
		flat_model = smf.ols(formula='y ~ x + z',data=self.df_thresh).fit()
		xx,zz = np.meshgrid(x,z)
		Y = flat_model.params[0] + flat_model.params[1]*xx + flat_model.params[2]*zz
		self.f_plane = plane(flat_model,xx,Y,zz)

		#Identify parabolic plane
		para_model = smf.ols(formula='z ~ y + x + I(x**2)',data=self.df_thresh).fit()
		xx,yy = np.meshgrid(x,y)
		Z = para_model.params[0] + para_model.params[1]*yy + para_model.params[2]*xx + para_model.params[3]*(xx**2)
		self.p_plane = plane(para_model,xx,yy,Z)

		#Find intersection
		model = {
		'a' : para_model.params[3],
		'b' : para_model.params[2],
		'c' : para_model.params[1],
		'd' : para_model.params[0],
		'e' : flat_model.params[1],
		'f' : flat_model.params[2],
		'g' : flat_model.params[0]
		}

		model['a_prime'] = (model['a']*model['f']) / (1 - model['c']*model['f'])
		model['b_prime'] = (model['e'] + model['b']*model['f']) / (1 - model['c']*model['f'])
		model['c_prime'] = (model['g'] + model['d']*model['f']) / (1 - model['c']*model['f'])

		#Parametric equation in terms of t
		t = np.arange(0,1000)
		x_line = t
		y_line = model['a_prime']*(t**2) + model['b_prime']*t + model['c_prime']
		z_line = (model['a'] + model['c']*model['a_prime'])*(t**2) + (model['b'] + model['c']*model['b_prime'])*t + model['c']*model['c_prime'] + model['d']

		self.parabola = math_model(model,x_line,y_line,z_line)

	def plot_model(self,sample_frac=0.5,cmap=plt.cm.Greys):
		'''Plot two planes, line model, and percentage of points'''

		subset = self.df_thresh.sample(frac=sample_frac)

		fig = plt.figure()
		ax = Axes3D(fig)

		ax.scatter(subset['x'],subset['y'],subset['z'],alpha=0.1,s=0.1)

		ax.plot_surface(self.f_plane.xx,self.f_plane.yy,self.f_plane.zz,cmap=cmap,alpha=0.6,linewidth=0)
		ax.plot_surface(self.p_plane.xx,self.p_plane.yy,self.p_plane.zz,cmap=cmap,alpha=0.6,linewidth=0)

		ax.plot(self.parabola.x[:600],self.parabola.y[:600],self.parabola.z[:600])

		plt.show()


class plane:
	'''Class to contain attributes and data associated with a plane'''

	def __init__(self,model,xx,yy,zz):
		'''Save global variables'''

		self.model = model
		self.xx = xx
		self.yy = yy
		self.zz = zz

class math_model:
	'''Class to contain attribues and data associated with math model'''

	def __init__(self,coef,x,y,z):

		self.coef = coef
		self.x = x
		self.y = y
		self.z = z