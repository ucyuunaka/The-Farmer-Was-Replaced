# 3×3农场灌木

for i in range(get_world_size()):
    for j in range(get_world_size()):
        plant(Entities.Bush)
        move(North)
    move(East)

while True:
    for i in range(get_world_size()):
        for j in range(get_world_size()):
            if can_harvest():
                harvest()
                plant(Entities.Bush)
            move(North)
        move(East)