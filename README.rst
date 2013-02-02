spectrometers
~~~~~~~~~~~~~~~

Spectrometers is a simple python API for working with
spectrometers/spectrophotometers. This was originally created as a gist to help
with development of `openSpectrometer`_. This doesn't do anything interesting
yet.

.. _`openSpectrometer`: http://openspectrometer.com/

Example usage
----------

here you go (Nanodrop code not yet actually implemented)

.. code-block:: python

    from spectrometers.devices import Nanodrop

    nanodrop = Nanodrop()

    wavelengths = nanodrop.capture()

    >>> wavelengths
    [0.500, 0.520]


pH determination

.. code-block:: python

    import spectrometers
    spectrometers.calculate_pH("./examples/pH_experiment_data/pH_experiment_config.txt")


    >>>acid lambda max: 445
    >>>acid absorbance: 0.260324
    >>>base absorbance: 0.0559506333333
    >>>buffer absorbance0.157026333333
    >>>base lambda max: 613
    >>>acid absorbance: 0.0142135
    >>>base absorbance: 0.563308666667
    >>>buffer absorbance0.282933333333

Choosing lambda max, and the results of the pH determination
.. image:: https://github.com/nmz787/python-spectrometers/blob/master/python-spectrometers.png

Install
----------
(pip archive not maintained by me, and does not reflect the current github code)

.. code-block:: bash

    sudo pip install spectrometers

or maybe you hate package managers,

.. code-block:: bash

    sudo python setup.py install

Testing
----------

.. code-block:: bash

    make test

Changelog
----------

* 0.0.3: get unit tests passing

* 0.0.2: really minor README tweaks

* 0.0.1: basic python module

License
----------

BSD
