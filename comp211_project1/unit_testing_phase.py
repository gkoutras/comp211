import unittest
import logging 
import logging.config
from unit_testing_phase_rp import UnitTest
from unit_testing_phase_rp import FileHandler
from unit_testing_phase_rp import Utils


class Test_readCurrentTweet_class(unittest.TestCase):
    
    def setUp(self):
        
        init(self)

    def test_readCurrentTweet(self):

        self.data = self.u.menu_handler('=', self.data, self.fh, self.logfile, self.ut, 1)
        self.assertEqual(self.ut.get_tweet(self.data), "RT @ShitNobodySays: I'm voting Obama in 2012!")
        print('\nTEST 1: =/q --> read current tweet.......................................... OK \n')

    def test_readCurrentTweet_afterDown(self):

        self.data = self.u.menu_handler('-', self.data, self.fh, self.logfile, self.ut, 4)
        self.assertEqual(self.ut.get_tweet(self.data), "\"Anatomy of a Campus Coup\" On the failed deposal of University of Virginia's president: http://t.co/IpGPw3E4  (by @riceid, new @NYTmag)")
        print('\nTEST 2: -/= --> first down then read current tweet.......................... OK \n')


class Test_readUpDownTweet_class(unittest.TestCase):
    
    def setUp(self):
        
        init(self)

    def test_readDownTweet(self):

        self.data = self.u.menu_handler('-', self.data, self.fh, self.logfile, self.ut, 1)
        self.assertEqual(self.ut.get_tweet(self.data), "\"Anatomy of a Campus Coup\" On the failed deposal of University of Virginia's president: http://t.co/IpGPw3E4  (by @riceid, new @NYTmag)")
        print('TEST 3: -/q --> down current tweet.......................................... OK')

    def test_readUpTweet(self):
        
        self.data = self.u.menu_handler('-', self.data, self.fh, self.logfile, self.ut, 3)
        self.assertEqual(self.ut.get_tweet(self.data), "RT @ShitNobodySays: I'm voting Obama in 2012!")
        print('TEST 4: -/+ --> first down then up.......................................... OK')


class Test_simple_readLastOriginal_class(unittest.TestCase):
    
    
    def setUp(self):
        
        init(self)
    
    def test_readLastOriginal(self):

        self.data = self.u.menu_handler('$', self.data, self.fh, self.logfile, self.ut, 1)
        self.assertEqual(self.ut.get_tweet(self.data), "RT @ShitNobodySays: I'm voting Obama in 2012!")
        print('TEST 5: $/q --> read last tweet............................................. OK')

    
class Test_creation_noSave_class(unittest.TestCase):
    
    def setUp(self):
        
      init(self)
    
    def test_creation_noSave(self):

        self.data = self.u.menu_handler('c', self.data, self.fh, self.logfile, self.ut, 1)
        self.assertEqual(self.ut.get_tweet(self.data), "tuc tuc")
        print('TEST 6: c/q --> create tweet/no save........................................ OK')
    
    def test_readLast(self):
        
        self.data = self.u.menu_handler('$', self.data, self.fh, self.logfile, self.ut, 1)
        self.assertEqual(self.ut.get_tweet(self.data), "RT @ShitNobodySays: I'm voting Obama in 2012!")
        print('TEST 7: $/q --> after creation read last tweet (no change).................. OK')


class Test_creation_withSave_class(unittest.TestCase):
   
    def setUp(self):
        
        init(self)
    
    def test_creation_withSave(self):

        self.data = self.u.menu_handler('c', self.data, self.fh, self.logfile, self.ut, 2)
        self.assertEqual(self.ut.get_tweet(self.data), "tuc tuc")
        print('TEST 8: c/x --> create tweet/with save ..................................... OK')
    
    def test_readLastCreated(self):
        
        self.data = self.u.menu_handler('$', self.data, self.fh, self.logfile, self.ut, 1)
        self.assertEqual(self.ut.get_tweet(self.data), "tuc tuc")
        print('TEST 9: $/q --> after creation read last tweet (changed).................... OK')


class Test_DeleteLastTweet_noSave_class(unittest.TestCase):
    
    def setUp(self):
        
        init(self)

    def test_delete_lastTweet(self):
    
        self.data = self.u.menu_handler('d', self.data, self.fh, self.logfile, self.ut, 1)
        self.assertEqual(self.ut.get_tweet(self.data), "RT @ShitNobodySays: I'm voting Obama in 2012!")
        print('TEST 10: d/q --> delete last tweet/no save................................... OK')
    
    def test_readLastTweet(self):
    
        self.data = self.u.menu_handler('$', self.data, self.fh, self.logfile, self.ut, 1)
        self.assertEqual(self.ut.get_tweet(self.data), "tuc tuc")
        print('TEST 11: $/q --> after deletion read last tweet (no change).................. OK')

    
class Test_DeleteLastTweet_withSave_class(unittest.TestCase):
    
    def setUp(self):
        
        init(self)

    def test_delete_lastTweet(self):
    
        self.data = self.u.menu_handler('d', self.data, self.fh, self.logfile, self.ut, 2)
        self.assertEqual(self.ut.get_tweet(self.data), "RT @ShitNobodySays: I'm voting Obama in 2012!")
        print('\nTEST 12: d/x --> delete tweet/with save ..................................... OK')
    
    def test_readLastTweet(self):
    
        self.data = self.u.menu_handler('$', self.data, self.fh, self.logfile, self.ut, 1)
        self.assertEqual(self.ut.get_tweet(self.data), "RT @ShitNobodySays: I'm voting Obama in 2012!")
        print('TEST 13: $/q --> after deletion read last tweet (changed).................... OK')


class Test_chunkSize_class(unittest.TestCase):
    
    def setUp(self):

        init(self)
    
    def test_chunkSize(self):

        self.data = self.u.menu_handler('q', self.data, self.fh, self.logfile, self.ut, 1)
        self.assertEqual(self.fh.determine_chunks(self.ut.get_sizeOfFile(),10000), 30)
        print('TEST 14: (q) --> check chunck size when the program initialized ............. OK')


class Test_chunkSize_afterCreate_class(unittest.TestCase):
    
    def setUp(self):

        init(self)

    def test_first_create1(self):
    
        self.data = self.u.menu_handler('c', self.data, self.fh, self.logfile, self.ut, 2)
        self.assertEqual(self.ut.get_tweet(self.data), "tuc tuc")
        print('TEST 15: c/x --> create tweet check(with save) .............................. OK')

    def test_first_create2(self):
    
        self.data = self.u.menu_handler('c', self.data, self.fh, self.logfile, self.ut, 2)
        self.assertEqual(self.ut.get_tweet(self.data), "tuc tuc")
        print('TEST 16: c/x --> create tweet check(with save) .............................. OK')
        
    def test_first_create_then_checkChunks(self):
    
        self.assertEqual(self.fh.determine_chunks(self.ut.get_sizeOfFile(),10000), 31)
        print('TEST 17: (q) --> check chunck size(changed) ................................. OK')


class Test_updateNoSave_class(unittest.TestCase):

    def setUp(self):

        init(self)
    
    def test_1updateNoSave(self):

        self.data = self.u.menu_handler('u', self.data, self.fh, self.logfile, self.ut, 1)
        self.assertEqual(self.ut.get_tweet(self.data), "tuc tuc")
        print('TEST 18: u/q --> update no save ............................................. OK')


class Test_updateWithWrite_class(unittest.TestCase):
    
    def setUp(self):

        init(self)
    
    def test_1updateWithWrite(self):

        self.data = self.u.menu_handler('u', self.data, self.fh, self.logfile, self.ut, 5)
        self.assertEqual(self.ut.get_tweet(self.data), "tuc tuc")
        print('\nTEST 19: u/w --> update with write .......................................... OK')

    def test_2readAfterUpdate(self):

        self.data = self.u.menu_handler('r', self.data, self.fh, self.logfile, self.ut, 1)
        self.assertEqual(self.ut.get_tweet(self.data), "tuc tuc")
        print('\nTEST 20: r/q --> read the updated and saved tweet............................ OK')
    
    def test_3last(self):

        self.data = self.u.menu_handler('d', self.data, self.fh, self.logfile, self.ut, 2)
        self.assertEqual(self.ut.get_tweet(self.data), "tuc tuc")
        print('TEST 21: d/x --> delete the last tweet with save............................ OK')

    def test_4last(self):

        self.data = self.u.menu_handler('d', self.data, self.fh, self.logfile, self.ut, 2)
        self.assertEqual(self.ut.get_tweet(self.data), "RT @ShitNobodySays: I'm voting Obama in 2012!")
        print('TEST 22: d/x --> delete the last tweet with save............................ OK')


def run_tests():

    test_classes_to_run = [Test_readCurrentTweet_class,Test_readUpDownTweet_class,
    Test_simple_readLastOriginal_class,Test_creation_noSave_class,
    Test_creation_withSave_class,Test_DeleteLastTweet_noSave_class,Test_DeleteLastTweet_withSave_class,
    Test_chunkSize_class,Test_chunkSize_afterCreate_class,Test_updateNoSave_class,Test_updateWithWrite_class]
    
    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)
        
    big_suite = unittest.TestSuite(suites_list)
    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)

def init(self):

    self.ut = UnitTest()
    self.fh = FileHandler()
    self.u = Utils() 
    self.data = self.fh.read_from_json()

    logging.config.fileConfig('myeditorlog.conf')
    self.logfile = logging.getLogger("tester")


if __name__ == '__main__':
    run_tests()
    