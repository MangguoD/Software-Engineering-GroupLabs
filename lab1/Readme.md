# Lab1—基于文本的有向图生成与算法演示

本项目实现了从英文文本生成加权有向图，并在该图上提供多种算法操作。支持命令行交互，并可将图导出为 PNG 图像。

---

## 功能概览

1. **文本预处理**
    - 将文本统一转为小写
    - 非字母字符当做空格处理
    - 按空格分词

2. **有向图构建**
    - 节点：文本中出现的单词
    - 边  A → B：单词 A 与 B 在原文中相邻出现
    - 边权重：相邻出现的次数

3. **算法操作**
    - 展示有向图（ASCII 表格）
    - 查询桥接词（Bridge Words）
    - 根据桥接词生成新文本
    - 计算最短路径（Dijkstra；支持单词对或单词到全图）
    - 计算 PageRank（阻尼系数 0.85）
    - 随机游走
    - 导出图形文件（Graphviz PNG）

---

## 目录结构

```
Lab1Project/
├─ lab1.h           # 类与函数声明
├─ lab1.cpp         # 主程序与算法实现
├─ Makefile         # 编译 & 运行脚本
├─ sample.txt       # 测试文本示例
└─ output/          # 导出的 .dot 和 .png 文件
```
---

## 快速开始

### 1. 环境准备

- **C++17 编译器**（g++ 7+ 或 clang++）
- **Graphviz**（用于导出 PNG）
  ```
  # macOS (Homebrew)
  brew install graphviz

  # Ubuntu / Debian
  sudo apt update
  sudo apt install graphviz
  ```

### 2. 编译 & 运行

在项目根目录下执行：

# 编译（生成可执行文件 lab1）
```
make
```
# 运行（命令行交互）
```
./lab1
```
或者：
```
make run
```

### 3. 命令行示例

1.	输入文本文件路径
```
请输入文本文件路径：sample.txt
```

2.	选择功能
```
1. 展示有向图
2. 查询桥接词
3. 根据桥接词生成新文本
4. 计算最短路径（输入一或二个单词）
5. 计算 PageRank
6. 随机游走
7. 导出图形文件
0. 退出
```

3.	导出图形文件

```
Graph image saved to output/graph.png
```

导出的 output/graph.dot 和 output/graph.png 即为 Graphviz 生成的图。

⸻

代码说明

- lab1.h  
- DirectedGraph：有向图数据结构  
- Lab1：静态工具函数（读文件、预处理、构建图、查询、算法等）  
- lab1.cpp  
- 包含所有功能的具体实现  
- 菜单驱动的 main() 负责交互  
- 算法实现：Dijkstra、PageRank、随机游走  
- 可选功能：调用 Graphviz 导出图像  

⸻

测试数据

- Easy Test.txt：小规模示例  
- Cursed Be The Treasure.txt：大规模测试  

可自行替换为其他文本文件，验证程序正确性与性能。

⸻

清理

make clean

该命令会删除可执行文件及导出的 .dot、.png 文件。

⸻

联系 & 贡献

如有问题或建议，请联系：
•	作者：MangguoD
•	邮箱：MangguoD@example.com

欢迎提出 Issue 或 Pull Request！
