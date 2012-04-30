# -*- coding: utf-8 -*-
"""
    gtasks.config
    ~~~~~~~~~~~~~

    :copyright: (c) 2012 by Daisuke Igarashi.
    :license: BSD, see LICENSE for more details.
"""
import imp
import errno

class Config(object):
    """
    """

    def from_pyfile(self, filename, silent=False):
        """
        :param filename: file name
        :param silent:
        """
        d = imp.new_module('config')
        d.__file__ = filename
        try:
            execfile(filename, d.__dict__)
            self.from_object(d)
        except IOError, e:
            if silent and e.errno in (errno.ENOENT, errno.EISDIR):
                return False
            e.strerror = "Unable to load configuration file {0}".format(e.strerror)
            raise
        return True
        

    def from_module_name(self, module_name):
        """
        """
        try:
            obj = __import__(module_name)
            self.from_object(obj)
        except:
            raise
        
    def from_object(self, obj):
        """
        """
        for key in dir(obj):
            self.__dict__[key] = obj.__dict__[key]

