# A simple Frozen Class Decorator for Python

Often it is easy to create bugs in your python code by spelling attributes wrong.
This becomes more of a problem when your python classes get big and complex.

## For example

```
    
    foo = SomeClass()
    foo.spelled_correctly = True
    foo.speled_correctly = False
    foo.spelled_corectly = False
```

This ends up causing no end of little problems, and finding where this
occurs is sometimes non-trivial.

*The Goal* This module aims to make it easier to not do the above..

## usage

```python
    from frozenclass import FrozenClass
    
    @FrozenClass
    class FooBar():
         def __init__( self ):
             self.x = 42
        def this_fails(self):
             # Assuming the class is frozen...
             self.kabang = "This will raise an exception"
        def this_works(self):
             # Assuming the class is frozen
             self._thaw()
             # It's not froze so we can add something
             self.water = "not frozen"
             # And freeze again
             self._freeze()

    foo = FooBar()
    foo.x = 42 # this works
    foo.bang = "this fails"
    
    # you can also thaw, modify then refreeze
    foo._thaw()
    foo.changed = True
    foo._freeze()
    
    # you can also debug things
    foo._freeze_enable_tracking()

    foo._thaw()
    foo.wow = 1234
     
     # Then later in your code, or in the debugger
     foo._freeze_print_birthplace()
     # will produce a nice human report showing where the attibute where defined.
```

