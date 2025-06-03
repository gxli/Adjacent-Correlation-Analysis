#!/usr/bin/env python
# coding: utf-8

# # Adjacent Correlation Mapping
# 
# This example shows how to compute and visualize the adjacent correlation map. 
# 

# In[1]:


import adjacent_correlation_analysis as aca
import numpy as np
import matplotlib.pyplot as plt


# Load the data

# In[2]:


data_temp = np.load('./tests/NOAA_temp.npy')
data_perc = np.load('./tests/NOAA_perc.npy')
data_log_perc = np.log10(data_perc)


# Plot the data

# In[3]:


plt.figure(dpi=100)
plt.subplot(211)
plt.imshow(data_temp)
plt.title('Temperature')
plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
plt.tick_params(axis='y', which='both', bottom=False, top=False, labelbottom=False)

plt.subplot(212)
plt.imshow(data_log_perc)
plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
plt.tick_params(axis='y', which='both', bottom=False, top=False, labelbottom=False)
plt.title('Loig(Perc)')


# Compute correlation maps:

# In[4]:


p, angle, coef, i = aca.compute_correlation_map(data_temp, data_log_perc)


# In[5]:


plt.figure(dpi=200)


plt.subplot(211)
plt.imshow(p)
plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
plt.tick_params(axis='y', which='both', bottom=False, top=False, labelbottom=False)
plt.title('correlation degree')
plt.colorbar()

plt.subplot(212)
plt.imshow(angle, cmap='seismic')
plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
plt.tick_params(axis='y', which='both', bottom=False, top=False, labelbottom=False)
plt.title('correlation angle')
plt.colorbar()


plt.figure(dpi=200)


plt.subplot(211)
plt.imshow(coef, cmap='gray_r',alpha=0.5)
plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
plt.tick_params(axis='y', which='both', bottom=False, top=False, labelbottom=False)
plt.title('correlation coefficient')
plt.colorbar()

plt.subplot(212)
plt.imshow(coef,cmap='gray_r',alpha=0.5)
plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
plt.tick_params(axis='y', which='both', bottom=False, top=False, labelbottom=False)
plt.title('gradient magintude')
plt.colorbar()



# In[6]:


angle.shape


# In[ ]:





# In[ ]:




