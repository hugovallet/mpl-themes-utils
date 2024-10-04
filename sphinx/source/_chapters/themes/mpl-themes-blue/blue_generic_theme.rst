Blue Generic Theme
==================

Usage
-----

>>> from mpl_themes_utils.themes import set_theme
>>> set_theme("mpl-themes-blue")

Theme features
--------------

.. image:: mpl-themes-blue_theme_0.png

.. image:: mpl-themes-blue_theme_1.png

.. image:: mpl-themes-blue_theme_2.png

.. image:: mpl-themes-blue_theme_3.png

.. image:: mpl-themes-blue_theme_4.png

Examples
--------

.. code-block:: python

    import seaborn as sns
    df = sns.load_dataset("penguins")
    sns.pairplot(df, hue="species")

.. image:: mpl-themes-blue_scatter.png
