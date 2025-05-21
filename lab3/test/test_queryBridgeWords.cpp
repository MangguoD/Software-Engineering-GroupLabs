//
// Created by 李博文 on 25-5-21.
//

#include "../lab1.h"
#include <gtest/gtest.h>

TEST(BridgeWordsTest, NormalCase) {
    DirectedGraph G = buildGraph("this is a test and this is an experiment");
    std::string res = queryBridgeWords(G, "this", "a");
    EXPECT_EQ(res, "The bridge words from this to a are: is.");
}

TEST(BridgeWordsTest, NoBridgeCase) {
    DirectedGraph G = buildGraph("to be or not to be");
    std::string res = queryBridgeWords(G, "be", "or");
    EXPECT_EQ(res, "No bridge words from be to or!");
}

TEST(BridgeWordsTest, InvalidInput) {
    DirectedGraph G = buildGraph("a b c");
    std::string res = queryBridgeWords(G, "a", "d");
    EXPECT_EQ(res, "No word1 or word2 in the graph!");
}