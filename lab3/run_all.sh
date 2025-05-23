#!/bin/bash
# 执行静态检查、单元测试和覆盖率统计

BREW_PREFIX=$(brew --prefix)

echo "Running cpplint..."
cpplint --recursive src test

echo "Running cppcheck..."
cppcheck --enable=all --inconclusive --std=c++17 src test 2> cppcheck_report.txt
cat cppcheck_report.txt

echo "Compiling tests and generating coverage..."
clang++ -std=c++17 -O0 --coverage -Wall -Isrc -I${BREW_PREFIX}/include -c src/lab1.cpp -o lab1.o -DGTEST
clang++ -std=c++17 -O0 --coverage -Wall -Isrc -I${BREW_PREFIX}/include -c test/test_bridgewords.cpp -o test_bridgewords.o
clang++ -std=c++17 -O0 --coverage -Wall -Isrc -I${BREW_PREFIX}/include -c test/test_shortestpath.cpp -o test_shortestpath.o
clang++ --coverage lab1.o test_bridgewords.o test_shortestpath.o -L${BREW_PREFIX}/lib -lgtest -lgtest_main -pthread -o runTests

echo "Running tests..."
./runTests

echo "Collecting coverage data..."
lcov --directory . --capture -o coverage.info --ignore-errors inconsistent,unsupported
lcov --remove coverage.info '*/test/*' '/usr/*' --output-file coverage.info
genhtml coverage.info -o coverage

echo "Done. Coverage report generated at coverage/index.html"