//
// Created by 李博文 on 25-5-21.
//

#include "../lab1.h"
#include <gtest/gtest.h>

TEST(ShortestPathTest, Reachable) {
    DirectedGraph G = buildGraph("a b c d");
    std::string res = calcShortestPath(G, "a", "d");
    EXPECT_NE(res.find("Length: 3"), std::string::npos);
}

TEST(ShortestPathTest, Unreachable) {
    DirectedGraph G = buildGraph("x y z   a b");
    std::string res = calcShortestPath(G, "x", "b");
    EXPECT_EQ(res, "Unreachable!");
}

TEST(ShortestPathTest, InvalidNode) {
    DirectedGraph G = buildGraph("m n o");
    std::string res = calcShortestPath(G, "m", "z");
    EXPECT_EQ(res, "No such nodes in graph!");
}