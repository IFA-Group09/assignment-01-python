import iv2py as iv

from assignment_01_python.suffix_array_search import print_suffixes, sa_search_naive


def test_sa_search_naive():
    reference_text = "banana$"
    sa = iv.create_suffixarray(reference_text)
    print_suffixes(sa=sa, reference=reference_text)
    assert sa_search_naive(sa=sa, pattern="n", reference=reference_text) == (5,6)

    assert sa_search_naive(sa=sa, pattern="b", reference=reference_text) == (4,4)

    assert sa_search_naive(sa=sa, pattern="ban", reference=reference_text) == (4,4)

    assert sa_search_naive(sa=sa, pattern="z", reference=reference_text) is None

    assert sa_search_naive(sa=sa, pattern="banana", reference=reference_text) == (4,4)
