# 迷宫寻宝算法 - 简化版本


# 主循环 - 确保持续运行
while True:
	# 检查是否在灌木上，如果不是则种植
	if get_entity_type() != Entities.Bush:
		if can_harvest():
			harvest()
		plant(Entities.Bush)
		use_item(Items.Weird_Substance)  # 生成迷宫

	# 测量宝藏位置
	treasure_pos = measure()
	treasure_x = treasure_pos[0]
	treasure_y = treasure_pos[1]

	# 简单寻路：向宝藏方向移动
	current_x = get_pos_x()
	current_y = get_pos_y()

	# 优先向东移动
	if treasure_x > current_x and can_move(East):
		move(East)
	# 向西移动
	elif treasure_x < current_x and can_move(West):
		move(West)
	# 向北移动
	elif treasure_y > current_y and can_move(North):
		move(North)
	# 向南移动
	elif treasure_y < current_y and can_move(South):
		move(South)
	# 如果都不能移动，随机尝试一个方向
	elif can_move(East):
		move(East)
	elif can_move(North):
		move(North)
	elif can_move(West):
		move(West)
	elif can_move(South):
		move(South)

	# 检查是否找到宝藏
	if get_entity_type() == Entities.Treasure:
		harvest()
		quick_print("收获黄金:", num_items(Items.Gold))
		# 继续寻找下一个宝藏