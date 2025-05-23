## 使用指南

### 1. 环境依赖（macOS）
运行 `setup.sh` 脚本可通过 Homebrew 自动安装以下依赖项：
- Google Test（googletest）：用于单元测试
- cpplint：用于代码风格检查
- cppcheck：用于静态代码分析
- lcov：用于生成代码覆盖率报告

### 2. 编译与测试
执行 `run_all.sh` 脚本将自动完成以下步骤：

1. 使用 `cpplint` 检查源代码的编码规范
2. 使用 `cppcheck` 进行静态错误分析（结果输出至控制台并保存为 `cppcheck_report.txt`）
3. 使用 `clang++` 编译源代码及 Google Test 测试用例（启用 `--coverage` 覆盖率选项）
4. 运行所有单元测试，显示测试结果
5. 使用 `lcov` 收集覆盖率数据，并用 `genhtml` 生成 HTML 格式的报告至 `coverage/` 目录

### 3. 查看分析结果

- ✅ 代码规范 & 潜在 Bug：
  查看 `cpplint` 和 `cppcheck` 输出，定位不符合规范的代码和潜在缺陷。我们已做如下修复示例：
  - 移除 `using namespace std`，统一使用 `std::` 前缀
  - 补全 `I/O` 操作中的命名空间前缀
  - 修复 `PageRank` 中对无出边节点可能导致除零的问题

- 🧪 单元测试结果：
  控制台将输出所有 Google Test 测试结果。我们围绕 `queryBridgeWords` 和 `calcShortestPath` 函数，设计了等价类和边界测试用例，涵盖：
  - 空图 / 不存在节点 / 多桥接词 / 不可达路径等情况

- 📊 覆盖率报告：
  打开 `coverage/index.html` 可查看每个函数和语句的测试覆盖率（包含循环、分支、异常路径等）

### 4. 运行示例
可通过程序 `main()` 交互式体验各项功能，例如：
- 查询桥接词
- 生成新文本
- 计算最短路径
- PageRank 分析
- 随机游走图路径

输出文件（如 `graph.png`, `random_walk.txt`）将自动生成于 `output/` 目录。

### 5. 项目结构说明

```
Lab3Project/
├── src/                # Lab1 源代码
├── test/               # 单元测试代码（基于 Google Test）
├── setup.sh            # 安装依赖脚本（macOS）
├── run_all.sh          # 一键运行测试与分析脚本
├── coverage/           # 覆盖率报告输出目录
├── output/             # 示例输出结果目录
└── README.md           # 项目说明文档
```

本项目已在 CLion 中完整测试，确保无编译错误，功能可交互调用，覆盖率报告正确生成。