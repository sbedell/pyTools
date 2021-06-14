import unittest
import password_generator

class TestPasswordGenerator(unittest.TestCase):
  #def setUp(self):

  def testPickCharsFromString(self):
    mystr = "teststring"
    pickChars = password_generator.pickCharsFromString(mystr, 3)
    # Assert that the length is correct:
    self.assertEqual(len(pickChars), 3)

    # Assert that each chosen character was in the original string:
    for c in pickChars:
      self.assertTrue(c in mystr)

  def testShuffleString(self):
    mystr = "teststring"
    shuffledString = password_generator.shuffleString(mystr)
    self.assertNotEqual(mystr, shuffledString)

  def testCorrectPasswordLength(self):
    passw = password_generator.generateRandomPassword(15)
    self.assertEqual(len(passw), 15)

if __name__ == '__main__':
  unittest.main()