# 全尺寸-收获清理

def harvest_column():
	for _ in range(get_world_size()):
		if can_harvest():
			harvest()
		elif get_entity_type() == Entities.Dead_Pumpkin:
			plant(Entities.Grass)
		move(North)

for _ in range(get_world_size()):
	if not spawn_drone(harvest_column):
		harvest_column()
	move(East)