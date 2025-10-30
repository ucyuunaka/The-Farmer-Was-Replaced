# 全尺寸-胡萝卜

def till_and_plant_column():
	for _ in range(get_world_size()):
		if can_harvest():
			harvest()
		if get_ground_type() != Grounds.Soil:
			till()
		plant(Entities.Carrot)
		move(North)

def harvest_and_replant_column():
	for _ in range(get_world_size()):
		if can_harvest():
			harvest()
		if get_ground_type() != Grounds.Soil:
			till()
		plant(Entities.Carrot)
		move(North)

for _ in range(get_world_size()):
	if not spawn_drone(till_and_plant_column):
		till_and_plant_column()
	move(East)

while True:
	for _ in range(get_world_size()):
		if not spawn_drone(harvest_and_replant_column):
			harvest_and_replant_column()
		move(East)