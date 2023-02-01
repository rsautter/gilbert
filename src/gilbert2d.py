#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-2-Clause
# Copyright (c) 2018 Jakub Červený

import numpy as np 

def gilbert2d(width, height):
    """
    Generalized Hilbert ('gilbert') space-filling curve for arbitrary-sized
    2D rectangular grids. Generates discrete 2D coordinates to fill a rectangle
    of size (width x height).
    """

    if width >= height:
        yield from generate2d(0, 0, width, 0, 0, height)
    else:
        yield from generate2d(0, 0, 0, height, width, 0)


def sgn(x):
    return -1 if x < 0 else (1 if x > 0 else 0)


def generate2d(x, y, ax, ay, bx, by):

    w = abs(ax + ay)
    h = abs(bx + by)

    (dax, day) = (sgn(ax), sgn(ay)) # unit major direction
    (dbx, dby) = (sgn(bx), sgn(by)) # unit orthogonal direction

    if h == 1:
        # trivial row fill
        for i in range(0, w):
            yield(x, y)
            (x, y) = (x + dax, y + day)
        return

    if w == 1:
        # trivial column fill
        for i in range(0, h):
            yield(x, y)
            (x, y) = (x + dbx, y + dby)
        return

    (ax2, ay2) = (ax//2, ay//2)
    (bx2, by2) = (bx//2, by//2)

    w2 = abs(ax2 + ay2)
    h2 = abs(bx2 + by2)

    if 2*w > 3*h:
        if (w2 % 2) and (w > 2):
            # prefer even steps
            (ax2, ay2) = (ax2 + dax, ay2 + day)

        # long case: split in two parts only
        yield from generate2d(x, y, ax2, ay2, bx, by)
        yield from generate2d(x+ax2, y+ay2, ax-ax2, ay-ay2, bx, by)

    else:
        if (h2 % 2) and (h > 2):
            # prefer even steps
            (bx2, by2) = (bx2 + dbx, by2 + dby)

        # standard case: one step up, one long horizontal, one step down
        yield from generate2d(x, y, bx2, by2, ax2, ay2)
        yield from generate2d(x+bx2, y+by2, ax, ay, bx-bx2, by-by2)
        yield from generate2d(x+(ax-dax)+(bx2-dbx), y+(ay-day)+(by2-dby),
                              -bx2, -by2, -(ax-ax2), -(ay-ay2))

def vec2mat(vet, s=4):
	'''
	Transforms the vector into a matrix using the generalized hilbert curve
	--------------
	vet - input vector
	s - the first dimension of the matrix, if it is not multple, then returns an exception
	--------------
	Author: Rubens A. Sautter (2023)
	'''
	if len(vet)%s != 0:
		raise Excetion("Invalid dimenson size!")
	mat = np.zeros((s,len(vet)//s))
	gb = gilbert2d(s,len(vet)//s)
	for idx, (x,y) in enumerate(gb):
		mat[x,y] = vet[idx]
	return mat
		
def mat2vec(mat):
	'''
	Transforms the vector into a matrix using the generalized hilbert curve
	--------------
	mat - input matrix
	--------------
	Author: Rubens A. Sautter (2023)
	'''
	vet = np.zeros(len(mat)*len(mat[0]))
	gb = gilbert2d(len(mat),len(mat[0]))
	for idx, (x,y) in enumerate(gb):
		vet[idx] = mat[x,y]
	return vet

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('width', type=int)
    parser.add_argument('height', type=int)
    args = parser.parse_args()

    for x, y in gilbert2d(args.width, args.height):
        print(x, y)
