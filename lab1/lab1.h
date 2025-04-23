//
// Created by 李博文 on 25-4-23.
//

#ifndef LAB1_H
#define LAB1_H

#include <string>
#include <vector>
#include <unordered_map>
#include <unordered_set>

// 有向图类声明
class DirectedGraph {
public:
    void addNode(const std::string &u);
    void addEdge(const std::string &u, const std::string &v);
    bool hasNode(const std::string &u) const;
    std::vector<std::string> nodes() const;
    int nodeCount() const;
    const std::unordered_map<std::string,int>& outgoing(const std::string &u) const;
    const std::unordered_map<std::string,int>& incoming(const std::string &u) const;
    int edgeCount() const;
};

// Lab1 功能函数封装
class Lab1 {
public:
    // 读取文件内容
    static bool readFile(const std::string &path, std::string &out);
    // 文本预处理
    static std::vector<std::string> preprocess(const std::string &raw);
    // 构建图
    static DirectedGraph buildGraph(const std::string &text);
    // 展示有向图
    static void showDirectedGraph(const DirectedGraph &G);
    // 查询桥接词
    static std::string queryBridgeWords(const DirectedGraph &G,
                                        const std::string &w1,
                                        const std::string &w2);
    // 生成新文本
    static std::string generateNewText(const DirectedGraph &G,
                                       const std::string &input);
    // 计算最短路径
    static std::string calcShortestPath(const DirectedGraph &G,
                                        const std::string &src,
                                        const std::string &dst);
    // 计算 PageRank
    static double calPageRank(const DirectedGraph &G,
                              const std::string &word);
    // 随机游走
    static std::string randomWalk(const DirectedGraph &G,
                                  int maxSteps = 1000);
};

#endif //LAB1_H
