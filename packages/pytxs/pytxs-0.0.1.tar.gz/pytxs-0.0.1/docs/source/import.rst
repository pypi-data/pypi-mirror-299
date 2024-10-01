Import and inspect data
=======================


Creating an azimuthal integrator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The txs software makes use of 
`pyFAI <https://pyfai.readthedocs.io/en/v2023.1/>`_ 
to perform the azimuthal integration on the images.

Hence, the first step to process your data is to create a so-called
`AzimuthalIntegrator <https://pyfai.readthedocs.io/en/v2023.1/api/pyFAI.html#module-pyFAI.azimuthalIntegrator>`_ 
object.

The azimuthal integrator takes information about the detector and the
geometry of the setup to compute the position of the pixels corresponding
to the same scattering angle.

In txs, the :py:func:`utils.get_ai` helper function is provided to ease 
the creation of this object:

.. code:: python

    import txs

    ai = txs.get_ai(
        15e3,  # the incoming X-ray energy (in eV)
        0.15,  # the sample-to-detector distance (in m)
        center=(968, 969),  # the beam center on the detector (in pixels)
        detector='rayonix',  # the detector being used
        binning=(2, 2),  # the pixel binning being used
    )

.. note::

    The creation of the AzimuthalIntegrator object is expected to be 
    automatized in the future on ID09 at the ESRF by using the metadata 
    that are recorded during the experiment.


Using .edf files (old setup)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Prior to the installation of BLISS software at the ESRF, the detector 
images were recorded in the .edf file format.

The raw images can be visualized using the 
`FabIO viewer <https://www.silx.org/doc/fabio/latest/man/fabio_viewer.html>`_.

To perform the **azimuthal integration** for these experiments,
the :py:func:`azav.integrate1d_dataset` function is 
to be used by providing the data folder as well as the file extension
as such:

.. code:: python

    azav = txs.int1d_dset(
        "<data_folder>",  # the scan folder containing the images
        ai,  # the previously created AzimuthalIntegrator object
        extension="edf",
        method='csr_ocl',  # faster, multi-threaded integration
        sample_thickness=1.2e-3,  # sample thickness in m (for transmission)
        sample_material='H2O'
    )


Using BLISS dataset
^^^^^^^^^^^^^^^^^^^
The folder hierarchy in BLISS and associated HDF5 files makes possible to
access the data in multiple ways. 
The recommanded method is to import the 'dataset' HDF5 file using the 
:py:class:`datasets.BlissDataset` class:

.. code:: python

    dset = txs.BlissDataset(
        "path_to/<sample_name>_<dataset_number>.h5"
    )

The resulting *dset* object is an iterator over the scans and the images which
contains also metadata related to the experiment:

.. code:: python

    dset.scans  # -> ['1.1', '1.2', '2.1', '3.1',...]
    
    # to obtain the metadata for scans '1.2'
    dset.metdata(1, 2)

Hence, for a given scan '2.1', the images can be accessed and plotted 
as follows:

.. code:: python

    import matplotlib.pyplot as plt

    plt.imshow(dset["2.1"][0])  # plot the first image
    plt.imshow(dset["2.1"][4])  # plot the fifth's image

The **azimuthal integration** is done similarly as above by using the 
:py:func:`azav.integrate1d_dataset` function:

.. code:: python

    azav = txs.azav.integrate1d_dataset(
        dset["2.1"].folder,  # the folder of scan 2.1 containing the images
        extension='h5',  # default value, so it can be ommited
        ai,  # the previously created AzimuthalIntegrator object
        method='csr_ocl',  # faster, multi-threaded integration
        sample_thickness=1.2e-3,  # sample thickness in m (for transmission)
        sample_material='H2O'
    )


The resulting *azav* object
^^^^^^^^^^^^^^^^^^^^^^^^^^^
The *azav* object obtained above is a Python dictionary that contains
the 1D scattering patterns with their associated errors as well as 
other information about the data and the methods used to process them.

The scattering vector magnitude q, the intensities and errors are 
contained in the `q`, `i` and `e` keys of the *azav* dictionary, respectively.


Plotting possibilities
^^^^^^^^^^^^^^^^^^^^^^
Some plotting functions are available to quickly plot useful information.
For the azimuthal integration, the function :py:func:`plot.plot_azim_regroup`
allows to view the projection map used by the azimuthal integrator:

.. image:: ../fig/fig_txs_plot_azim_regroup.png
    :width: 600
    :alt: projection map of the azimuthal integrator


Additional options
^^^^^^^^^^^^^^^^^^
.. toctree::
    :maxdepth: 1

    mask