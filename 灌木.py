# 全尺寸-灌木

def plant_column():
    for _ in range(get_world_size()):
        plant(Entities.Bush)
        move(North)

def harvest_and_replant_column():
    for _ in range(get_world_size()):
        if can_harvest():
            harvest()
            plant(Entities.Bush)
        move(North)

for _ in range(get_world_size()):
    if not spawn_drone(plant_column):
        plant_column()
    move(East)

while True:
    for _ in range(get_world_size()):
        if not spawn_drone(harvest_and_replant_column):
            harvest_and_replant_column()
        move(East)