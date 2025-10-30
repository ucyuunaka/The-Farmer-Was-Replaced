# 全尺寸-南瓜（记忆优化版-无goto）

def goto(x, y):
	while get_pos_x() != x:
		move(East)
	while get_pos_y() != y:
		move(North)

def plant_column():
	for _ in range(get_world_size()):
		if get_ground_type() != Grounds.Soil:
			till()
		plant(Entities.Pumpkin)
		move(North)

# 初始种植
for _ in range(get_world_size()):
	if not spawn_drone(plant_column):
		plant_column()
	move(East)

bad_coords = []

while True:
	if can_harvest():
		# 可能形成巨型南瓜，扫描坏果
		new_bad = []
		for x in range(get_world_size()):
			for y in range(get_world_size()):
				goto(x, y)
				if get_entity_type() == Entities.Dead_Pumpkin:
					new_bad.append((x, y))
		
		if len(new_bad) == 0:
			# 全场完美，收获
			harvest()
			for _ in range(get_world_size()):
				if not spawn_drone(plant_column):
					plant_column()
				move(East)
			bad_coords = []
		else:
			# 并行修复坏果
			for i in range(len(new_bad)):
				x, y = new_bad[i]
				def fix_task(px=x, py=y):
					goto(px, py)
					if get_ground_type() != Grounds.Soil:
						till()
					plant(Entities.Pumpkin)
				
				if not spawn_drone(fix_task):
					fix_task()
			bad_coords = new_bad
	else:
		# 未成熟阶段
		if len(bad_coords) == 0:
			# 首次全场扫描
			for x in range(get_world_size()):
				for y in range(get_world_size()):
					goto(x, y)
					if get_entity_type() == Entities.Dead_Pumpkin:
						bad_coords.append((x, y))
						if get_ground_type() != Grounds.Soil:
							till()
						plant(Entities.Pumpkin)
		else:
			# 只检查记录的坏果位置
			new_bad = []
			for i in range(len(bad_coords)):
				x, y = bad_coords[i]
				goto(x, y)
				if get_entity_type() == Entities.Dead_Pumpkin:
					new_bad.append((x, y))
					if get_ground_type() != Grounds.Soil:
						till()
					plant(Entities.Pumpkin)
			bad_coords = new_bad