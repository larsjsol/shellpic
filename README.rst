Shellpic
========
-ASCII-art is so 2013.

Shellpic uses escape codes to display images in a terminal or irc-client.

Examples
--------
    .. image:: img/shell8.png
        :alt: Lenna displayed with a color depth of 8 bits.
Running 'shellpic <image>' in a terminal that supports 256-colors
will get you something that looks like the image above.

If you happen to have a terminal that is capable of showing true colors,
you can use the '--shell24'-switch to enable 24bit outout. It will look something like this:
    .. image:: img/shell24.png
        :alt: Lenna displayed with a color depth of 24 bits.

Shellpic can also be used with irc-clients. Run the script from your client and use the '--irc'-switch, the result will depend on the client used. This is how it looks in xchat:

    .. image:: img/irc.png
        :alt: Lenna displayed in 16 colors by xchat.


Install
-------
You should have PIL installed. Shellpic is tested with Python 2.7.

If you have PIP installed: 'sudo pip install Shellpic'


If you do not have PIP or want the bleeding edge version of Shellpic::

    # clone the repo
    git clone https://github.com/larsjsol/shellpic.git
    # install the package
    cd shellpic
    sudo python setup.py install

