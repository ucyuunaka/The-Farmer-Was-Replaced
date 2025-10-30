# t2.py - 添加停止条件

def plant_column():
	for _ in range(get_world_size()):
		till()
		plant(Entities.Pumpkin)
		move(North)

def check_dead_column():
	for _ in range(get_world_size()):
		if get_entity_type() == Entities.Dead_Pumpkin:
			plant(Entities.Pumpkin)
		move(North)

# 初始种植
for _ in range(get_world_size()):
	spawn_drone(plant_column)
	move(East)

# 主循环
harvest_count = 0
max_runs = 5

while harvest_count < max_runs:
	# 并行检查枯萎
	for _ in range(get_world_size()):
		spawn_drone(check_dead_column)
		move(East)
	
	# 检查收获
	if can_harvest():
		harvest()
		harvest_count += 1
		quick_print("收获次数: " + str(harvest_count))
		
		# 并行重种
		for _ in range(get_world_size()):
			spawn_drone(plant_column)
			move(East)