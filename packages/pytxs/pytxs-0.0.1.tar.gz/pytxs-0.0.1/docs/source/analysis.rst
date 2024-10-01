Analyze the processed data
==========================

.. note::
        
   The following code snippets assumes that you have processed the 
   data using the procedure described earlier in the 
   :doc:`previous section <datared>`.

Subtract the heating signal
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    import txs

    ai = txs.get_ai(
        15e3,  # the incoming X-ray energy (in eV)
        0.15,  # the sample-to-detector distance (in m)
        center=(968, 969),  # the beam center on the detector (in pixels)
        detector='rayonix',  # the detector being used
        binning=(2, 2),  # the pixel binning being used
    )
