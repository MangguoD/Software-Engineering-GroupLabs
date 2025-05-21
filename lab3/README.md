使用指南
1.	环境依赖：运行 setup.sh 脚本将在 macOS 环境下通过 Homebrew 安装项目所需工具，包括 Google Test (googletest)、代码风格检查工具 cpplint、静态分析工具 cppcheck、代码覆盖率工具 lcov 等。
2.	编译与测试：运行 run_all.sh 脚本将自动执行以下步骤：
•	使用 cpplint 对源码进行编码规范检查，并输出不符合规范的代码问题。
•	使用 cppcheck 对源码进行静态分析，检查潜在错误和警告（结果将保存于 cppcheck_report.txt 并同时输出至控制台）。
•	使用 clang++ 编译源代码和 Google Test 单元测试（启用覆盖率选项 --coverage），生成可执行测试文件 runTests。
•	运行所有 Google Test 测试用例，显示测试通过/失败结果。
•	使用 lcov 收集测试覆盖率数据，并利用 genhtml 生成覆盖率报告至 coverage/ 目录下的 HTML 文件。
3.	查看结果：
•	代码规范与 Bug 报告：根据 cpplint 和 cppcheck 的输出，查看是否存在代码格式或潜在错误问题。我们已根据这些工具的报告，对 Lab1 原始代码进行了修改，例如移除了全局使用 using namespace std（改用 std:: 前缀）、为I/O操作添加了缺失的 std:: 前缀、修复了 PageRank 函数中可能的除零错误（对无出边节点进行了处理）等。
•	测试结果：run_all.sh 执行时将在控制台显示 Google Test 的测试结果。我们针对 queryBridgeWords 和 calcShortestPath 两个核心函数分别设计了黑盒和白盒测试用例，包括各种等价类和边界情况。例如，测试桥接词功能对无节点图、无桥接词、有单个/多个桥接词等情况的处理；测试最短路径功能对不存在节点、不可达路径、正常最短路径及起点终点相同等情况的输出是否符合预期。所有测试均应通过，表示相应功能行为正确。
•	覆盖率报告：生成的 coverage/index.html 展示了单元测试对源码的覆盖率细节。打开该报告即可查看每个文件的覆盖率百分比和未覆盖的代码行。经过设计的测试用例，应实现对 queryBridgeWords 和 calcShortestPath 等关键函数逻辑分支的完全覆盖（包括循环分支和异常路径）。
4.	运行示例：项目的 main 函数仍保留了交互式菜单，可以输入文本文件路径并选择不同功能进行体验（例如查询桥接词、计算最短路径、执行随机游走等）。需要注意，输出的 graph.png 和 random_walk.txt 将生成在 output/ 目录下。
5.	项目结构：源代码位于 src/ 目录下，包含原始 Lab1 功能的实现（经过代码规范清理和 Bug 修复）；test/ 目录下包含针对核心功能的单元测试代码；setup.sh 和 run_all.sh 脚本实现了一键化的环境配置和构建测试；运行后将生成 coverage/ 报告目录和 output/ 示例输出等。整个项目已经过完整编译测试，确保无编译错误，所有功能运行正常。