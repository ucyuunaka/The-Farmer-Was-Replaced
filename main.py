# 遍历整个农场收获所有作物并处理死南瓜
for i in range(get_world_size()):
	for j in range(get_world_size()):
		if can_harvest():
			harvest()
		elif get_entity_type() == Entities.Dead_Pumpkin:
			# 清除死南瓜：种植新植物会自动移除死南瓜
			plant(Entities.Grass)  # 种植草来清除死南瓜
		move(North)
	move(East)