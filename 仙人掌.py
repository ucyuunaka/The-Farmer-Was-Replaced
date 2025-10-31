# 全尺寸-仙人掌排序（多无人机版）

clear()
s = get_world_size()

# 循环浇水函数
def water_column():
	for _ in range(s):
		if get_water() < 0.4:
			use_item(Items.Water)
		move(North)

# 初始种植 - 多无人机并行
def plant_column():
	for _ in range(s):
		till()
		plant(Entities.Cactus)
		if get_water() < 0.4:
			use_item(Items.Water)
		move(North)

for _ in range(s):
	if not spawn_drone(plant_column):
		plant_column()
	move(East)

while True:
	# 循环浇水 - 多无人机并行
	for _ in range(s):
		if not spawn_drone(water_column):
			water_column()
		move(East)
	
	# 排序阶段 - 保持单无人机
	for round in range(s):
		for i in range(s):
			for j in range(s):
				if get_pos_x() < s - 1:
					c = measure()
					e = measure(East)
					if c != None and e != None and c > e:
						swap(East)
				move(North)
			move(East)
	
	for round in range(s):
		for i in range(s):
			for j in range(s):
				if get_pos_y() < s - 1:
					c = measure()
					n = measure(North)
					if c != None and n != None and c > n:
						swap(North)
				move(North)
			move(East)
	
	all_ready = False
	while not all_ready:
		all_ready = True
		for i in range(s):
			for j in range(s):
				if get_entity_type() == Entities.Cactus:
					if not can_harvest():
						all_ready = False
				move(North)
			move(East)
	
	before = num_items(Items.Cactus)
	
	harvested = False
	for i in range(s):
		for j in range(s):
			if can_harvest():
				harvest()
				harvested = True
				break
		if harvested:
			break
		move(North)
	move(East)
	
	gained = num_items(Items.Cactus) - before
	min_chain = s * s * 6 // 10
	min_yield = min_chain * min_chain
	
	quick_print("Gained:", gained, "Target:", min_yield)
	
	if gained < min_yield:
		quick_print("Replanting all...")
		
		def replant_column():
			for _ in range(s):
				if can_harvest():
					harvest()
				till()
				plant(Entities.Cactus)
				if get_water() < 0.4:
					use_item(Items.Water)
				move(North)
		
		for _ in range(s):
			if not spawn_drone(replant_column):
				replant_column()
			move(East)
		
		# 收获后循环浇水
		for _ in range(s):
			if not spawn_drone(water_column):
				water_column()
			move(East)
	else:
		quick_print("Refilling gaps...")
		
		def refill_column():
			for _ in range(s):
				if get_entity_type() != Entities.Cactus:
					till()
					plant(Entities.Cactus)
					if get_water() < 0.4:
						use_item(Items.Water)
				elif get_water() < 0.4:
					use_item(Items.Water)
				move(North)
		
		for _ in range(s):
			if not spawn_drone(refill_column):
				refill_column()
			move(East)
		
		# 收获后循环浇水
		for _ in range(s):
			if not spawn_drone(water_column):
				water_column()
			move(East)