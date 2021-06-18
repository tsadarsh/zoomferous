def tl_tr_bl_br(random):
	def takeSecond(elem):
		return elem[1]

	random.sort(reverse=True, key=takeSecond)
	res = []
	rep = []
	res.append(random[0])
	res.append(random[1])
	rep.append(random[2])
	rep.append(random[3])
	res.sort(reverse=True, key=lambda x: int(x[0]))
	rep.sort(reverse=True, key=lambda x: int(x[0]))
	random.sort(reverse=True, key=lambda x: int(x[0]))
	final = [res[0], res[1], rep[0], rep[1]]
	return final
