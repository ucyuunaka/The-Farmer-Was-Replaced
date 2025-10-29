plant(Entities.Bush)
move(South)
plant(Entities.Bush)
move(South)
plant(Entities.Bush)

# 收获-重种
while True:
	move(South)
	if can_harvest():
		harvest()
		plant(Entities.Bush)