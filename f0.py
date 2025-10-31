# 灌木种植优化版
# 每架无人机负责间隔的多行，避免重叠并充分利用所有无人机

def work_on_assigned_rows():
	total_drones = max_drones()
	world_size = get_world_size()
	start_row = get_pos_y()
	
	while True:
		row = start_row
		
		while row < world_size:
			# 移动到目标行
			while get_pos_y() != row:
				if get_pos_y() < row:
					move(North)
				else:
					move(South)
			
			# 移动到行首
			while get_pos_x() > 0:
				move(West)
			
			# 向右处理整行
			for _ in range(world_size - 1):
				if can_harvest():
					harvest()
				plant(Entities.Bush)
				move(East)
			
			# 处理最后一格
			if can_harvest():
				harvest()
			plant(Entities.Bush)
			
			# 移到下一个分配给此无人机的行
			row = row + total_drones

def main():
	world_size = get_world_size()
	num_drones = min(world_size, max_drones())
	
	# 为每行生成无人机（如果无人机数量足够）
	# 或生成所有可用无人机，让它们分担所有行
	for i in range(num_drones):
		# 移动主无人机到第i行作为起始行
		for _ in range(i):
			move(North)
		
		# 在该位置生成工作无人机
		spawn_drone(work_on_assigned_rows)
		
		# 主无人机返回原点继续生成下一个
		for _ in range(i):
			move(South)

main()