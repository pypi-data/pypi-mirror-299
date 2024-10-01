Data reduction
==============

The data reduction methods in the :py:mod:`datared` allow to obtain
X-ray scattering difference patterns based on the result of the azimuthal
integration as obtained in the :doc:`previous section <import>`.

The data reduction proceeds as follows:

#. Identify each scattering pattern with its associated time delay.
#. Normalize each pattern based on the signal in a given q region.
#. Computes the differences by subtracting the reference signal to each pattern.
#. Computes the average of the differences for each time delay.
#. Optionally, apply a filter to discard outliers.


Performing data reduction 
^^^^^^^^^^^^^^^^^^^^^^^^^
Most of the work done by the :py:func:`datared.datared` function is automatic
and the function can be used as follows:

.. code:: python

    import txs

    # from previous section
    dset = ...
    azav = ...

    dred = txs.datared.datared(azav, "<your reference delay, e.g. '-20us'>")


Plot the result
^^^^^^^^^^^^^^^
Helper functions are available in :py:mod:`plot` to quickly plot the 
data. For the difference patterns, :py:func:`plot.plot_diffs` may be used.

.. code:: python

    txs.plot_diffs(dred)

Resulting in a `matplotlib <https://matplotlib.org/>`_ figure:

.. image:: ../fig/fig_plot_diffs.png
    :width: 600
    :alt: Difference patterns at various time delays


The resulting *dred* object
^^^^^^^^^^^^^^^^^^^^^^^^^^^
The *dred* object is a Python dictionary containing the reduced dataset as well
the content of the *azav* object generated in the `last section <import>`_

The import entries are:

* *q*, the scattering angle amplitudes vector.
* *t*, the time delays as strings.
* | *diff_av*, the averaged - and potentially filtered - difference patterns
  | for each time delay. The axes of the array are (q, time delays).
* *diff_err*, the errors associated with *diff_av*.


Additional options
^^^^^^^^^^^^^^^^^^
.. toctree::
    :maxdepth: 1

