# 全尺寸-草料收获

clear()

while True:
	for i in range(get_world_size()):
		for j in range(get_world_size()):
			if can_harvest():
				harvest()
			move(North)
		move(East)