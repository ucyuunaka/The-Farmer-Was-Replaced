# t2.py - 修正版
set_world_size(8)

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

# 初始种植（只保留这一段）
for _ in range(get_world_size()):
	spawn_drone(plant_column)
	move(East)

harvest_count = 0
max_runs = 10
total_pumpkins = 0

while harvest_count < max_runs:
	for _ in range(get_world_size()):
		spawn_drone(check_dead_column)
		move(East)
	
	if can_harvest():
		initial = num_items(Items.Pumpkin)
		harvest()
		gained = num_items(Items.Pumpkin) - initial
		total_pumpkins = total_pumpkins + gained
		harvest_count = harvest_count + 1
		quick_print("第" + str(harvest_count) + "次收获: " + str(gained) + "个南瓜")
		
		for _ in range(get_world_size()):
			spawn_drone(plant_column)
			move(East)

quick_print("总产量: " + str(total_pumpkins))
quick_print("总收获次数: " + str(harvest_count))