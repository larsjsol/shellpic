Shellpic
========
-ASCII-art is so 2013.

Shellpic uses escape codes to display images in a terminal or irc-client.

Examples
--------
    .. image:: img/shell8.png
        :alt: Lenna displayed with a color depth of 8 bits.

Running ``shellpic <image>`` in a terminal that supports 256-colors
will get you something that looks like the image above.

If you happen to have a terminal that is capable of showing true
colors, you can use the ``--shell24``-switch to enable 24bit output.
It will look something like this:

    .. image:: img/shell24.png
        :alt: Lenna displayed with a color depth of 24 bits.

Shellpic can also be used with irc-clients. Run the script from your
client and use the ``--irc``-switch, the result will depend on the
client used. This is how it looks in xchat:

    .. image:: img/irc.png
        :alt: Lenna displayed in 16 colors by xchat.

Use the ``--animate`` (show the animation once, then exit) or
``--loop`` (animate and loop forever) to animate gifs.

    .. image:: img/imp_shell24.gif
        :alt: An animated gif shown in a terminal.

Install
-------
You should have PIL_ (>=1.1.7) or Pillow_ (>=1.0) installed. Shellpic is tested with Python 2.7.

.. _PIL: https://pypi.python.org/pypi/PIL
.. _Pillow: https://pypi.python.org/pypi/Pillow

If you have PIP installed:

.. code:: sh

   sudo pip install Shellpic

If you do not have PIP or want the bleeding edge version of Shellpic:

.. code:: sh

    # clone the repo
    git clone https://github.com/larsjsol/shellpic.git
    # install the package
    cd shellpic
    sudo python setup.py install

