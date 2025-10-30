# 全尺寸-草料收获

clear()

def harvest_column():
    for _ in range(get_world_size()):
        if can_harvest():
            harvest()
        move(North)

while True:
    for _ in range(get_world_size()):
        if not spawn_drone(harvest_column):
            harvest_column()
        move(East)