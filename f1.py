# 全尺寸-胡萝卜

for i in range(get_world_size()):
	for j in range(get_world_size()):
		if get_ground_type() != Grounds.Soil:
			till()
		plant(Entities.Carrot)
		move(North)
	move(East)

while True:
	for i in range(get_world_size()):
		for j in range(get_world_size()):
			if can_harvest():
				harvest()
				if get_ground_type() != Grounds.Soil:
					till()
				plant(Entities.Carrot)
			move(North)
		move(East)