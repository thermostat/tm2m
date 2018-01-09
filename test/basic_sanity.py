


import unittest
import tm2m.named_histories
from tm2m.named_histories import History

class TM2MSanity(unittest.TestCase):
    def test_max_count(self):
        fd = open('./ex_history.txt', 'rt')
        history = tm2m.named_histories.add_fd('test', fd)
        self.assertEqual(len(history), 100)
        fd.close()

if __name__ == '__main__':
    unittest.main()
