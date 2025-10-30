# test_pumpkin.py - 修正版

def test_efficiency():
	print("南瓜收获方案效率测试")
	
	test_runs = 10
	world_size = 8  # 测试田地大小
	
	print("测试方案1 (简洁版)...")
	time_v1 = simulate("t1", Unlocks, {Items.Carrot: 1000000, Items.Hay: 1000}, {"max_runs": test_runs}, 42, 32)
	
	print("测试方案2 (多无人机版)...")
	time_v2 = simulate("t2", Unlocks, {Items.Carrot: 1000000, Items.Hay: 1000}, {"max_runs": test_runs}, 42, 32)
	
	pumpkins_per_harvest = world_size * world_size * world_size
	total_pumpkins = pumpkins_per_harvest * test_runs
	
	efficiency_v1 = total_pumpkins / time_v1
	efficiency_v2 = total_pumpkins / time_v2
	
	print("")
	print("测试结果 (田地:" + str(world_size) + "x" + str(world_size) + ")")
	print("方案1:")
	print("  总时间: " + str(round(time_v1, 2)) + "秒")
	print("  总产量: " + str(total_pumpkins) + "个南瓜")
	print("  效率: " + str(round(efficiency_v1, 2)) + " 南瓜/秒")
	print("")
	print("方案2:")
	print("  总时间: " + str(round(time_v2, 2)) + "秒")
	print("  总产量: " + str(total_pumpkins) + "个南瓜")
	print("  效率: " + str(round(efficiency_v2, 2)) + " 南瓜/秒")
	print("")
	
	if efficiency_v1 > efficiency_v2:
		improvement = ((efficiency_v1 - efficiency_v2) / efficiency_v2) * 100
		print("方案1更高效，提升 " + str(round(improvement, 1)) + "%")
	else:
		improvement = ((efficiency_v2 - efficiency_v1) / efficiency_v1) * 100
		print("方案2更高效，提升 " + str(round(improvement, 1)) + "%")

test_efficiency()