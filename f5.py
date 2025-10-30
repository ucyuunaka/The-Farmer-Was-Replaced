# 高级迷宫寻宝算法 - 12x12固定迷宫优化版本

# 确保生成12x12固定大小迷宫
set_world_size(12)

# 清理当前地块并准备迷宫生成
if can_harvest():
	harvest()
	
# 种植迷宫生成基础植物
plant(Entities.Bush)

# 生成12x12迷宫
use_item(Items.Weird_Substance)

# ===== 寻宝算法核心 =====

# 第一步：测量宝藏位置（关键功能）
treasure_pos = measure()
treasure_x, treasure_y = treasure_pos
quick_print("宝藏位置:", treasure_pos)

# 第二步：迷宫探索与寻路算法
# 使用右手法则沿墙探索，结合已知宝藏位置进行目标导向搜索

def move_towards_target(target_x, target_y):
	"""向目标位置移动的智能函数"""
	current_x, current_y = get_pos_x(), get_pos_y()
	
	# 简单的坐标差移动策略
	while (current_x, current_y) != (target_x, target_y):
		# 优先水平移动
		if current_x < target_x and can_move(East):
			move(East)
			current_x += 1
		elif current_x > target_x and can_move(West):
			move(West)
			current_x -= 1
		# 垂直移动
		elif current_y < target_y and can_move(North):
			move(North)
			current_y += 1
		elif current_y > target_y and can_move(South):
			move(South)
			current_y -= 1
		else:
			# 如果直接移动受阻，尝试右手法则探索
			break

# 右手法则迷宫探索
def explore_maze_to_treasure():
	"""使用右手法则探索迷宫直到找到宝藏"""
	directions = [North, East, South, West]  # 右手优先顺序
	current_dir_index = 0
	
	steps = 0
	max_steps = 200  # 防止无限循环
	
	while steps < max_steps:
		# 检查是否到达宝藏
		if get_entity_type() == Entities.Treasure:
			quick_print("找到宝藏！用时", steps, "步")
			harvest()
			quick_print("收获黄金数量:", num_items(Items.Gold))
			return True
		
		# 检查当前方向是否可移动
		current_dir = directions[current_dir_index]
		if can_move(current_dir):
			move(current_dir)
			# 右转（顺时针）
			current_dir_index = (current_dir_index + 1) % 4
		else:
			# 如果不能移动，左转寻找新路径
			current_dir_index = (current_dir_index - 1) % 4
		
		steps += 1
	
	quick_print("未能在限定步数内找到宝藏")
	return False

# 主要寻宝流程
try:
	# 策略1：直接向宝藏位置移动
	move_towards_target(treasure_x, treasure_y)
	
	# 如果到达宝藏位置，收获
	if get_entity_type() == Entities.Treasure:
		quick_print("直接到达宝藏！")
		harvest()
		quick_print("收获黄金数量:", num_items(Items.Gold))
	else:
		# 策略2：使用迷宫探索算法
		quick_print("开始迷宫探索...")
		explore_maze_to_treasure()
		
except Exception as e:
	quick_print("寻宝过程中出现错误:", e)
	# 备用方案：全图遍历
	for i in range(12):
		for j in range(12):
			if get_entity_type() == Entities.Treasure:
				harvest()
				quick_print("备用方案找到宝藏！")
			move(North)
		move(East)