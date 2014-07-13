Shellpic
========
-ASCII-art is so 2013.

Shellpic uses escape codes to display images in a terminal, IRC or NUTS client.

Examples
--------
    .. image:: https://raw.github.com/larsjsol/shellpic/master/img/shell8.png
        :alt: Lenna displayed with a color depth of 8 bits.

Running ``shellpic <image>`` in a terminal that supports 256-colors
will get you something that looks like the image above.

If you happen to have a terminal that is capable of showing true
colors, you can use the ``--shell24``-switch to enable 24bit output.
It will look something like this:

    .. image:: https://raw.github.com/larsjsol/shellpic/master/img/shell24.png
        :alt: Lenna displayed with a color depth of 24 bits.

Shellpic can also be used with irc-clients. Run the script from your
client and use the ``--irc``-switch, the result will depend on the
client used. This is how it looks in xchat:

    .. image:: https://raw.github.com/larsjsol/shellpic/master/img/irc.png
        :alt: Lenna displayed in 16 colors by xchat.

The ``--nuts``-switch will do the same, but for NUTS talkers. This is how it looks
in konsole:

    .. image:: https://raw.github.com/larsjsol/shellpic/master/img/nuts.png
        :alt: Farnsworth and imp displayed in 16 colors in a NUTS talker

The ``--tinymux``-switch will also do that, generating 256 color images for 
TinyMUX servers.

Use the ``--animate`` (show the animation once, then exit) or
``--loop`` (animate and loop forever) to animate gifs. There is a
noticable difference between between terminals of how smooth 
the animation looks. KDE's ``konsole`` seems to handle it well.

    .. image:: https://raw.github.com/larsjsol/shellpic/master/img/imp_shell24.gif
        :alt: An animated gif shown in a terminal.

Installation
------------
You should have Pillow_ (>=1.0) installed. Shellpic works with
Python 2.6, 2.7, 3.3 and 3.4. It will not work with Python 2.5 or 3.2.

.. _Pillow: https://pypi.python.org/pypi/Pillow

If you have PIP installed:

.. code:: sh

   sudo pip install Shellpic

If you do not have PIP or want the bleeding edge version of Shellpic:

.. code:: sh

    # clone the repo
    git clone https://github.com/larsjsol/shellpic.git
    # optional - run tests
    ./shellpic/tests/run_tests.sh
    # install the package
    cd shellpic
    sudo python setup.py install

Changelog
---------
See `CHANGES.rst <https://github.com/larsjsol/shellpic/blob/master/CHANGES.rst>`_
