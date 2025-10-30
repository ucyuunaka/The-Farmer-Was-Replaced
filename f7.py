# 仙人掌种植收获

# 初始种植
for i in range(get_world_size()):
	for j in range(get_world_size()):
		if get_ground_type() != Grounds.Soil:
			till()
		if can_harvest():
			harvest()
		plant(Entities.Cactus)
		move(North)
	move(East)

# 循环收获和排序
while True:
	for i in range(get_world_size()):
		for j in range(get_world_size()):
			if can_harvest():
				harvest()
				if get_ground_type() != Grounds.Soil:
					till()
				plant(Entities.Cactus)

			if get_entity_type() == Entities.Cactus:
				if measure() != None:
					east_size = measure(East)
					if east_size != None and measure() > east_size:
						if get_pos_x() < get_world_size() - 1:
							swap(East)
			move(North)
		move(East)