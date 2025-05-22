//
// Created by 李博文 on 25-5-21.
//
#include <gtest/gtest.h>
#include "../src/lab1.h"

TEST(BridgeWordsTest, EmptyGraph) {
    DirectedGraph G;
    EXPECT_EQ(Lab1::queryBridgeWords(G, "foo", "bar"),
              "No word1 or word2 in the graph!");
}

TEST(BridgeWordsTest, NoBridgeWords) {
    std::string text = "x y z. w.";
    DirectedGraph G = Lab1::buildGraph(text);
    std::string output = Lab1::queryBridgeWords(G, "x", "w");
    EXPECT_EQ(output, "No bridge words from x to w!");
}

TEST(BridgeWordsTest, SingleBridgeWord) {
    std::string text = "x y z.";
    DirectedGraph G = Lab1::buildGraph(text);
    EXPECT_EQ(Lab1::queryBridgeWords(G, "x", "z"),
              "The bridge words from x to z are: y.");
}

TEST(BridgeWordsTest, MultipleBridgeWords) {
    std::string text = "x u z. x v z.";
    DirectedGraph G = Lab1::buildGraph(text);
    std::string output = Lab1::queryBridgeWords(G, "x", "z");
    bool correctOrder = (output == "The bridge words from x to z are: u, v." ||
                         output == "The bridge words from x to z are: v, u.");
    EXPECT_TRUE(correctOrder);
}

TEST(BridgeWordsTest, WordNotFound) {
    std::string text = "hello world";
    DirectedGraph G = Lab1::buildGraph(text);
    EXPECT_EQ(Lab1::queryBridgeWords(G, "hello", "there"),
              "No word1 or word2 in the graph!");
}

// 测试用例1
TEST(BridgeWordsTest, SingleBridgeWordExists) {
    DirectedGraph G = Lab1::buildGraph("x y z");
    EXPECT_EQ(Lab1::queryBridgeWords(G, "x", "z"), "The bridge words from x to z are: y.");
}

// 测试用例2
TEST(BridgeWordsTest, NoBridgeWordsExist) {
    DirectedGraph G = Lab1::buildGraph("x y z w");
    EXPECT_EQ(Lab1::queryBridgeWords(G, "x", "w"), "No bridge words from x to w!");
}

// 测试用例3
TEST(BridgeWordsTest, MultipleBridgeWordsExist) {
    DirectedGraph G = Lab1::buildGraph("x u z x v z");
    std::string result = Lab1::queryBridgeWords(G, "x", "z");
    bool correctOrder = (result == "The bridge words from x to z are: u, v." ||
                         result == "The bridge words from x to z are: v, u.");
    EXPECT_TRUE(correctOrder);
}

// 测试用例4
TEST(BridgeWordsTest, FirstWordNotExists) {
    DirectedGraph G = Lab1::buildGraph("x y z");
    EXPECT_EQ(Lab1::queryBridgeWords(G, "notexist", "z"), "No word1 or word2 in the graph!");
}