from functools import wraps
import inspect
# (C) 2018 - Duane Ellis, Duane Ellis duane@duaneellis.com
# License: Same as Python, using the PSF copyright.
# ---------------
# I have seen multiple implimentations
# this is a combination of various ones I've seen
#
# Alternate methods, this is sort of a combination of these
#==========================================================
#  http://code.activestate.com/recipes/252158-how-to-freeze-python-classes/
#  https://stackoverflow.com/questions/3603502/prevent-creating-new-attributes-outside-init
#  https://github.com/python-attrs/attrs/ (see "frozen")
#  https://im-coder.com/verhindert-das-erstellen-neuer-attribute-ausserhalb-von-__init__.html

__all__ = ['FrozenError', 'FrozenClass']

class FrozenError( Exception ):
    pass


def FrozenClass(cls):
    '''
    This class decorator is used to stop human spelling mistakes
    that happen when creating attributes for a class

    For example, it is easy to do things like "foo.girls" 
    when you meant "foo.girl" or other silly mistakes
    like "foo.spelled_correctly" and "foo.speled_correctly"

    Effectively, this restricts attribute creating (addition)
    to the class __init__() function, or the __init__() function
    of any subclass of this function

    Usage: 

    >>> @FrozenClass
    >>> class FooBar():
    >>>     def __init__( self ):
    >>>          self.x = 42
    >>>     def this_fails(self):
    >>>          self.kabang = "This will raise an exception"
    >>>     def this_works(self):
    >>>          self._thaw()
    >>>          self.water = "not ice"
    >>>          self._freeze()


    Another example:

    >>>  foo = FooBar()
    >>>  foo.x = 42    # no problem, attr (x) exists.
    >>>  foo.xxx = 42  # xxx does not exist, raises FrozenError
 
    In contrast, you can thaw, then refreeze the class
    while thawed - you can add anything you need.

    >>>  foo._thaw()
    >>>  x.yyyy = 42    # It's not frozen, this works
    >>>  x._freeze() # lock it up

    '''

    # Provide default values only if not already present
    cls.__frozen = False
    '''Current state, use self._freeze() or self._thaw() to change'''
    
    cls.__frozen_auto_freeze = True
    '''Automatically freeze at end of __init__() call'''
    
    cls.__frozen_track_where = False
    '''
    Set to true, and the frozen decorator will try to track where 
    (filename/linenumber) attributes are added or defined within a 
    class. Useful for tracking down variable name typos.
    '''
    cls.__frozen_where = dict()
    '''
    When tracking is enabled, key = attribute name.
    Data is a tuple of (filename, lineno) where the attribute
    was created

    NOTE: In a debugger, invoke self._print_attribute_birthplace()
    it will print the attributes, and where they where defined.
    '''

    def frozen_print(self):
        print("")
        print("===========================================")
        print("Attribute locations for: %s" % self.__class__.__name__)
        for k in sorted(self.__frozen_where.keys()):
            filename,lineno = self.__frozen_where[k]
            print("%*s: %s:%d" % (15,k,filename,lineno))
        print("===========================================")

    cls._freeze_print_birthplace = frozen_print
        
    def thaw(self):
        '''Thaw this class, allow modification '''
        self.__dict__['__frozen'] = False

    cls._thaw = thaw
        
    def enableTracking(self):
        self.__dict__['__frozen_track_where'] = True

    cls._freeze_enable_tracking = enableTracking
        
    def disableTracking(self):
        self.__dict__['__frozen_track_where'] = False

    cls._freeze_disable_tracking = disableTracking
        
    def isFrozen(self):
        return self.__dict__['__frozen']

    cls._isfrozen = isFrozen
    
    def freeze(self):
        '''Freeze this class, prevent modification'''
        self.__dict__['__frozen'] = True

    # The callable to change state to frozen
    cls._freeze = freeze
        
    def init_decorator(func):
        @wraps(func)
        def wrapper( self, *args, **kwargs ):
            old = self.__frozen
            if (not old) and (self.__frozen_auto_freeze):
                self.__frozen = False
            # call the init function
            func(self, *args, **kwargs)
            if self.__frozen_auto_freeze:
                old = True
            self.__frozen = old
        return wrapper

    
    # Decorate the init function
    cls.__init__ = init_decorator( cls.__init__ )

    # Do this last provide our catch function
    def my_setattr( self, key, value ):
        # Decisions are made in an order for performance reasons.
        
        # most common case is success
        #  just set the value
        if key in self.__dict__:
            self.__dict__[key] = value
            return

        # Second most common case, success if not frozen
        if not self.__frozen:
            # Not frozen, add the new attribute
            self.__dict__[key] = value
            if self.__frozen_track_where:
                # If enabled track where it was created
                calling_frame_record = inspect.stack()[1]
                # tuple Filename:LineNumber
                self.__frozen_where[ key ] = (calling_frame_record[1],calling_frame_record[2])
            return
        
        # We are going to die here... we can do time-expensive things
        # Inspect parent (our caller) are we in the __init__() call?
        frame_record = inspect.stack()
        if inspect.stack()[1][3] == '__init__':
            self.__dict__[key] = value
            return

        # We are dead
        raise FrozenError("class %s is frozen cannot add %s=%s" % (self.__class__.__name__,key,value))
    
    cls.__setattr__ = my_setattr

    # Return the decorated class
    return cls

