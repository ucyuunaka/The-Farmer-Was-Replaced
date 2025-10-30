# 全尺寸-奇异物质

def plant_column():
	for _ in range(get_world_size()):
		if can_harvest():
			harvest()
		plant(Entities.Bush)
		move(North)

def fertilize_and_harvest_column():
	for _ in range(get_world_size()):
		if get_entity_type() == Entities.Bush:
			use_item(Items.Fertilizer)
		if can_harvest():
			harvest()
		plant(Entities.Bush)
		move(North)

for _ in range(get_world_size()):
	if not spawn_drone(plant_column):
		plant_column()
	move(East)

while True:
	for _ in range(get_world_size()):
		if not spawn_drone(fertilize_and_harvest_column):
			fertilize_and_harvest_column()
		move(East)