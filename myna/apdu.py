

def new_APDU_case2(cla: int, ins: int, p1: int, p2: int, le: int):
	return [cla, ins, p1, p2, le]

def new_APDU_case3(cla: int, ins: int, p1: int, p2: int, data):
	cmd = [cla, ins, p1, p2, len(data)] + data
	return cmd