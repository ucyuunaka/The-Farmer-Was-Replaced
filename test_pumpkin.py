# test_pumpkin.py - 修复版

def test_efficiency():
	print("南瓜收获方案效率测试")
	
	test_runs = 10
	world_size = 12
	
	print("测试方案1 (简洁版)...")
	time_v1 = simulate("t1", Unlocks, {Items.Carrot: 1000000, Items.Hay: 1000}, {"max_runs": test_runs}, 42, 32)
	
	print("测试方案2 (多无人机版)...")
	time_v2 = simulate("t2", Unlocks, {Items.Carrot: 1000000, Items.Hay: 1000}, {"max_runs": test_runs}, 42, 32)
	
	# 理论产量：每次收获整个8x8方形
	pumpkins_per_harvest = world_size * world_size * world_size
	total_pumpkins = pumpkins_per_harvest * test_runs
	
	efficiency_v1 = total_pumpkins / time_v1
	efficiency_v2 = total_pumpkins / time_v2
	
	# 手动四舍五入
	time_v1_display = (time_v1 * 100) // 100
	time_v2_display = (time_v2 * 100) // 100
	eff_v1_display = (efficiency_v1 * 100) // 100
	eff_v2_display = (efficiency_v2 * 100) // 100
	
	print("")
	print("测试结果 (田地:" + str(world_size) + "x" + str(world_size) + ")")
	print("方案1:")
	print("  总时间: " + str(time_v1_display) + "秒")
	print("  理论产量: " + str(total_pumpkins) + "个南瓜")
	print("  效率: " + str(eff_v1_display) + " 南瓜/秒")
	print("")
	print("方案2:")
	print("  总时间: " + str(time_v2_display) + "秒")
	print("  理论产量: " + str(total_pumpkins) + "个南瓜")
	print("  效率: " + str(eff_v2_display) + " 南瓜/秒")
	print("")
	
	if efficiency_v1 > efficiency_v2:
		improvement = ((efficiency_v1 - efficiency_v2) / efficiency_v2) * 100
		print("方案1更高效，提升 " + str((improvement * 10) // 10) + "%")
	else:
		improvement = ((efficiency_v2 - efficiency_v1) / efficiency_v1) * 100
		print("方案2更高效，提升 " + str((improvement * 10) // 10) + "%")

test_efficiency()