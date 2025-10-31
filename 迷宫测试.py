# 22x22迷宫高效求解器 - 简洁版
# 遵循核心设计原则：信任游戏机制，最小代码量

def solve_maze_simple():
	tx, ty = measure()
	
	while get_entity_type() != Entities.Treasure:
		cx = get_pos_x()
		cy = get_pos_y()
		
		moved = False
		
		# 优先靠近宝藏
		if cx < tx and can_move(East):
			move(East)
			moved = True
		elif cx > tx and can_move(West):
			move(West)
			moved = True
		elif cy < ty and can_move(North):
			move(North)
			moved = True
		elif cy > ty and can_move(South):
			move(South)
			moved = True
		
		# 被墙挡住则随机尝试
		if not moved:
			for d in [North, East, South, West]:
				if can_move(d):
					move(d)
					break
	
	harvest()

def run_maze_farming(maze_count):
	size = get_world_size()
	substance_amount = size * 2**(num_unlocked(Unlocks.Mazes) - 1)
	
	# 初始化迷宫
	clear()
	plant(Entities.Bush)
	use_item(Items.Weird_Substance, substance_amount)
	
	# 循环求解
	for i in range(maze_count):
		solve_maze_simple()
		if i < maze_count - 1:
			use_item(Items.Weird_Substance, substance_amount)

# 执行300次迷宫
run_maze_farming(300)