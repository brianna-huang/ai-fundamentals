import homework1
import numpy as np


def test_concatenate() -> None:
    ans = homework1.concatenate(["abc", (0, [0])])
    assert ['a', 'b', 'c', 0, [0]] == ans, "Incorrect concatenation"


def test_transpose() -> None:
    ans = homework1.transpose([[1, 2], [3, 4], [5, 6]])
    assert [[1, 3, 5], [2, 4, 6]] == ans, "Incorrect transpose"


def test_copy() -> None:
    copy_123 = homework1.copy((1, 2, 3))
    assert (1, 2, 3) == copy_123, "Incorrect copy"


def test_all_but_last() -> None:
    ans = homework1.all_but_last((1, 2, 3))
    assert (1, 2) == ans, "Incorrect all but last"
    ans = homework1.all_but_last("")
    assert "" == ans, "Incorrect all but last"


def test_every_other() -> None:
    ans = homework1.every_other("abcde")
    assert 'ace' == ans, "Incorrect every other"


def test_prefix() -> None:
    ans = list(homework1.prefixes([1, 2, 3]))
    assert [[], [1], [1, 2], [1, 2, 3]] == ans, "Incorrect prefixes"


def test_suffix() -> None:
    ans = list(homework1.suffixes("abc"))
    assert ['abc', 'bc', 'c', ''] == ans, "Incorrect suffixes"


def test_slices() -> None:
    ans = list(homework1.slices("abc"))
    assert ['a', 'ab', 'abc', 'b', 'bc', 'c'] == ans, "Incorrect slices"


def test_normalize() -> None:
    ans = homework1.normalize(" EXTRA   SPACE ")
    assert 'extra space' == ans, "incorrect normalize"


def test_no_vowels() -> None:
    ans = homework1.no_vowels("This Is An Example.")
    assert 'Ths s n xmpl.' == ans, "incorrect no vowels"


def test_dig_to_words() -> None:
    ans = homework1.digits_to_words("Pi is 3.1415...")
    assert 'three one four one five' == ans, "incorrect dig to words"


def test_to_mixed_case() -> None:
    ans = homework1.to_mixed_case("__EXAMPLE__NAME__")
    assert 'exampleName' == ans, "incorrect to mixed case"


def test_polynomial() -> None:
    p = homework1.Polynomial([(2, 1), (1, 0)])
    ans = p.get_polynomial()
    assert ((2, 1), (1, 0)) == ans, 'incorrect get polynomial'
    q = -p
    ans = q.get_polynomial()
    assert ((-2, 1), (-1, 0)) == ans, 'incorrect neg'
    q = p + p
    ans = q.get_polynomial()
    assert ((2, 1), (1, 0), (2, 1), (1, 0)) == ans, 'incorrect add'
    q = p - p
    ans = q.get_polynomial()
    assert ((2, 1), (1, 0), (-2, 1), (-1, 0)) == ans, 'incorrect sub'
    q = p * p
    ans = q.get_polynomial()
    assert ((4, 2), (2, 1), (2, 1), (1, 0)) == ans, 'incorrect mul'
    q = -(p * p) + p
    ans = [q(x) for x in range(5)]
    assert [0, -6, -20, -42, -72] == ans, 'incorrect call'
    q = -p + (p * p)
    q.simplify()
    ans = q.get_polynomial()
    assert ((4, 2), (2, 1)) == ans, 'incorrect simplify'
    q = p - p
    q.simplify()
    ans = q.get_polynomial()
    assert ((0, 0),) == ans, 'incorrect simplify'
    q = homework1.Polynomial([(1, 1), (2, 3)])
    ans = str(-q * q)
    assert '-x^2 - 2x^4 - 2x^4 - 4x^6' == ans, 'incorrect str'


def test_sort_array() -> None:
    matrix1 = np.array([[1, 2], [3, 4]])
    matrix2 = np.array([[5, 6, 7], [7, 8, 9], [0, -1, -2]])
    ans = homework1.sort_array([matrix1, matrix2])
    assert np.array_equal(np.array(
        [9, 8, 7, 7, 6, 5, 4, 3, 2, 1, 0, -1, -2]), ans), 'incorrect sort array'


def test_pos_tag() -> None:
    sentence = 'The Force will be with you. Always.'
    ans = homework1.POS_tag(sentence)
    assert [('force', 'NN'), ('always', 'RB')] == ans, 'incorrect pos tag'


def main() -> None:
    # test_concatenate()
    # test_copy()
    # test_transpose()
    # test_all_but_last()
    # test_every_other()
    # test_prefix()
    # test_suffix()
    # test_slices()
    test_normalize()
    # test_no_vowels()
    # test_dig_to_words()
    # test_to_mixed_case()
    # test_polynomial()
    # test_pos_tag()
    # test_sort_array()


if __name__ == '__main__':
    main()
