import unittest
import password_generator

class TestPasswordGenerator(unittest.TestCase):
  def setUp(self):
    self.mystr = "teststring"
    self.pickChars = password_generator.pickCharsFromString(self.mystr, 5)
    self.shuffledString = password_generator.shuffleString(self.mystr)

  def testPickCharsFromStringLength(self):
    # Assert that the length is correct:
    self.assertEqual(len(self.pickChars), 5)

  def testPickCharsCharacters(self):
    # Assert that each chosen character was in the original string:
    for c in self.pickChars:
      self.assertTrue(c in self.mystr)

  def testShuffleString(self):
    # Assert that the shuffle actually produces a different string:
    # (I guess there is some % chance that the shuffle produces the exact same string, but that's gonna be rare.)
    self.assertNotEqual(self.mystr, self.shuffledString)

  def testShuffleStringChars(self):
    # Assert that all the same chars are in the shuffled string. (Why wouldn't this pass?)
    for c in self.shuffledString:
      self.assertTrue(c in self.mystr)
  
  def testShuffleLength(self):
    # Assert that the shuffled string is the same length as the original:
    self.assertEqual(len(self.mystr), len(self.shuffledString))

  def testCorrectPasswordLength(self):
    passw = password_generator.generateRandomPassword(15)
    # Assert that generateRandomPassword produces a password of correct given length:
    self.assertEqual(len(passw), 15)

if __name__ == '__main__':
  unittest.main()