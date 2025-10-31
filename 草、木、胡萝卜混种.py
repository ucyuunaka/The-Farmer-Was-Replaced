# 混合种植 - 草、胡萝卜、灌木（带自动浇水）

def process_column():
	col = get_pos_x()
	crop_index = col % 3
	for _ in range(get_world_size()):
		if can_harvest():
			harvest()
		if crop_index == 0:
			plant(Entities.Grass)
		elif crop_index == 1:
			if get_ground_type() != Grounds.Soil:
				till()
			plant(Entities.Carrot)
			# 检查胡萝卜地块含水量，低于0.5时浇水
			if get_water() < 0.7:
				use_item(Items.Water)
		else:
			plant(Entities.Bush)
		move(North)

while True:
	for _ in range(get_world_size()):
		if not spawn_drone(process_column):
			process_column()
		move(East)