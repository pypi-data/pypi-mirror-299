=======
CERBERE
=======

The IFREMER / CERSAT geospatial processing tool.

See online documentation at: http://cerbere.readthedocs.org

---------------
 Development
---------------

Create conda env
=================

.. code-block:: shell

    conda creaate -n cerbere -c conda-forge python=3.7 pygrib netcdf4 pyproj xarray


Install poetry
=================

.. code-block:: shell

    pip install poetry poetry-dynamic-versioning poetry2conda
    poetry --version
    poetry config repositories.nexus-public-release https://nexus-test.ifremer.fr/repository/hosted-pypi-public-release/


retrieve and install project
=============================

.. code-block:: shell

    git clone https://gitlab.ifremer.fr/cerbere/cerbere.git
    poetry install -v --no-root


List dependencies
==================

.. code-block:: shell

    poetry show --tree

---------------
build
---------------

wheel
==================

.. code-block:: shell

    poetry build --format wheel
    poetry publish -r nexus-public-release -u nexus-ci -p w2bH2NjgFmQnzVk3


conda
==================

.. code-block:: shell

    mkdir -p dist/conda
    conda build assets/conda -c conda-forge --output-folder dist/conda


documentation
==================

.. code-block:: shell

    poetry run sphinx-build -b html docs public
