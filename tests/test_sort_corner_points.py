from itertools import permutations

import quadrilateral_sort


def test():
	test_tl_tr_bl_br()

def test_tl_tr_bl_br():
	print("Testing quadrilateral_sort.tl_tr_bl_br()")
	corner_points = [[537, 390], [301, 399], [517, 173], [278, 177]]

	for perm in permutations(corner_points):
		sorted_input = quadrilateral_sort.tl_tr_bl_br(list(perm))
		if sorted_input == corner_points:
			print('.', end='')
		else:
			print('x')
			print("Test failed for input:", perm)
			print("Got sorted result:", sorted_input)
