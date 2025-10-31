# 全尺寸-灌木-高级优化版

# 移动到指定坐标的函数
def move_to_position(target_x, target_y):
	# 获取当前位置
	current_x = get_pos_x()
	current_y = get_pos_y()
	
	# 计算需要移动的方向和距离
	while current_x != target_x:
		if current_x < target_x:
			move(East)
			current_x += 1
		else:
			move(West)
			current_x -= 1
	
	while current_y != target_y:
		if current_y < target_y:
			move(North)
			current_y += 1
		else:
			move(South)
			current_y -= 1

# 处理单个地块的函数
def process_tile():
	# 如果可以收获，先收获
	if can_harvest():
		harvest()
	
	# 种植灌木
	plant(Entities.Bush)
	
	# 检查伴生植物信息
	companion = get_companion()
	if companion:
		plant_type, (x, y) = companion
		# 保存当前位置
		original_x = get_pos_x()
		original_y = get_pos_y()
		# 移动到伴生植物位置并种植
		move_to_position(x, y)
		if not get_entity_type():
			if plant_type == Entities.Carrot:
				# 胡萝卜需要先耕地，检查地面类型
				if get_ground_type() == Grounds.Grassland:
					till()  # 草地变土壤
			plant(plant_type)
		# 返回原位置
		move_to_position(original_x, original_y)
	
	# 浇水以加速生长
	if num_items(Items.Water) > 0 and get_water() < 0.75:
		use_item(Items.Water)

# 处理指定行的函数
def process_row(row, direction):
	# 移动到指定行的起始位置
	move_to_position(0, row)
	
	# 根据方向处理行
	if direction == "east":
		for _ in range(get_world_size()):
			process_tile()
			if get_pos_x() < get_world_size() - 1:
				move(East)
	else:  # west
		move_to_position(get_world_size() - 1, row)
		for _ in range(get_world_size()):
			process_tile()
			if get_pos_x() > 0:
				move(West)

# 无人机工作函数
def drone_work(start_row, rows_per_drone):
	current_row = start_row
	direction = "east"  # 初始方向向东
	
	while True:
		# 处理当前行
		process_row(current_row, direction)
		
		# 切换方向
		if direction == "east":
			direction = "west"
		else:
			direction = "east"
		
		# 移动到下一行
		current_row += 1
		if current_row >= start_row + rows_per_drone:
			current_row = start_row  # 回到起始行

# 为不同无人机创建特定的工作函数
def create_drone_work_function(sr, rpd):
	def drone_function():
		drone_work(sr, rpd)
	return drone_function

# 初始化农场并分配无人机工作
def initialize_farm():
	world_size = get_world_size()
	max_drone_count = max_drones()
	
	# 计算每架无人机负责的行数
	rows_per_drone = (world_size + max_drone_count - 1) // max_drone_count
	
	# 为每架无人机分配工作
	for i in range(max_drone_count):
		start_row = i * rows_per_drone
		if start_row < world_size:
			# 生成新无人机
			drone_func = create_drone_work_function(start_row, rows_per_drone)
			spawn_drone(drone_func)
			
			# 等待一段时间让新无人机启动
			for _ in range(10):
				pass
	
	# 主无人机也开始工作
	drone_work(0, rows_per_drone)

# 主程序
if __name__ == "__main__":
	# 初始化农场并开始工作
	initialize_farm()