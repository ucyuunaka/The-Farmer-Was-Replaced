# 全尺寸-施肥刷取奇异物质
for i in range(get_world_size()):
	for j in range(get_world_size()):
		plant(Entities.Bush)
		move(North)
	move(East)

while True:
	for i in range(get_world_size()):
		for j in range(get_world_size()):
			if get_entity_type() == Entities.Bush:
				use_item(Items.Fertilizer)

			if can_harvest():
				harvest()
				plant(Entities.Bush)

			move(North)
		move(East)