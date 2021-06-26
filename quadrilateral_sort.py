def tl_tr_bl_br(corner_points):
	sort_cpts_wrt_y = sorted(corner_points, key=lambda x: x[1], reverse=True)

	upper_cpts = sort_cpts_wrt_y[:2]
	bottom_cpts = sort_cpts_wrt_y[2:]

	sort_upper_cpts_wrt_x = sorted(upper_cpts, key=lambda x: x[0], reverse=True)
	sort_bottom_cpts_wrt_x = sorted(bottom_cpts, key=lambda x: x[0], reverse=True)

	corner_points_in_tl_tr_bl_br_order = sort_upper_cpts_wrt_x + sort_bottom_cpts_wrt_x

	return corner_points_in_tl_tr_bl_br_order
