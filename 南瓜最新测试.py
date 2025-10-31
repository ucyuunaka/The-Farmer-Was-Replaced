# ========== 工具函数 ==========

def goto(x, y):
	while get_pos_x() != x:
		move(East)
	while get_pos_y() != y:
		move(North)


def optimize_coords(coords):
	if not coords:
		return []
	
	# 按x坐标分组
	by_column = {}
	for x, y in coords:
		if x not in by_column:
			by_column[x] = []
		by_column[x].append(y)
	
	# 蛇形排序
	result = []
	columns = sorted(by_column.keys())
	for i, col in enumerate(columns):
		ys = sorted(by_column[col], reverse=(i % 2 == 1))
		result.extend([(col, y) for y in ys])
	
	return result


# ========== 种植模块 ==========

def plant_column():
	for _ in range(get_world_size()):
		if get_ground_type() != Grounds.Soil:
			till()
		plant(Entities.Pumpkin)
		move(North)


def parallel_plant():
	s = get_world_size()
	half = s // 2
	
	# 子无人机负责后半部分列
	def plant_back_half():
		for col in range(half, s):
			goto(col, 0)
			plant_column()
	
	# 派发子无人机
	drone = spawn_drone(plant_back_half)
	
	# 主无人机负责前半部分列
	for col in range(half):
		goto(col, 0)
		plant_column()
	
	# 等待子无人机完成
	if drone:
		wait_for(drone)
	else:
		# 派发失败，自己完成后半部分
		plant_back_half()


# ========== 检测模块 ==========

def check_position(x, y):
	goto(x, y)
	
	# 检查成熟度
	if not can_harvest():
		return ("UNRIPE", (x, y))
	
	# 已成熟，检查是否坏果
	if get_entity_type() == Entities.Dead_Pumpkin:
		# 坏果，立即重种
		if get_ground_type() != Grounds.Soil:
			till()
		plant(Entities.Pumpkin)
		return ("BAD", (x, y))
	
	return ("GOOD", (x, y))


def check_column(col_x):
	results = []
	for y in range(get_world_size()):
		status, coord = check_position(col_x, y)
		if status != "GOOD":  # 只记录BAD和UNRIPE
			results.append((status, coord))
	return results


def parallel_check_all():
	s = get_world_size()
	half = s // 2
	
	# 子无人机负责后半部分列
	def check_back_half():
		results = []
		for col in range(half, s):
			results.extend(check_column(col))
		return results
	
	# 派发子无人机
	drone = spawn_drone(check_back_half)
	
	# 主无人机负责前半部分列
	main_results = []
	for col in range(half):
		main_results.extend(check_column(col))
	
	# 等待子无人机结果
	if drone:
		sub_results = wait_for(drone)
		if sub_results:
			main_results.extend(sub_results)
	else:
		# 派发失败，自己完成后半部分
		main_results.extend(check_back_half())
	
	return main_results


def check_coords(coords):
	if not coords:
		return []
	
	# 蛇形路径优化
	optimized_path = optimize_coords(coords)
	
	results = []
	for x, y in optimized_path:
		status, coord = check_position(x, y)
		results.append((status, coord))
	
	return results


# ========== 记录库更新 ==========

def update_libraries(check_results, bad_set, unripe_set):
	for status, coord in check_results:
		if status == "UNRIPE":
			unripe_set.add(coord)
		elif status == "BAD":
			bad_set.add(coord)
			# 如果这个坐标之前在B库，移除（说明成熟后变成坏果）
			unripe_set.discard(coord)
		elif status == "GOOD":
			# 好果成熟，从两个库都移除
			bad_set.discard(coord)
			unripe_set.discard(coord)


# ========== 主循环 ==========

bad_set = set()      # A库：已知坏果
unripe_set = set()   # B库：未成熟坐标

while True:
	# ========== a. 全场种植 ==========
	parallel_plant()
	
	# 清空记录库（新一轮开始）
	bad_set = set()
	unripe_set = set()
	
	# ========== b. 全场检测建库 ==========
	check_results = parallel_check_all()
	update_libraries(check_results, bad_set, unripe_set)
	
	# ========== c. 坏果重检循环 ==========
	# 退出条件：A空 + B空 + 可收获
	while not (len(bad_set) == 0 and len(unripe_set) == 0 and can_harvest()):
		# 合并A库和B库，一次性检测
		all_coords = list(bad_set | unripe_set)
		
		if not all_coords:
			# 理论上不应该到这里（退出条件会先触发）
			# 但保险起见，避免死循环
			break
		
		# 检测所有需要关注的坐标
		check_results = check_coords(all_coords)
		
		# 更新记录库
		# 注意：这里需要先清空再重建，因为坐标状态可能变化
		old_bad = bad_set.copy()
		old_unripe = unripe_set.copy()
		bad_set = set()
		unripe_set = set()
		
		update_libraries(check_results, bad_set, unripe_set)
	
	# ========== d. 收获重启 ==========
	harvest()