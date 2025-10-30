# t1.py - 添加停止条件

# 初始种植
for _ in range(get_world_size()):
	for _ in range(get_world_size()):
		till()
		plant(Entities.Pumpkin)
		move(North)
	move(East)

# 主循环 - 添加计数器
harvest_count = 0
max_runs = 5  # 默认5次，可通过globals覆盖

while harvest_count < max_runs:
	# 扫描并重种枯萎的南瓜
	for _ in range(get_world_size()):
		for _ in range(get_world_size()):
			if get_entity_type() == Entities.Dead_Pumpkin:
				plant(Entities.Pumpkin)
			move(North)
		move(East)
	
	# 当整个农场成熟时收获
	if can_harvest():
		harvest()
		harvest_count += 1
		quick_print("收获次数: " + str(harvest_count))
		
		# 重新种植
		for _ in range(get_world_size()):
			for _ in range(get_world_size()):
				till()
				plant(Entities.Pumpkin)
				move(North)
			move(East)