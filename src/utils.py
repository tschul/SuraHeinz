"""
all nuclear functions that are better suited in a compositional way
out of the rigid hierarchy of classes
"""
import logging as l


def perform_action(iteration, param, func, *args):
    if not param > 0:
        return
    if iteration % param != 0:
        return
    try:
        func(*args)
    except Exception, e:
        l.critical(e)
