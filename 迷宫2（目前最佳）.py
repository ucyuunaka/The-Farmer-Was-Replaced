while True:
	if get_entity_type() != Entities.Bush:
		if can_harvest():
			harvest()
		plant(Entities.Bush)
	
	substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
	
	use_item(Items.Weird_Substance, substance)
	
	directions = [North, East, South, West]
	direction_index = 0
	
	while get_entity_type() != Entities.Treasure:
		right_index = (direction_index + 1) % 4
		forward_index = direction_index
		left_index = (direction_index - 1) % 4
		back_index = (direction_index + 2) % 4
		
		if can_move(directions[right_index]):
			move(directions[right_index])
			direction_index = right_index
		elif can_move(directions[forward_index]):
			move(directions[forward_index])
		elif can_move(directions[left_index]):
			move(directions[left_index])
			direction_index = left_index
		else:
			move(directions[back_index])
			direction_index = back_index
	
	harvest()