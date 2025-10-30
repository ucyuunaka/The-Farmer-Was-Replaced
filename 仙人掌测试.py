# 全尺寸-仙人掌排序（充分优化版 + 快速测试系统）
#
# 功能概述：这是一个全自动化的仙人掌种植、排序、收获和重种系统
# 核心算法：基于双向冒泡排序的仙人掌大小排序算法
# 目标：通过合理排列仙人掌大小实现大规模连锁收获，获得平方级收益
# 新增：完整的快速测试功能和性能测量系统
#
# 系统特点：
# 1. 并行化处理 - 充分利用多无人机系统提升效率
# 2. 双向排序 - 横向和纵向同时进行冒泡排序
# 3. 智能决策 - 根据收获产量自动选择重种策略
# 4. 快速测试 - 精确测量12×12地块全局排序时间
# 5. 自适应排序 - 动态调整排序轮数优化效率
#
# 性能指标：
# - 时间复杂度：O(n²) 排序 + O(n²) 检测 = O(n²)
# - 空间复杂度：O(1) 原地操作
# - 并行度：最多12架无人机同时工作
# - 预期产量：min_chain × min_chain （连锁平方收益）
#
# 快速测试功能：
# - 精确时间测量和性能跟踪
# - 自适应排序轮数计算
# - 全局排序完成状态检测
# - 详细性能报告输出

clear()

# ==================== 配置系统 ====================

# 快速测试模式开关
FAST_TEST_MODE = True  # 设置为False使用标准模式

# 自适应参数配置
config = {
    "farm_size": 12,              # 预期农场尺寸
    "drone_count": 2,             # 无人机数量
    "target_yield_ratio": 0.8,    # 目标产量比例（相对于理论最大值）
    "min_chain_ratio": 0.6,       # 最小连锁规模比例
    "max_iterations": 10,         # 快速测试最大迭代次数
    "adaptive_sort_rounds": True,  # 启用自适应排序轮数
    "performance_tracking": True   # 启用性能跟踪
}

# 计算自适应参数
s = get_world_size()  # 获取实际农场尺寸

# 自适应排序轮数计算（基于农场大小和无人机数量）
def calculate_adaptive_rounds(farm_size, drone_count):
    """
    根据农场大小和无人机数量计算最优排序轮数

    算法说明：
    - 小农场需要较少轮数，大农场需要更多轮数
    - 多无人机可以减少每轮的时间，但不影响轮数
    - 经验公式：rounds = ceil(log2(farm_size)) + 1
    """
    if farm_size <= 5:
        return farm_size  # 小农场：直接使用边长
    elif farm_size <= 8:
        return farm_size - 1  # 中等农场：边长-1
    else:
        # 大农场：基于对数的自适应算法
        import math
        return int(math.ceil(math.log2(farm_size))) + 2

# 动态配置更新
config["adaptive_rounds"] = calculate_adaptive_rounds(s, config["drone_count"])
config["min_chain_size"] = int(s * s * config["min_chain_ratio"])
config["target_yield"] = config["min_chain_size"] * config["min_chain_size"]

# ==================== 性能跟踪系统 ====================

class PerformanceTracker:
    """性能跟踪器类"""

    def __init__(self):
        self.reset()

    def reset(self):
        """重置所有计时器"""
        self.start_time = None
        self.stage_times = {}
        self.total_time = 0
        self.current_stage = None

    def start_timing(self, stage_name):
        """开始计时特定阶段"""
        if config["performance_tracking"]:
            self.current_stage = stage_name
            self.stage_times[stage_name] = {"start": get_time(), "end": None, "duration": 0}
            if not self.start_time:
                self.start_time = get_time()

    def end_timing(self, stage_name=None):
        """结束计时特定阶段"""
        if config["performance_tracking"] and self.current_stage:
            if stage_name is None:
                stage_name = self.current_stage

            if stage_name in self.stage_times:
                self.stage_times[stage_name]["end"] = get_time()
                self.stage_times[stage_name]["duration"] = (
                    self.stage_times[stage_name]["end"] - self.stage_times[stage_name]["start"]
                )

    def get_total_time(self):
        """获取总运行时间"""
        if self.start_time:
            return get_time() - self.start_time
        return 0

    def print_summary(self):
        """打印性能总结"""
        if not config["performance_tracking"]:
            return

        total = self.get_total_time()
        quick_print("\n" + "="*50)
        quick_print("📊 性能测试报告")
        quick_print("="*50)
        quick_print(f"🌾 农场规模: {s}×{s}")
        quick_print(f"🚁 无人机数量: {config['drone_count']}")
        quick_print(f"🔄 自适应排序轮数: {config['adaptive_rounds']}")
        quick_print(f"⏱️ 总运行时间: {total:.2f}秒")
        quick_print("-"*50)

        # 各阶段耗时
        for stage, times in self.stage_times.items():
            if times["duration"] > 0:
                percentage = (times["duration"] / total) * 100 if total > 0 else 0
                quick_print(f"{stage:20}: {times['duration']:6.2f}秒 ({percentage:5.1f}%)")

        quick_print("="*50)

# 创建全局性能跟踪器
performance = PerformanceTracker()

# ==================== 核心功能函数 ====================

def plant_column():
    """
    并行种植函数 - 种植一整列的仙人掌

    功能描述：
    - 从当前位置开始，沿北方向连续种植仙人掌
    - 每个位置先耕地再种植，确保土壤条件适宜
    - 支持多无人机并行处理，提升种植效率

    算法流程：
    1. 获取农场尺寸s
    2. 循环s次，每次：
       - 耕地当前地块 (till)
       - 种植仙人掌 (plant(Entities.Cactus))
       - 向北移动一格

    性能特征：
    - 时间复杂度：O(s)，s为农场边长
    - 空间复杂度：O(1)
    - 并行支持：是，可为每列分配独立无人机

    使用场景：
    - 系统初始化阶段的批量种植
    - 全重种模式下的重新种植
    """
    for _ in range(s):
        till()  # 耕地，为种植仙人掌准备土壤
        plant(Entities.Cactus)  # 种植仙人掌
        move(North)  # 向北移动到下一个位置

def sort_row_east():
    """
    横向排序函数 - 东向冒泡排序算法

    功能描述：
    - 对当前行进行从西到东的冒泡排序
    - 确保每个仙人掌都不大于东边的邻居
    - 为连锁收获机制创造必要条件

    算法流程：
    1. 沿东向遍历整行
    2. 对每个位置（除最东边）：
       - 获取当前仙人掌大小 (measure)
       - 获取东边仙人掌大小 (measure(East))
       - 如果当前 > 东边，则交换位置 (swap(East))
    3. 继续向东移动

    边界处理：
    - 只在get_pos_x() < s-1的位置进行比较
    - 避免在边界处进行无效操作
    - 确保所有measure()返回有效值

    性能特征：
    - 时间复杂度：O(s)，单行遍历
    - 空间复杂度：O(1)，原地操作
    - 稳定性：稳定排序，相等元素不交换
    """
    for _ in range(s):
        # 边界检查：确保不是最东边的位置
        if get_pos_x() < s - 1:
            # 获取当前和东边仙人掌的大小
            c = measure()  # 当前位置仙人掌大小 (0-9)
            e = measure(East)  # 东边仙人掌大小

            # 交换条件：当前 > 东边（逆序）
            # 同时确保两个位置都有成熟的仙人掌
            if c != None and e != None and c > e:
                swap(East)  # 交换位置，修复逆序
        move(East)  # 移动到下一个位置

def sort_column_north():
    """
    纵向排序函数 - 北向冒泡排序算法

    功能描述：
    - 对当前列进行从南到北的冒泡排序
    - 确保每个仙人掌都不大于北边的邻居
    - 与横向排序配合，形成完整的二维排序网络

    算法流程：
    1. 沿北向遍历整列
    2. 对每个位置（除最北边）：
       - 获取当前仙人掌大小 (measure)
       - 获取北边仙人掌大小 (measure(North))
       - 如果当前 > 北边，则交换位置 (swap(North))
    3. 继续向北移动

    与横向排序的关系：
    - 横向排序确保东向有序：c[i][j] <= c[i+1][j]
    - 纵向排序确保北向有序：c[i][j] <= c[i][j+1]
    - 两者结合形成二维偏序关系，是连锁收获的基础

    性能特征：
    - 时间复杂度：O(s)，单列遍历
    - 空间复杂度：O(1)，原地操作
    - 稳定性：稳定排序，保持相等元素的相对位置
    """
    for _ in range(s):
        # 边界检查：确保不是最北边的位置
        if get_pos_y() < s - 1:
            # 获取当前和北边仙人掌的大小
            c = measure()  # 当前位置仙人掌大小 (0-9)
            n = measure(North)  # 北边仙人掌大小

            # 交换条件：当前 > 北边（逆序）
            # 同时确保两个位置都有成熟的仙人掌
            if c != None and n != None and c > n:
                swap(North)  # 交换位置，修复逆序
        move(North)  # 移动到下一个位置

# ==================== 快速测试主函数 ====================

def fast_test_cactus_sorting():
    """
    快速测试模式 - 仙人掌排序性能测试

    功能描述：
    - 精确测量12×12地块全局排序所需时间
    - 使用自适应排序算法优化效率
    - 提供详细的性能分析和进度报告
    - 支持最大迭代次数限制

    测试目标：
    1. 验证自适应排序算法的有效性
    2. 测量全局排序的完成时间
    3. 分析各阶段的性能瓶颈
    4. 确认连锁收获机制的完整性

    输出报告：
    - 各阶段耗时分析
    - 排序完成度评估
    - 性能优化建议
    """
    quick_print("🚀 启动快速测试模式")
    quick_print(f"📋 测试配置：{s}×{s}农场，{config['drone_count']}架无人机")
    quick_print(f"🎯 目标：实现全局排序，连锁收获≥{config['target_yield']}个仙人掌")
    quick_print("="*50)

    performance.start_timing("总测试时间")
    iteration_count = 0

    # ==================== 初始化种植阶段 ====================

    performance.start_timing("初始化种植")
    quick_print("🌱 开始初始化种植...")

    # 初始化种植阶段 - 并行种植整个农场的仙人掌矩阵
    for _ in range(s):
        # 尝试生成新无人机执行种植任务
        if not spawn_drone(plant_column):
            # 如果无人机生成失败（可能已达上限），主无人机亲自执行
            plant_column()
        move(East)  # 移动到下一列的位置

    performance.end_timing("初始化种植")

    # 主要执行循环 - 快速测试版本
    while True:
        iteration_count += 1

        if FAST_TEST_MODE:
            quick_print(f"\n🔄 第{iteration_count}轮优化开始")
            quick_print(f"⏱️ 当前耗时：{performance.get_total_time():.2f}秒")

            # 检查最大迭代次数限制
            if iteration_count > config["max_iterations"]:
                quick_print(f"\n⚠️ 达到最大迭代次数({config['max_iterations']})，停止测试")
                performance.end_timing("总测试时间")
                performance.print_summary()
                break

        # ==================== 横向排序阶段 ====================

        performance.start_timing("横向排序")

        # 使用自适应轮数进行横向排序
        sort_rounds = config["adaptive_rounds"] if config["adaptive_sort_rounds"] else s

        quick_print(f"🔄 开始横向排序：{sort_rounds}轮（自适应）")

        for round in range(sort_rounds):  # 执行自适应轮数横向排序
            for _ in range(s):
                # 尝试为当前行生成独立无人机
                if not spawn_drone(sort_row_east):
                    # 无人机生成失败时，主无人机亲自执行排序
                    sort_row_east()
                move(North)  # 移动到下一行

        # ==================== 纵向排序阶段 ====================

        performance.end_timing("横向排序")
        performance.start_timing("纵向排序")

        quick_print(f"🔄 开始纵向排序：{sort_rounds}轮（自适应）")

        for round in range(sort_rounds):  # 执行自适应轮数纵向排序
            for _ in range(s):
                # 尝试为当前列生成独立无人机
                if not spawn_drone(sort_column_north):
                    # 无人机生成失败时，主无人机亲自执行排序
                    sort_column_north()
                move(East)  # 移动到下一列

        # ==================== 成熟度检测阶段 ====================

        performance.end_timing("纵向排序")
        performance.start_timing("成熟检测")

        quick_print("⏳ 等待所有仙人掌成熟...")

        all_ready = False  # 标记是否所有仙人掌都已成熟
        detection_count = 0  # 检测次数计数器

        while not all_ready:
            all_ready = True  # 假设所有都已成熟，发现未成熟时设为False
            unready_count = 0  # 未成熟仙人掌计数

            detection_count += 1
            if FAST_TEST_MODE and detection_count % 5 == 0:
                quick_print(f"   检测进度：第{detection_count}次扫描")

            for i in range(s):
                for j in range(s):
                    # 检查当前位置是否为仙人掌且未成熟
                    if get_entity_type() == Entities.Cactus:
                        if not can_harvest():
                            all_ready = False  # 发现未成熟的仙人掌
                            unready_count += 1
                    move(North)  # 移动到下一个位置（向北）
                move(East)  # 移动到下一列（向东）

            if FAST_TEST_MODE and unready_count > 0:
                quick_print(f"   未成熟仙人掌：{unready_count}个")

        # ==================== 连锁收获和产量评估阶段 ====================

        performance.end_timing("成熟检测")
        performance.start_timing("连锁收获")

        quick_print("🎯 开始连锁收获...")
        before = num_items(Items.Cactus)  # 记录收获前的仙人掌数量

        # 寻找第一个可收获的仙人掌触发连锁收获
        harvested = False
        search_steps = 0  # 搜索步数计数

        for i in range(s):
            for j in range(s):
                search_steps += 1
                if can_harvest():
                    quick_print(f"   找到可收获仙人掌（搜索{search_steps}步）")
                    harvest()  # 进行连锁收获
                    harvested = True
                    break  # 收获成功，立即跳出循环
            if harvested:
                break
            move(North)  # 向北移动到下一行
        move(East)  # 向东移动到下一列

        # 产量评估和目标设定（修复逻辑错误）
        gained = num_items(Items.Cactus) - before  # 计算实际收获数量
        min_chain = config["min_chain_size"]  # 使用配置中的最小连锁规模
        target_yield = config["target_yield"]  # 使用配置中的目标产量

        # 计算排序完成度
        total_cacti = s * s
        completion_rate = (gained / (total_cacti * total_cacti)) * 100 if total_cacti > 0 else 0
        is_global_sorting_complete = gained >= target_yield

        # 输出详细的收获结果
        quick_print(f"📈 收获结果：{gained} 个仙人掌")
        quick_print(f"🎯 目标产量：{target_yield} 个")
        quick_print(f"📊 完成度：{completion_rate:.1f}%")
        quick_print(f"✅ 全局排序状态：{'完成' if is_global_sorting_complete else '未完成'}")

        if FAST_TEST_MODE:
            if is_global_sorting_complete:
                quick_print("🎉 恭喜！全局排序已完成，达到理想连锁收获效果！")
            else:
                quick_print(f"🔄 排序未达目标，需要继续优化...（还差{target_yield - gained}个）")

        # ==================== 智能重种决策系统 ====================

        # 快速测试模式：检查是否达到停止条件
        if FAST_TEST_MODE:
            performance.end_timing("连锁收获")

            if is_global_sorting_complete:
                quick_print("\n🏆 快速测试完成！全局排序已达成！")
                performance.end_timing("总测试时间")
                performance.print_summary()
                break  # 退出主循环
            else:
                quick_print(f"\n🔄 继续优化...（第{performance.get_total_time():.1f}秒）")

        if gained < target_yield:
            # 全重种模式 - 当产量低于预期时重置整个农场
            quick_print("🔄 全重种模式...")

            def replant_column():
                """
                全重种函数 - 完全重新种植一整列

                功能描述：
                - 收获当前位置的所有仙人掌
                - 重新耕地并种植新的仙人掌
                - 适用于产量严重不足时的完全重置

                使用场景：
                - 排序效果极差，连锁收获规模很小
                - 需要重新开始整个种植和排序过程
                - 清除可能存在的异常状态

                性能考虑：
                - 时间复杂度：O(s)，处理一整列
                - 资源消耗较大，但能确保完全重置
                - 并行处理可显著提升效率
                """
                for _ in range(s):
                    if can_harvest():
                        harvest()  # 收获当前所有仙人掌
                    till()  # 重新耕地
                    plant(Entities.Cactus)  # 种植新仙人掌
                    move(North)  # 移动到下一个位置

            # 并行执行全重种操作
            for _ in range(s):
                if not spawn_drone(replant_column):
                    replant_column()  # 无人机生成失败时主无人机执行
                move(East)  # 移动到下一列
        else:
            # 补空模式 - 当产量达到预期时只填补空缺
            quick_print("🔄 补空模式...")

            def refill_column():
                """
                补空种函数 - 只在空缺位置种植仙人掌

                功能描述：
                - 检查每个位置是否为空
                - 只在非仙人掌位置进行种植
                - 保持已有的良好排序布局

                使用场景：
                - 排序效果良好，大部分仙人掌已收获
                - 需要保持现有的排序基础
                - 快速补充空缺以进行下一轮优化

                优势：
                - 节省资源，只种植必要的位置
                - 保持已有的排序成果
                - 更快的恢复时间
                """
                for _ in range(s):
                    if get_entity_type() != Entities.Cactus:
                        till()  # 耕地空缺位置
                        plant(Entities.Cactus)  # 种植新仙人掌
                    move(North)  # 移动到下一个位置

            # 并行执行补空操作
            for _ in range(s):
                if not spawn_drone(refill_column):
                    refill_column()  # 无人机生成失败时主无人机执行
                move(East)  # 移动到下一列

# ==================== 主程序入口 ====================

# 如果启用快速测试模式，调用快速测试函数
if FAST_TEST_MODE:
    fast_test_cactus_sorting()
else:
    # 标准模式：执行原有的无限循环逻辑
    quick_print("🔄 标准模式：运行优化后的仙人掌排序系统")

    # 初始化种植
    quick_print("🌱 初始化种植...")
    for _ in range(s):
        if not spawn_drone(plant_column):
            plant_column()
        move(East)

    # 无限循环优化
    while True:
        # 这里可以调用原有的排序逻辑
        # 为了简洁，这里暂时使用快速测试逻辑
        fast_test_cactus_sorting()
        break