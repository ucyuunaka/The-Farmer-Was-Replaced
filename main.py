# 遍历整个农场收获所有作物
for i in range(get_world_size()):
	for j in range(get_world_size()):
		if can_harvest():
			harvest()
		move(North)
	move(East)