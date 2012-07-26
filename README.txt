===========
mindcontrol
===========

mindcontrol provides an api that allows python programs to capture data that
is emitted by the NeuroSky MindWave headsets. It uses a socket to connect to
the ThinkGearConnector application that acts as a server for the headset data::

    #!/usr/bin/env python

    from mindcontrol.userbrain import Brain
    from time import sleep

    SLEEP_TIME = 5 # seconds
    CONCENTRATE_TIME = 5 # seconds
    my_brain = Brain()
    while not my_brain.isConnected():
        print 'Not connected to brain yet. Will try again in %d seconds' % SLEEP_TIME
        sleep(SLEEP_TIME)
    # brain is now connected, get some stuff
    print 'Concentrate really hard for the next %d seconds!' % CONCENTRATE_TIME
    # sample once each second
    conc_vals = []
    for idx in xrange(CONCENTRATE_TIME):
        conc_vals.append(my_brain.getProperty('attention'))
        sleep(1)
    print 'Your recorded concentration values were:\n\t[%s]' % ', '.join([str(x) for x in conc_vals])




collaboration
=========

This project is GPL licensed so do whatever you want with the code. This module is currently being source controlled
on GitHub, so if you want to check out the project you can find it here: https://github.com/georgeBoole/mindcontrol.
This module is mostly experimental at the moment, but expect more development soon.