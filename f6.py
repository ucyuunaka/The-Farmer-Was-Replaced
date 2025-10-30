# 全尺寸-仙人掌自动化种植与收获脚本
# 仙人掌特性：连锁收获、尺寸排序、产量平方机制

"""
仙人掌种植收获脚本详解：
- 产量机制：收获n个仙人掌获得 n² 个仙人掌物品（指数增长！）
- 生长时间：平均1秒（0.8-1.2秒随机波动）
- 尺寸系统：10种不同尺寸（0-9），随机生成
- 连锁收获：相邻且按特定规则排序的仙人掌会连锁收获
- 排序规则：North/East方向 >= 自身，South/West方向 <= 自身
- 地形要求：必须种植在土壤(Grounds.Soil)上
- 兼容性：处理原有物品，确保在任何农场状态下都能正常运行
"""

# 农场清理和初始种植阶段
# 首先清理农场，然后在整个农场种植仙人掌
for i in range(get_world_size()):           # 外层循环：遍历行（东西方向）
	for j in range(get_world_size()):       # 内层循环：遍历列（南北方向）
		# 第一步：确保地形为土壤
		if get_ground_type() != Grounds.Soil:
			till()                          # 耕地：将草地转换为土壤

		# 第二步：处理原有物品（关键改进）
		# 先检查是否有可收获的原有物品
		if can_harvest():
			harvest()                       # 收获原有物品，清理地块

		# 第三步：种植仙人掌
		# plant()会自动检查当前位置是否为空地
		# 如果仍有原有物品（如死南瓜、无法收获的物品），会自动处理
		plant(Entities.Cactus)              # 种植仙人掌

		move(North)                         # 向北移动，准备处理下一个地块
	move(East)                             # 完成一列后向东移动，进入下一列

# 主要循环：持续收获和重新种植
# 这是一个无限循环，确保农场持续生产仙人掌
while True:
	for i in range(get_world_size()):       # 外层循环：遍历行
		for j in range(get_world_size()):   # 内层循环：遍历列
			# 第一步：收获任何成熟的物品（包括仙人掌和其他植物）
			if can_harvest():               # 检查当前位置是否有可收获的物品
				harvest()                   # 收获当前物品（可能是仙人掌或其他植物）

				# 收获后确保地形正确并重新种植仙人掌
				if get_ground_type() != Grounds.Soil:
					till()                  # 确保地形适合种植
				plant(Entities.Cactus)      # 立即重新种植仙人掌，保持农场统一

			# 第二步：仙人掌排序优化（仅在当前位置是仙人掌时执行）
			# 确保只有在仙人掌上才执行排序操作
			if get_entity_type() == Entities.Cactus:
				current_size = measure()     # 获取当前仙人掌的尺寸（0-9）
				if current_size != None:     # 确保测量成功
					east_size = measure(East) # 获取东边相邻仙人掌的尺寸
					# 检查东边是否也是仙人掌并且需要进行排序
					if east_size != None and current_size > east_size:
						# 排序逻辑：如果当前仙人掌比东边的大，交换位置
						swap(East)          # 与东边的仙人掌交换位置

			move(North)                     # 向北移动，处理下一个地块
		move(East)                         # 完成一列后向东移动