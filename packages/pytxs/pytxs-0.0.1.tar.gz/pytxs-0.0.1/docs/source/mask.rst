Using a mask
============


Create the mask with pyFAI
^^^^^^^^^^^^^^^^^^^^^^^^^^
The mask can be created using 
`pyFAI-drawmask <https://pyfai.readthedocs.io/en/master/man/pyFAI-drawmask.html>`_ 
by loading a image HDF5 file using:

.. code:: bash

    # from the experiment 'raw' folder
    pyFAI-drawmask sample/sample_0001/scan0001/<detector_name>_0000.h5

Use the draw tools and/or the threshold to draw your mask and then save it.


Apply the mask in txs
^^^^^^^^^^^^^^^^^^^^^
The mask can be used in :py:func:`azav.integrate1d_dataset` using:

.. code:: python

    import txs


    mask = txs.utils.load_mask("<your_mask_name>.edf")

    txs.azav.integrate1d_dataset(
        ...,  # the function arguments
        mask=mask,
    )

    # similarly with the live analysis
    txs.live.ana(
        ...,  # the function arguments
        mask=mask, 
    )