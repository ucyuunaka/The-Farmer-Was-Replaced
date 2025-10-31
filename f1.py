# 全尺寸-灌木-优化版

# 持续处理一行的函数，采用蛇形路径
def process_snake_path():
	# 无限循环，使无人机不会消失
	while True:
		# 从西向东处理当前行
		for _ in range(get_world_size() - 1):
			if can_harvest():
				harvest()
			plant(Entities.Bush)
			move(East)
		
		# 处理最后一格
		if can_harvest():
			harvest()
		plant(Entities.Bush)
		
		# 移到下一行
		move(North)
		
		# 从东向西处理下一行
		for _ in range(get_world_size() - 1):
			if can_harvest():
				harvest()
			plant(Entities.Bush)
			move(West)
		
		# 处理最后一格
		if can_harvest():
			harvest()
		plant(Entities.Bush)
		
		# 如果不是最后一行，移到下一行
		if get_pos_y() < get_world_size() - 1:
			move(North)

# 初始化农场，生成多架无人机
def initialize_farm():
	# 计算需要的无人机数量，每两行一架无人机
	drones_needed = (get_world_size() + 1) // 2
	
	# 为每两行生成一个无人机
	for i in range(drones_needed):
		# 移到起始位置
		for _ in range(i):
			move(North)
		
		# 生成无人机
		spawn_drone(process_snake_path)
		
		# 返回原点
		for _ in range(i):
			move(South)

# 初始化农场
initialize_farm()

# 主无人机也进入无限循环，处理第一行
process_snake_path()