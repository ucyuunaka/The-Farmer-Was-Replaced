# test_pumpkin.py - 南瓜方案对比测试
from __builtins__ import *
def test_pumpkin_strategies():
	"""对比测试两个南瓜种植方案"""
	
	print("=" * 60)
	print("🎃 南瓜收获方案性能测试")
	print("=" * 60)
	
	# 测试配置
	test_config = {
		"unlocks": Unlocks,  # 全部解锁
		"items": {
			Items.Carrot: 50000,  # 足够的胡萝卜（南瓜需要1个胡萝卜种植）
			Items.Hay: 1000       # 一些干草
		},
		"seed": 42,  # 固定种子确保公平对比
		"speedup": 32  # 32倍速加快测试
	}
	
	# 定义测试时长（通过globals传递）
	# 让脚本运行一定时间后自动停止
	test_globals = {
		"max_runs": 5  # 运行5个收获周期
	}
	
	print("\n📝 测试配置:")
	print(f"  - 初始胡萝卜: {test_config['items'][Items.Carrot]}")
	print(f"  - 随机种子: {test_config['seed']}")
	print(f"  - 加速倍率: {test_config['speedup']}x")
	print(f"  - 测试周期: {test_globals['max_runs']} 次收获")
	
	# 测试方案1：简洁版
	print("\n" + "=" * 60)
	print("🧪 测试方案1: 简洁高效版")
	print("=" * 60)
	
	time_v1 = simulate(
		filename="t1",
		sim_unlocks=test_config["unlocks"],
		sim_items=test_config["items"],
		sim_globals=test_globals,
		seed=test_config["seed"],
		speedup=test_config["speedup"]
	)
	
	print(f"✅ 方案1完成 - 耗时: {time_v1:.2f}秒")
	
	# 测试方案2：多无人机版
	print("\n" + "=" * 60)
	print("🧪 测试方案2: 多无人机并行版")
	print("=" * 60)
	
	time_v2 = simulate(
		filename="t2",
		sim_unlocks=test_config["unlocks"],
		sim_items=test_config["items"],
		sim_globals=test_globals,
		seed=test_config["seed"],  # 相同种子
		speedup=test_config["speedup"]
	)
	
	print(f"✅ 方案2完成 - 耗时: {time_v2:.2f}秒")
	
	# 性能对比分析
	print("\n" + "=" * 60)
	print("📊 性能对比分析")
	print("=" * 60)
	
	print(f"\n方案1 (简洁版):     {time_v1:.2f}秒")
	print(f"方案2 (多无人机版): {time_v2:.2f}秒")
	
	if time_v1 < time_v2:
		improvement = ((time_v2 - time_v1) / time_v2) * 100
		print(f"\n🏆 方案1更快! 提升 {improvement:.1f}%")
	elif time_v2 < time_v1:
		improvement = ((time_v1 - time_v2) / time_v1) * 100
		print(f"\n🏆 方案2更快! 提升 {improvement:.1f}%")
	else:
		print(f"\n⚖️ 两个方案速度相当")
	
	# 推荐
	print("\n" + "=" * 60)
	print("💡 推荐方案")
	print("=" * 60)
	
	if abs(time_v1 - time_v2) < time_v1 * 0.1:  # 性能差异小于10%
		print("两个方案性能接近，推荐 方案1（代码更简洁）")
	elif time_v1 < time_v2:
		print("方案1 性能更优且代码简洁，强烈推荐！")
	else:
		print("方案2 性能更优，适合追求极致效率的场景")
	
	print("\n" + "=" * 60)

# 运行测试
test_pumpkin_strategies()