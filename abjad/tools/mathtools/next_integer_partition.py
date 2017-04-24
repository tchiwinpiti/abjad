# -*- coding: utf-8 -*-


# TODO: make private and add to yield_all_integer_partitions()
def next_integer_partition(integer_partition):
    r'''Gets next integer partition following `integer_partition`
    in descending lex order.

    ..  container:: example

        ::

            >>> mathtools.next_integer_partition((8, 3))
            (8, 2, 1)

        ::

            >>> mathtools.next_integer_partition((8, 2, 1))
            (8, 1, 1, 1)

        ::

            >>> mathtools.next_integer_partition((8, 1, 1, 1))
            (7, 4)

    `integer_partition` must be tuple of positive integers.

    Returns new integer partition tuple.
    '''
    _validate_input(integer_partition)
    left_half, right_half = _split_into_left_and_right_halves(
        integer_partition
        )
    # if input was all 1s like (1, 1, 1, 1) then we're done
    if not left_half:
        return None
    new_left_half = left_half[:-1] + [left_half[-1] - 1]
    new_right_weight = sum(right_half) + 1
    new_right_half = _rewrite(new_right_weight, new_left_half[-1])
    result = new_left_half + new_right_half
    result = tuple(result)
    return result


def _split_into_left_and_right_halves(integer_partition):
    r'''Splits not-1s (left half) from 1s (right half).

    _split_into_left_and_right_halves((8, 3))
    [8, 3], []

    _split_into_left_and_right_halves((8, 2, 1))
    [8, 2], [1, ]

    _split_into_left_and_right_halves((8, 1, 1, 1))
    [8], [1, 1, 1]

    '''
    left_half = []
    right_half = []
    for part in integer_partition:
        if not part == 1:
            left_half.append(part)
        else:
            right_half.append(part)
    return left_half, right_half


def _validate_input(integer_partition):
    r'''Ensures monotonically decreasing iterable of positive integers.

    (8, 2, 2, 1) is OK.
    (8, 1, 2, 2) is not.

    '''
    previous = None
    for current in integer_partition:
        if not isinstance(current, int):
            message = 'must be integer.'
            raise TypeError(message)
        if not 0 < current:
            message = 'must be positive.'
            raise ValueError(message)
        if previous is not None:
            if not current <= previous:
                message = 'parts must decrease monotonically.'
                raise ValueError(message)


def _rewrite(n, m):
    r'''Write positive integer n as the sum of many m in a row, followed either
    by nothing or by a final positive integer p such that p is strictly less
    than m.

        _rewrite(8, 4)
        (4, 4)

        _rewrite(8, 3)
        (3, 3, 2)

        _rewrite(8, 2)
        (2, 2, 2, 2)

        _rewrite(8, 1)
        (1, 1, 1, 1, 1, 1, 1, 1)

    '''
    quotient = int(n / m)
    remainder = n % m
    if remainder:
        return [m] * quotient + [remainder]
    else:
        return [m] * quotient
