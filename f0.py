# 全尺寸-仙人掌排序（充分优化版）

clear()
s = get_world_size()

def plant_column():
	for _ in range(s):
		till()
		plant(Entities.Cactus)
		move(North)

for _ in range(s):
	if not spawn_drone(plant_column):
		plant_column()
	move(East)

while True:
	# 横向排序 - 按行并行（关键优化！）
	def sort_row_east():
		for _ in range(s):
			if get_pos_x() < s - 1:
				c = measure()
				e = measure(East)
				if c != None and e != None and c > e:
					swap(East)
			move(East)
	
	for round in range(s):
		for _ in range(s):
			if not spawn_drone(sort_row_east):
				sort_row_east()
			move(North)
	
	# 纵向排序 - 按列并行（关键优化！）
	def sort_column_north():
		for _ in range(s):
			if get_pos_y() < s - 1:
				c = measure()
				n = measure(North)
				if c != None and n != None and c > n:
					swap(North)
			move(North)
	
	for round in range(s):
		for _ in range(s):
			if not spawn_drone(sort_column_north):
				sort_column_north()
			move(East)
	
	# 等待成熟 - 保持简单
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
	min_yield = min_chain * min_yield
	
	quick_print("Gained:", gained, "Target:", min_yield)
	
	if gained < min_yield:
		quick_print("Replanting all...")
		
		def replant_column():
			for _ in range(s):
				if can_harvest():
					harvest()
				till()
				plant(Entities.Cactus)
				move(North)
		
		for _ in range(s):
			if not spawn_drone(replant_column):
				replant_column()
			move(East)
	else:
		quick_print("Refilling gaps...")
		
		def refill_column():
			for _ in range(s):
				if get_entity_type() != Entities.Cactus:
					till()
					plant(Entities.Cactus)
				move(North)
		
		for _ in range(s):
			if not spawn_drone(refill_column):
				refill_column()
			move(East)