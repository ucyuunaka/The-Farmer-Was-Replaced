# t1.py - 简化修复版
set_world_size(12)

# 初始种植
for _ in range(get_world_size()):
	for _ in range(get_world_size()):
		till()
		plant(Entities.Pumpkin)
		move(North)
	move(East)

harvest_count = 0
max_runs = 10

while harvest_count < max_runs:
	# 简单扫描枯萎
	for _ in range(get_world_size()):
		for _ in range(get_world_size()):
			if get_entity_type() == Entities.Dead_Pumpkin:
				plant(Entities.Pumpkin)
			move(North)
		move(East)
	
	# 简单检查收获
	if can_harvest():
		harvest()
		harvest_count = harvest_count + 1
		quick_print("第" + str(harvest_count) + "次收获")
		
		# 重新种植
		for _ in range(get_world_size()):
			for _ in range(get_world_size()):
				if get_ground_type() != Grounds.Soil:
					till()
				plant(Entities.Pumpkin)
				move(North)
			move(East)

quick_print("总收获次数: " + str(harvest_count))