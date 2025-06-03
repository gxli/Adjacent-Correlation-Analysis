#!/usr/bin/env python
# coding: utf-8

# #Adjacent Correlation Analysis on Time Series
# 
# The *adjacent correlation asnalysis* can also be used to construct phase plot using time series

# In[4]:


import adjacent_correlation_analysis as aca
import numpy as np
import matplotlib.pyplot as plt

# load the data

x = np.load('tests/lorentz_x.npy')
y = np.load('tests/lorentz_y.npy')


# In[5]:


# Plotting the data
plt.subplot(211)
plt.plot(x)
plt.subplot(212)
plt.plot(y)


# In[2]:


# plotting the data in the phase space
plt.plot(x,y)
plt.xlabel('x')
plt.ylabel('y')
plt.show()


# In[3]:


# using the adjacent correlation analysis

aca.adjacent_correlation_plot(x, y,50,cmap='viridis_r',scale=30)
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:




