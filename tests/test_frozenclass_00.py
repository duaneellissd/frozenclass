from unittest import TestCase

from frozenclass import *
import frozenclass

@FrozenClass
class TestClassA():
    def __init__(self):
        self.foo = 123


    def this_fails(self):
        self.kabang = "This will raise an exception"
        
    def this_works(self):
        self._thaw()
        self.water = "not ice"
        self._freeze()
        
        
class TestClassB( TestClassA ):
    def __init__(self):
        TestClassA.__init__(self)
        self.bar = 321

    def this_fails(self):
        # This should raise an error, foo!=Foo
        self.Foo = 123
            
    def test_thaw(self):
        self._thaw()
        self.thaw_works = True
        self._freeze()

    def test_thawfreeze(self):
        self.test_thaw()
        # This should fail
        self.should_fail = 42+1
        
class  Test_01(TestCase):
    def test_10_decorate(self):
        # basic test to see if we can decorate

        x = TestClassA()
        self.assertEqual( x.foo,  123 )
        # Test complete, we can create the class.

    def test_15_doc_example(self):
        x = TestClassA()
        x.foo = 999
        x.this_works()
        with self.assertRaises( FrozenError ):
            x.bar = 'Ka Bang Fails'
        with self.assertRaises( FrozenError ):
            x.this_fails()
            
        # Test complete
    
        
    def test_20_raise(self):
        # Basic test to see if we can cause a failure
        x = TestClassA()
        with self.assertRaises( FrozenError ):
            x.does_not_exist = 1
        # Test complete
        
    def test_30_freezethaw(self):
        # Test the freeze thaw steps
        x = TestClassA()
        x._thaw()
        x.new_attr = 1
        x._freeze()
        self.assertEqual( x.new_attr, 1 )
        # The after freezing it should fail
        with self.assertRaises( FrozenError ):
            x.does_not_exist = 1
        x.new_attr = 2
        self.assertEqual( x.new_attr, 2 )
        # Test complete

    def test_40_twolayer_work(self):
        # Test derived classes.
        x = TestClassB()
        self.assertEqual( x.foo, 123 )
        self.assertEqual( x.bar, 321 )
        # sucess we can create the class
        
        
    def test_50_test_thaw(self):
            
        x = TestClassB()
        
        # test thawing from within class
        x.test_thaw()
        self.assertEqual( x._isfrozen(), True )
        self.assertEqual( x.thaw_works, True )

    def test_60_test_thawfreeze(self):
        x = TestClassB()
        
        # Add something that should fail
        with self.assertRaises( FrozenError ):
            x.test_thawfreeze()

    def test_70_print_where(self):
        x = TestClassB()
        print("")
        print(dir(x))
        x._freeze_enable_tracking()
        x._thaw()
        x.create_me_baby = True
        #self.assertTrue( len( x.__frozen_where ) == 1 )
        print("wheres: %s" % x.__frozen_where.keys())
        self.assertTrue( 'create_me_baby' in x.__frozen_where )
        x._print_attribute_birthplace()

