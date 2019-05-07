import unittest


def extract_elements(list1, list2):
    for i in range(len(list2)):
        if isinstance(list2[i], int):
            pass
        else:
            return "wrong input"
    try:
        return [list1[x] for x in list2]
    except IndexError:
        return 'index out of range'

lista1 = [5, 10, 15, 20]
lista2 = [3, 1, 2]
print(extract_elements(lista1, lista2))


class TestExtractElements(unittest.TestCase):
    def test_example(self):
        self.assertEqual(extract_elements(lista1, lista2), [20, 10, 15])

    def test_negative_numb_list2(self):
        self.assertEqual(extract_elements(lista1, [-1]), [20])

    def test_empty_list2(self):
        self.assertEqual(extract_elements(lista1, []), [])

    def test_float_list2(self):
        self.assertEqual(extract_elements(lista1, [2.0]), 'wrong input')

    def test_string_list2(self):
        self.assertEqual(extract_elements(lista1, ['str']), 'wrong input')

    def test_out_of_range_list2(self):
        self.assertEqual(extract_elements(lista1, [5]), 'index out of range')

