#Adjacent Correlation Analysis on Time Series

The *adjacent correlation asnalysis* can also be used to construct phase
plot using time series

.. code:: ipython3

    import adjacent_correlation_analysis as aca
    import numpy as np
    import matplotlib.pyplot as plt
    
    # load the data
    
    x = np.load('tests/lorentz_x.npy')
    y = np.load('tests/lorentz_y.npy')

.. code:: ipython3

    # plotting the data
    plt.plot(x,y)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()




.. image:: output_2_0.png


.. code:: ipython3

    # using the adjacent correlation analysis
    
    aca.adjacent_correlation_plot(x, y,50,cmap='viridis_r',scale=30)
    plt.show()



.. image:: output_3_0.png




