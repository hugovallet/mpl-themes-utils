Generic Green Theme
===================

Usage
-----

>>> from  mpl_themes_utils.themes import set_theme
>>> set_theme("mpl-themes-green")

Theme features
--------------

.. image:: mpl-themes-green_theme_0.png

.. image:: mpl-themes-green_theme_1.png

.. image:: mpl-themes-green_theme_2.png

.. image:: mpl-themes-green_theme_3.png

.. image:: mpl-themes-green_theme_4.png

Examples
--------

.. code-block:: python

    import seaborn as sns
    df = sns.load_dataset("penguins")
    sns.pairplot(df, hue="species")

.. image:: mpl-themes-green_scatter.png
