//
// Created by 李博文 on 25-5-21.
//
#include <gtest/gtest.h>
#include "../src/lab1.h"

TEST(ShortestPathTest, NodesNotFound) {
    DirectedGraph G;
    G.addNode("a");
    // "b" 不在图中
    EXPECT_EQ(Lab1::calcShortestPath(G, "a", "b"),
              "No such nodes in graph!");
}

TEST(ShortestPathTest, UnreachablePath) {
    DirectedGraph G;
    // 构造图：a->c (权重10), a->b (1), b->c (1), 独立节点 d
    G.addNode("a");
    G.addNode("b");
    G.addNode("c");
    G.addNode("d");
    // 模拟 a->c 权重10 （添加10次边）
    for (int i = 0; i < 10; ++i) {
        G.addEdge("a", "c");
    }
    G.addEdge("a", "b");
    G.addEdge("b", "c");
    std::string result = Lab1::calcShortestPath(G, "a", "d");
    EXPECT_EQ(result, "Unreachable!");
}

TEST(ShortestPathTest, ShortestPathFound) {
    DirectedGraph G;
    // 与上相同的图结构（不包含节点 d）
    G.addNode("a");
    G.addNode("b");
    G.addNode("c");
    for (int i = 0; i < 10; ++i) {
        G.addEdge("a", "c");
    }
    G.addEdge("a", "b");
    G.addEdge("b", "c");
    std::string expected = "Path: a -> b -> c\nLength: 2";
    EXPECT_EQ(Lab1::calcShortestPath(G, "a", "c"), expected);
}

TEST(ShortestPathTest, SameNodePath) {
    DirectedGraph G;
    G.addNode("x");
    EXPECT_EQ(Lab1::calcShortestPath(G, "x", "x"),
              "Path: x\nLength: 0");
}

// 测试用例1
TEST(ShortestPathTest, SameNode) {
    DirectedGraph G;
    G.addNode("a");
    EXPECT_EQ(Lab1::calcShortestPath(G, "a", "a"), "Path: a\nLength: 0");
}

// 测试用例2
TEST(ShortestPathTest, NodeNotExist) {
    DirectedGraph G;
    G.addNode("a");
    EXPECT_EQ(Lab1::calcShortestPath(G, "a", "d"), "No such nodes in graph!");
}

// 测试用例3
TEST(ShortestPathTest, ReachablePath) {
    DirectedGraph G;
    G.addNode("a"); G.addNode("b"); G.addNode("d");
    G.addEdge("a","b"); G.addEdge("b","d");
    EXPECT_EQ(Lab1::calcShortestPath(G, "a", "d"),
              "Path: a -> b -> d\nLength: 2");
}

// 测试用例4
TEST(ShortestPathTest, Unreachable) {
    DirectedGraph G;
    G.addNode("a"); G.addNode("b"); G.addNode("c");
    EXPECT_EQ(Lab1::calcShortestPath(G, "a", "c"), "Unreachable!");
}