# 全尺寸-仙人掌排序

s = get_world_size()

for i in range(s):
	for j in range(s):
		if can_harvest():
			harvest()
		till()
		plant(Entities.Cactus)
		move(North)
	move(East)

while True:
	
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
		for i in range(s):
			for j in range(s):
				if can_harvest():
					harvest()
				till()
				plant(Entities.Cactus)
				move(North)
			move(East)
	else:
		quick_print("Refilling gaps...")
		for i in range(s):
			for j in range(s):
				if get_entity_type() != Entities.Cactus:
					till()
					plant(Entities.Cactus)
				move(North)
			move(East)