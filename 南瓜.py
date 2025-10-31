# 全尺寸-南瓜（优化版）

def plant_column():
	for _ in range(get_world_size()):
		if get_ground_type() != Grounds.Soil:
			till()
		plant(Entities.Pumpkin)
		if get_water() < 0.7:
			use_item(Items.Water)
		move(North)

def check_dead_column():
	for _ in range(get_world_size()):
		if get_entity_type() == Entities.Dead_Pumpkin:
			plant(Entities.Pumpkin)
			if get_water() < 0.7:
				use_item(Items.Water)
		move(North)

# 初始种植
for _ in range(get_world_size()):
	if not spawn_drone(plant_column):
		plant_column()
	move(East)

# 主循环
while True:
	# 并行检查枯萎南瓜
	for _ in range(get_world_size()):
		if not spawn_drone(check_dead_column):
			check_dead_column()
		move(East)
	
	# 检查是否可收获
	if can_harvest():
		harvest()
		
		# 并行重种
		for _ in range(get_world_size()):
			if not spawn_drone(plant_column):
				plant_column()
			move(East)