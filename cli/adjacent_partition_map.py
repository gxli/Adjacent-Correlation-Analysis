#!/usr/bin/env python
from astropy.io import fits
# import adjacent_correlation
import numpy as np
import sys


def compute_stokes(ex, ey, normed=False):
    """A subroutine to compute the Stokes parameters from spin-2 vector component

    Args:
        ex (_type_): x component of the spin-2 vector 
        ey (_type_): y component of the spin-2 vector 
        normed (bool, optional): normalize the vectors according to the intensity. Defaults to True.
    Returns:
        the stokes i, q, u parameter
    """
    i = ex**2 + ey **2
    q = ex**2 - ey**2
    u = 2 * ex * ey
    if normed:
        return i/i,q/i, u/i
    else:
        return i, q, u
    
def compute_angle(i,q,u):
    """compute the polarization vector from the stokes i, q, u parameter 

    Args:
        i (_type_): _description_
        q (_type_): _description_
        u (_type_): _description_

    Returns:
        p, the polarization vector, and Ex, Ey, the x and y component of the polarization vector
    """
    p = np.sqrt(q**2 + u**2) / i
    angle = 1/2 * np.arctan2(u,q)
    return p, np.cos(angle), np.sin(angle)
    
def vector_norm(v,axis=0):
    return np.sqrt(np.array([i**2 for i in v]).sum(axis=axis))

def compute_correlation_coef(gx, gy):
    """compute the correlation coefficient between two measurements

    Args:
        gx (_type_): measurement 1
        gy (_type_): measurement 2
        xedges, yedges:  edges of the bins used by the histogram function.
        correlation (_type_): the correlation function to use

    Returns:
        the correlation value
    """
    # gx = np.array(np.gradient(xdata))
    # gy = np.array(np.gradient(ydata))
    
    # i, q, u = compute_stokes(gx,gy)
    
    # i_sum = i.sum(axis=0)
    # q_sum = q.sum(axis=0)
    # u_sum = u.sum(axis=0)
    
    # p, ex, ey = compute_angle(i_sum, q_sum, u_sum)
    gx2 = gx**2
    gy2 = gy**2
    gxgy = gx*gy
         
    gx2_value = np.sqrt(gx2.sum(axis=0))
    gy2_value = np.sqrt(gy2.sum(axis=0))
    gxgy_value = gxgy.sum(axis=0)
    
    return gxgy_value / (gx2_value * gy2_value)


def compute_correlation_map(xdata, ydata):
    """compute the correlation value between two measurements

    Args:
        xdata (_type_): measurement 1
        ydata (_type_): measurement 2
        xedges, yedges:  edges of the bins used by the histogram function.
        correlation (_type_): the correlation function to use

    Returns:
        the correlation value
    """
    
    
    gx = np.array(np.gradient(xdata))
    gy = np.array(np.gradient(ydata))
    
    i, q, u = compute_stokes(gx,gy)
    
    i_sum = i.sum(axis=0)
    q_sum = q.sum(axis=0)
    u_sum = u.sum(axis=0)
    
    corr_coef = compute_correlation_coef(gx, gy)
    
    p, ex, ey = compute_angle(i_sum, q_sum, u_sum)
    
    # stdx = np.nanstd(gx.flatten())
    # stdy = np.nanstd(gy.flatten())
    
    
    gradients = zip(gx,gy)


    return p, np.arctan2(ey,ex), ey/ex, corr_coef



    

if __name__ == '__main__': 
    
    # correlation_data = './result.npy'
    # correlations = np.load(correlation_data, allow_pickle=True).item()
    # xedges = correlations['xedges']
    # yedges = correlations['yedges']
    # Ex = correlations['Ex']
    # Ey = correlations['Ey']
    # f1 = sys.argv[1]
    # f2 = sys.argv[2]
    f1 = sys.argv[1]
    f2 = sys.argv[2]
    
    h1 = fits.open(f1)
    h2 = fits.open(f2)
    
    d1 = h1[0].data
    d2 = h2[0].data
    
    if d1 is None:
        d1 = h1[1].data
        d2 = h2[1].data
    try:
        print(sys.argv[3])
        if float(sys.argv[3]) > 0:
            Logdata1=True
        else:
            Logdata1=False        
    except:
        Logdata1 = False
        
    if Logdata1:    
        ld1 = np.log10(d1)
        # ld1[np.isnan(ld1)]=1
        # ld1[np.isinf(ld1)]=1
        # ld2[np.isnan(ld2)]=1
        # ld2[np.isinf(ld2)]=1
    else:
        ld1 = d1
     
        
    try:
        print(sys.argv[4])
        if float(sys.argv[4]) > 0:
            Logdata2=True
        else:
            Logdata2=False        
    except:
        Logdata2 = False
        
    if Logdata2:    
        ld2 = np.log10(d2)
        # ld1[np.isnan(ld1)]=1
        # ld1[np.isinf(ld1)]=1
        # ld2[np.isnan(ld2)]=1
        # ld2[np.isinf(ld2)]=1
    else:
        ld2 = d2
            


    
    
    
    correlation, angle, ratio, corre_coef = compute_correlation_map(ld1, ld2)
    
    
    nh = fits.PrimaryHDU(correlation)
    
    nh.writeto(f1+ '_' + f2 +'_adj_correlation.fits', overwrite=True)
    
    nh = fits.PrimaryHDU(angle)
    
    nh.writeto(f1+ '_' + f2 +'_adj_angle.fits', overwrite=True)
    
    # sangle = angle.copy()
    # positions = sangle < 0
    # sangle[positions] = sangle[positions] + np.pi
    # nh = fits.PrimaryHDU(sangle)
    
    # nh.writeto(f1+ '_' + f2 +'_angle_shift_90.fits', overwrite=True)
    
    
    
    # nh = fits.PrimaryHDU(ratio)
    
    # nh.writeto(f1+ '_' + f2 +'_ratio.fits', overwrite=True)
    
    nh = fits.PrimaryHDU(corre_coef)
    nh.writeto(f1+ '_' + f2 +'_correlation_coef.fits', overwrite=True)