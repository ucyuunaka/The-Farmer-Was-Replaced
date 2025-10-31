# 灌木效率比较测试 - 比较原始版本和优化版本的生产效率

# 测试参数
test_time = 300  # 5分钟（秒）
max_speedup = 64  # 最大加速倍率

# 运行测试
print("开始灌木效率比较测试...")
print("测试时间: " + str(test_time) + "秒")
print("加速倍率: " + str(max_speedup) + "倍")
print("==================================================")

# 测试原始版本
print("测试原始版本...")
original_time = simulate("f1", Unlocks, {Items.Water: 1000, Items.Fertilizer: 100}, {"test_time": test_time}, 0, max_speedup)
print("原始版本运行时间: " + str(original_time) + "秒")

# 测试优化版本
print("\n测试优化版本...")
optimized_time = simulate("f2", Unlocks, {Items.Water: 1000, Items.Fertilizer: 100}, {"test_time": test_time}, 0, max_speedup)
print("优化版本运行时间: " + str(optimized_time) + "秒")

# 比较结果
print("\n" + "==================================================")
print("效率比较结果:")

if original_time > 0 and optimized_time > 0:
	time_difference = original_time - optimized_time
	time_ratio = optimized_time / original_time
	
	print("原始版本用时: " + str(round(original_time, 2)) + "秒")
	print("优化版本用时: " + str(round(optimized_time, 2)) + "秒")
	print("时间差: " + str(round(time_difference, 2)) + "秒")
	print("时间比率: " + str(round(time_ratio, 2)))
	
	if time_difference > 0:
		improvement = (1 - time_ratio) * 100
		print("优化版本比原始版本快 " + str(round(time_difference, 2)) + "秒 (" + str(round(improvement, 2)) + "%)")
	else:
		regression = (time_ratio - 1) * 100
		print("原始版本比优化版本快 " + str(round(-time_difference, 2)) + "秒 (" + str(round(regression, 2)) + "%)")
else:
	print("无法比较，因为某个版本的运行时间为0")