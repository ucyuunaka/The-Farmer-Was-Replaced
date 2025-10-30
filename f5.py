# 迷宫

if can_harvest():
	harvest()
plant(Entities.Bush)

use_item(Items.Weird_Substance)

for i in range(get_world_size()):
	for j in range(get_world_size()):
		if get_entity_type() == Entities.Treasure:
			harvest()

		move(North)

	move(East)