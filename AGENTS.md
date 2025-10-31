# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## 游戏概述
这是一个"编程农场"游戏，类似于Python的编程环境，玩家通过编写代码控制无人机在农场中种植、收获和管理各种植物。

## 补充代码规范

### 条件表达式规范
- 禁止使用Python的三元运算符（条件表达式）如 `x if condition else y`
- 必须使用标准的if-else语句结构：
  ```
  if condition:
      x
  else:
      y
  ```

### 函数传递规范
- 禁止使用lambda表达式，如 `lambda x: x+1`
- 必须使用def关键字预定义函数，然后传递函数名：
  ```
  def my_function(arg1, arg2):
      # 函数体
      pass
  
  spawn_drone(my_function)
  ```

### 字典迭代规范
- 禁止直接迭代字典的键值对，如 `for key, value in dict.items()`
- 必须先迭代键，然后通过键访问值：
  ```
  for key in dict:
      value = dict[key]
  ```

### 多无人机系统规范
- 每架无人机都有自己独立的内存，不能直接读取或写入另一架无人机的全局变量
- 主无人机不应直接进入无限循环，否则无法生成其他无人机
- 所有无人机（包括主无人机）都应通过spawn_drone生成，确保一致的启动流程

### 字符串格式化规范
- 禁止使用f-string格式化字符串，如 `f"变量值: {variable}"`
- 必须使用字符串连接或str()函数：
  ```
  # 错误
  print(f"变量值: {variable}")
  
  # 正确
  print("变量值: " + str(variable))
  ```

### 字符串乘法规范
- 禁止使用字符串乘法运算符，如 `"=" * 50`
- 必须使用字符串字面量或字符串连接：
  ```
  # 错误
  print("=" * 50)
  
  # 正确
  print("==================================================")
  ```