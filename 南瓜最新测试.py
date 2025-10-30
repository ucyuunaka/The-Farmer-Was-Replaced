# 全尺寸-南瓜（终极优化版）

def plant_column():
	for _ in range(get_world_size()):
		if get_ground_type() != Grounds.Soil:
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
	if not spawn_drone(plant_column):
		plant_column()
	move(East)

# 主循环
while True:
	if can_harvest():
		# 可能形成巨型南瓜，逐列检查
		found_dead = False
		for _ in range(get_world_size()):
			if can_harvest():
				# 这一列完美，跳过
				pass
			else:
				# 这一列有问题，修复
				if not spawn_drone(check_dead_column):
					check_dead_column()
				found_dead = True
			move(East)
		
		if not found_dead:
			# 全场完美，收获
			harvest()
			# 重种
			for _ in range(get_world_size()):
				if not spawn_drone(plant_column):
					plant_column()
				move(East)
	else:
		# 还没成熟，修复坏果
		for _ in range(get_world_size()):
			if not spawn_drone(check_dead_column):
				check_dead_column()
			move(East)