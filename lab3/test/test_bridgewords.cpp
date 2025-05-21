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