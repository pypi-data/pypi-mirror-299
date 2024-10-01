txs
===
Process and analyze time-resolved X-ray scattering data.

.. image:: ../fig/fig_setup_beamline.png
    :width: 600
    :alt: TR-XSS beamline setup for proteins

Installation:
-------------

Unix and Windows
^^^^^^^^^^^^^^^^

For installation within your python framework, use:

.. code:: bash

    pip install [--upgrade --force-reinstall --no-deps] git+https://gitlab.esrf.fr/levantin/txs.git


Getting started
---------------
The txs Python package provides functions to process and analyze time-resolved X-ray scattering data.

On the ID09 beamline at the ESRF, the current data are recorded using `BLISS <https://www.esrf.fr/BLISS>`_. These data can have a specific directory hierarchy:

| **<experiment_folder>**
|     └── **raw**
|         ├── **<sample_01>**
|         │   ├── *sample_01.h5*
|         │   ├── **sample_01_0001**
|         │   │   ├── *sample_01_0001.h5*
|         │   │   ├── **scan0001**
|         │   │   │    ├── *<detector_name>_0000.h5*
|         │   │   │    └── *<detector_name>_0001.h5*
|         │   │   │ 
|         │   │   └── **scan0002**
|         │   │
|         │   ├── **sample_01_0002**
|         │   └── **sample_01_0003**
|         │ 
|         └── **<sample_02>**

The .h5 file in bold in the one of interest to access the data of a BLISS *dataset*. It can be opened using:

.. code:: python

    import txs
    import matplotlib.pyplot as plt
 
    dset = txs.BlissDataset("sample_0001.h5")  # the HDF5 file of the BLISS dataset
    
    dset.scans  # -> ['1.1', '1.2', '2.1', '2.2', '3.1', '3.2', '4.1', '4.2', '5.1', '5.2']
    
    # plot the 5th image of scan 2.2
    plt.imshow(dset["2.2"][4], vmin=50, vmax=5000)

The data processing requires to create an azimuthal integrator object (might be automatic in a future version):

.. code:: python

    ai = txs.get_ai(
        15.3,  # X-ray energy in keV
        0.15,  # sample to detector distance in m
        detector='rayonix',
        center=(969, 968),  # beam center on the detector (in pixels)
        binning=(2, 2),  # detector pixel binning
    )

The azimuthal and data reduction (calculation of difference patterns) is then performed:

.. code:: python

    azav = txs.int1d_dset(
        dset["2.2"].folder,  # the scan folder containing the images
        ai,
        method='csr_ocl',  # faster, multi-threaded integration
        sample_thickness=1.2e-3,  # sample thickness in m (for transmission)
        sample_material='H2O'
    )
 
    azav.keys()  # -> dict_keys(['npt', 'method', 'unit', ..., 'q', 'i', ...])
    
    red = txs.dred(
        azav,
        ref_delay='auto',  # the reference delay which will be subtracted from laser-exposed images.
        norm=(2.1, 2.2),  # normalize the patterns by the integral over the given a region before subtraction
        red_chi2_max='auto'  # filter out the data that diverge from the average difference curves by more than 2 sigmas
    )

Different plotting methods are also available:

.. code:: python

    # to plot the absolute patterns for the 10 ms time delay
    txs.plot_abs(red, ["10ms"])
    
    # to plot the difference patterns
    txs.plot_diffs(red)

During your experiment, a live analysis is also available (function arguments are similar as the ones from 'txs.int1d_dset' and 'txs.dred'):

.. code:: python

    txs.live.ana(
        "sample/sample_0001/scan0001",
        "-20us",  # reference delay
        ai=ai,
        qnorm=(2.1, 2.2),
        method='csr_ocl',  # faster, multi-threaded integration
        sample_thickness=1.2e-3,  # sample thickness in m (for transmission)
        sample_material='H2O',
        plot=True,  # plot the difference patterns
        track_abs=True,  # plot the absolute patterns
        red_chi2_max='auto',  # filter out the data that diverge from the average difference curves by more than 2 sigmas
    )


Documentation
-------------
.. toctree::
    :maxdepth: 1

    import
    datared
    analysis
    reference
    license
    help


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
