for i in range(get_world_size()):
	for j in range(get_world_size()):
		if get_ground_type() != Grounds.Soil:
			till()

		if can_harvest():
			harvest()

		plant(Entities.Cactus)

		move(North)
	move(East)

while True:
	for i in range(get_world_size()):
		for j in range(get_world_size()):
			if can_harvest():
				harvest()

				if get_ground_type() != Grounds.Soil:
					till()
				plant(Entities.Cactus)

			if get_entity_type() == Entities.Cactus:
				current_size = measure()
				if current_size != None:
					current_x = get_pos_x()
					world_size = get_world_size()

					if current_x < world_size - 1:
						east_size = measure(East)

						if east_size != None and current_size > east_size:
							swap(East)

			move(North)
		move(East)