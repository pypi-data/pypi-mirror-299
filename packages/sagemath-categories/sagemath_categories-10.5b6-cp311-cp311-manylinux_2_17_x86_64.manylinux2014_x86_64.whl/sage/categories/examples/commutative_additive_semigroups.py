# sage_setup: distribution = sagemath-categories
"""
Examples of commutative additive semigroups
"""
#*****************************************************************************
#  Copyright (C) 2008-2009 Nicolas M. Thiery <nthiery at users.sf.net>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#******************************************************************************

from sage.misc.cachefunc import cached_method
from sage.structure.parent import Parent
from sage.structure.element_wrapper import ElementWrapper
from sage.structure.unique_representation import UniqueRepresentation
from sage.categories.commutative_additive_semigroups import CommutativeAdditiveSemigroups
from sage.sets.family import Family


class FreeCommutativeAdditiveSemigroup(UniqueRepresentation, Parent):
    r"""
    An example of a commutative additive monoid: the free commutative monoid.

    This class illustrates a minimal implementation of a commutative additive monoid.

    EXAMPLES::

        sage: S = CommutativeAdditiveSemigroups().example(); S
        An example of a commutative semigroup: the free commutative semigroup generated by ('a', 'b', 'c', 'd')

        sage: S.category()
        Category of commutative additive semigroups

    This is the free semigroup generated by::

        sage: S.additive_semigroup_generators()
        Family (a, b, c, d)

    with product rule given by `a \times b = a` for all `a, b`::

        sage: (a,b,c,d) = S.additive_semigroup_generators()

    We conclude by running systematic tests on this commutative monoid::

        sage: TestSuite(S).run(verbose = True)
        running ._test_additive_associativity() . . . pass
        running ._test_an_element() . . . pass
        running ._test_cardinality() . . . pass
        running ._test_category() . . . pass
        running ._test_construction() . . . pass
        running ._test_elements() . . .
          Running the test suite of self.an_element()
          running ._test_category() . . . pass
          running ._test_eq() . . . pass
          running ._test_new() . . . pass
          running ._test_not_implemented_methods() . . . pass
          running ._test_pickling() . . . pass
          pass
        running ._test_elements_eq_reflexive() . . . pass
        running ._test_elements_eq_symmetric() . . . pass
        running ._test_elements_eq_transitive() . . . pass
        running ._test_elements_neq() . . . pass
        running ._test_eq() . . . pass
        running ._test_new() . . . pass
        running ._test_not_implemented_methods() . . . pass
        running ._test_pickling() . . . pass
        running ._test_some_elements() . . . pass
    """

    def __init__(self, alphabet=('a','b','c','d')):
        r"""
        The free commutative monoid.

        INPUT:

        - ``alphabet`` -- tuple of strings; the generators of the semigroup

        EXAMPLES::

            sage: M = CommutativeAdditiveSemigroups().example(alphabet=('a','b','c')); M
            An example of a commutative semigroup: the free commutative semigroup generated by ('a', 'b', 'c')

        TESTS::

            sage: TestSuite(M).run()
        """
        self.alphabet = alphabet
        Parent.__init__(self, category=CommutativeAdditiveSemigroups())

    def _repr_(self):
        r"""
        EXAMPLES::

            sage: M = CommutativeAdditiveSemigroups().example(alphabet=('a','b','c'))
            sage: M._repr_()
            "An example of a commutative semigroup: the free commutative semigroup generated by ('a', 'b', 'c')"
        """
        return "An example of a commutative semigroup: the free commutative semigroup generated by %s" % (self.alphabet,)

    def summation(self, x, y):
        r"""
        Return the product of ``x`` and ``y`` in the semigroup, as per
        :meth:`CommutativeAdditiveSemigroups.ParentMethods.summation`.

        EXAMPLES::

            sage: F = CommutativeAdditiveSemigroups().example()
            sage: (a,b,c,d) = F.additive_semigroup_generators()
            sage: F.summation(a,b)
            a + b
            sage: (a+b) + (a+c)
            2*a + b + c
        """
        assert x in self
        assert y in self
        return self((a, x.value[a] + y.value[a]) for a in self.alphabet)

    @cached_method
    def additive_semigroup_generators(self):
        r"""
        Return the generators of the semigroup.

        EXAMPLES::

            sage: F = CommutativeAdditiveSemigroups().example()
            sage: F.additive_semigroup_generators()
            Family (a, b, c, d)
        """
        return Family( [self(((a,1),)) for a in self.alphabet] )
        # FIXME: use this once the keys argument of FiniteFamily will be honoured
        # for the specifying the order of the elements in the family
        # return Family(self.alphabet, lambda a: self(((a,1),)))

    def an_element(self):
        r"""
        Return an element of the semigroup.

        EXAMPLES::

            sage: F = CommutativeAdditiveSemigroups().example()
            sage: F.an_element()
            a + 2*b + 3*c + 4*d
        """
        return self((a, (ord(a)-96)) for a in self.alphabet)

    class Element(ElementWrapper):
        def __init__(self, parent, iterable):
            """
            EXAMPLES::

                sage: F = CommutativeAdditiveSemigroups().example()
                sage: x = F.element_class(F, (('a',4), ('b', 0), ('a', 2), ('c', 1), ('d', 5)))
                sage: x
                2*a + c + 5*d
                sage: x.value
                {'a': 2, 'b': 0, 'c': 1, 'd': 5}
                sage: x.parent()
                An example of a commutative semigroup: the free commutative semigroup generated by ('a', 'b', 'c', 'd')

            Internally, elements are represented as dense dictionaries which
            associate to each generator of the monoid its multiplicity. In
            order to get an element, we wrap the dictionary into an element
            via :class:`ElementWrapper`::

                sage: x.value
                {'a': 2, 'b': 0, 'c': 1, 'd': 5}
            """
            d = {a: 0 for a in parent.alphabet}
            for a, c in iterable:
                d[a] = c
            ElementWrapper.__init__(self, parent, d)

        def _repr_(self):
            """
            EXAMPLES::

                sage: F = CommutativeAdditiveSemigroups().example()
                sage: F.an_element() # indirect doctest
                a + 2*b + 3*c + 4*d

                sage: F(())
                0
            """
            d = self.value
            result = ' + '.join( ("%s*%s" % (d[a],a) if d[a] != 1 else a) for a in sorted(d.keys()) if d[a] != 0)
            return '0' if result == '' else result

        def __hash__(self):
            """
            EXAMPLES::

                sage: F = CommutativeAdditiveSemigroups().example()
                sage: type(hash(F.an_element()))
                <... 'int'>
            """
            return hash(tuple(self.value.items()))


Example = FreeCommutativeAdditiveSemigroup
