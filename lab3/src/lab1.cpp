//
// Created by 李博文 on 25-5-21.
//
//
// Created by MangguoD on 25-4-23.
//

// Lab1Experiment1.cpp
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <queue>
#include <limits>
#include <random>
#include <algorithm>
#include <cctype>
#include <filesystem>
#include <iomanip>
#include <cmath>
#include <cstdlib>
#include "lab1.h"

// 添加节点
void DirectedGraph::addNode(const std::string &u) {
    out[u]; in[u];
}

// 添加边 u->v，权重自增
void DirectedGraph::addEdge(const std::string &u, const std::string &v) {
    addNode(u);
    addNode(v);
    out[u][v]++;
    in[v][u]++;
}

bool DirectedGraph::hasNode(const std::string &u) const {
    return out.count(u);
}

std::vector<std::string> DirectedGraph::nodes() const {
    std::vector<std::string> vs;
    vs.reserve(out.size());
    for (auto &p : out) vs.push_back(p.first);
    return vs;
}

int DirectedGraph::nodeCount() const {
    return out.size();
}

// 出边映射 v->weight
const std::unordered_map<std::string,int>& DirectedGraph::outgoing(const std::string &u) const {
    static const std::unordered_map<std::string,int> empty;
    auto it = out.find(u);
    return it==out.end() ? empty : it->second;
}

// 入边映射 v->weight
const std::unordered_map<std::string,int>& DirectedGraph::incoming(const std::string &u) const {
    static const std::unordered_map<std::string,int> empty;
    auto it = in.find(u);
    return it==in.end() ? empty : it->second;
}

// 边数（权重和）
int DirectedGraph::edgeCount() const {
    int sum = 0;
    for (auto &p : out)
        for (auto &e : p.second)
            sum += e.second;
    return sum;
}

// 将原始文本预处理：转小写、非字母替换为空格、分词
std::vector<std::string> Lab1::preprocess(const std::string &raw) {
    std::vector<std::string> words;
    std::string t;
    for (char c : raw) {
        if (std::isalpha(c)) t += std::tolower(c);
        else t += ' ';
    }
    std::istringstream iss(t);
    while (iss >> t) words.push_back(t);
    return words;
}

// 从文件读入整个文本
bool Lab1::readFile(const std::string &path, std::string &out) {
    std::ifstream ifs(path);
    if (!ifs) return false;
    std::ostringstream oss;
    oss << ifs.rdbuf();
    out = oss.str();
    return true;
}

// 构建图
DirectedGraph Lab1::buildGraph(const std::string &text) {
    auto ws = preprocess(text);
    DirectedGraph G;
    std::string prev;
    for (auto &w : ws) {
        G.addNode(w);
        if (!prev.empty()) G.addEdge(prev, w);
        prev = w;
    }
    return G;
}

// 功能 1：展示有向图
void Lab1::showDirectedGraph(const DirectedGraph &G) {
    // Determine column widths
    size_t nameWidth = 0;
    for (auto &u : G.nodes()) {
        nameWidth = std::max(nameWidth, u.size());
    }
    // Header border
    std::string border = "+" + std::string(nameWidth + 2, '-') + "+" + std::string(50, '-') + "+";
    std::cout << border << "\n";
    // Title row
    std::string title = " 有向图结构 ";
    size_t totalWidth = nameWidth + 2 + 50 + 2;
    size_t padLeft = (totalWidth - title.size()) / 2;
    std::cout << "|" << std::string(padLeft - 1, ' ') << title
              << std::string(totalWidth - padLeft - title.size() + 1, ' ')
              << "|\n";
    std::cout << border << "\n";
    // Each node
    for (auto &u : G.nodes()) {
        auto &outs = G.outgoing(u);
        // First line for node
        std::ostringstream cell;
        cell << " " << std::setw(nameWidth) << std::left << u << " ";
        if (outs.empty()) {
            std::cout << "|" << cell.str() << "|" << std::string(50, ' ') << "|\n";
        } else {
            bool first = true;
            for (auto &e : outs) {
                std::ostringstream edge;
                if (first) {
                    edge << "-> " << e.first << " (权重=" << e.second << ")";
                    first = false;
                } else {
                    edge << "   " << e.first << " (权重=" << e.second << ")";
                }
                std::string edgeStr = edge.str();
                // pad edgeStr to width 50
                if (edgeStr.size() < 50) edgeStr += std::string(50 - edgeStr.size(), ' ');
                std::cout << "|" << cell.str() << "|" << edgeStr << "|\n";
                // clear cell for subsequent lines
                cell.str("");
                cell.clear();
                cell << " " << std::setw(nameWidth) << std::left << "" << " ";
            }
        }
        std::cout << border << "\n";
    }
}

// 功能 2：查询桥接词
std::string Lab1::queryBridgeWords(const DirectedGraph &G,
                        const std::string &w1, const std::string &w2) {
    std::string a = w1, b = w2;
    // 已在 preprocess 中是小写
    if (!G.hasNode(a) || !G.hasNode(b))
        return "No word1 or word2 in the graph!";
    std::unordered_set<std::string> bridges;
    for (auto &e : G.outgoing(a)) {
        const std::string &mid = e.first;
        if (G.outgoing(mid).count(b))
            bridges.insert(mid);
    }
    if (bridges.empty())
        return "No bridge words from " + a + " to " + b + "!";
    std::ostringstream oss;
    oss << "The bridge words from " << a << " to " << b << " are: ";
    bool first = true;
    for (auto &w : bridges) {
        if (!first) oss << ", ";
        oss << w;
        first = false;
    }
    oss << ".";
    return oss.str();
}

// 功能 3：根据桥接词生成新文本
std::string Lab1::generateNewText(const DirectedGraph &G, const std::string &input) {
    auto words = preprocess(input);
    std::vector<std::string> out;
    std::random_device rd;
    std::mt19937 gen(rd());
    for (size_t i = 0; i < words.size(); ++i) {
        out.push_back(words[i]);
        if (i+1 < words.size()) {
            std::vector<std::string> bridges;
            // 找出 words[i] -> mid -> words[i+1]
            for (auto &e : G.outgoing(words[i])) {
                const std::string &mid = e.first;
                if (G.outgoing(mid).count(words[i+1]))
                    bridges.push_back(mid);
            }
            if (!bridges.empty()) {
                std::uniform_int_distribution<> dis(0, bridges.size()-1);
                out.push_back(bridges[dis(gen)]);
            }
        }
    }
    // 合并输出
    std::ostringstream oss;
    for (size_t i = 0; i < out.size(); ++i) {
        if (i) oss << ' ';
        oss << out[i];
    }
    return oss.str();
}

// 功能 4：最短路径（Dijkstra）
std::string Lab1::calcShortestPath(const DirectedGraph &G,
                        const std::string &src, const std::string &dst) {
    if (!G.hasNode(src) || !G.hasNode(dst))
        return "No such nodes in graph!";
    const int INF = std::numeric_limits<int>::max();
    std::unordered_map<std::string,int> dist;
    std::unordered_map<std::string,std::string> prev;
    for (auto &u : G.nodes()) dist[u] = INF;
    dist[src] = 0;
    // 小顶堆 (dist, node)
    using P = std::pair<int,std::string>;
    auto cmp = [](P &a, P &b){ return a.first > b.first; };
    std::priority_queue<P, std::vector<P>, decltype(cmp)> pq(cmp);
    pq.push({0, src});
    while (!pq.empty()) {
        auto [d,u] = pq.top(); pq.pop();
        if (d > dist[u]) continue;
        if (u == dst) break;
        for (auto &e : G.outgoing(u)) {
            const std::string &v = e.first;
            int w = e.second;
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                prev[v] = u;
                pq.push({dist[v], v});
            }
        }
    }
    if (dist[dst] == INF) return "Unreachable!";
    // 重建路径
    std::vector<std::string> path;
    for (std::string at = dst; !at.empty(); at = prev[at]) {
        path.push_back(at);
        if (at == src) break;
    }
    std::reverse(path.begin(), path.end());
    std::ostringstream oss;
    oss << "Path: ";
    for (size_t i = 0; i < path.size(); ++i) {
        if (i) oss << " -> ";
        oss << path[i];
    }
    oss << "\nLength: " << dist[dst];
    return oss.str();
}

// 功能 5：PageRank
double Lab1::calPageRank(const DirectedGraph &G, const std::string &word) {
    int N = G.nodeCount();
    if (!N) return 0.0;
    const double d = 0.85, eps = 1e-6;
    std::unordered_map<std::string,double> pr, tmp;
    double init = 1.0 / N;
    for (auto &u : G.nodes()) pr[u] = init;
    bool changed = true;
    while (changed) {
        changed = false;
        // 累积入链贡献值（处理无出边节点）
        double sinkSum = 0;
        for (auto &v_pair : pr) {
            const std::string &v = v_pair.first;
            if (G.outgoing(v).empty()) {
                sinkSum += pr[v];
            }
        }
        for (auto &u : G.nodes()) {
            double sum = sinkSum / N;
            for (auto &e : G.incoming(u)) {
                const std::string &v = e.first;
                sum += pr[v] / G.outgoing(v).size();
            }
            tmp[u] = (1-d)/N + d * sum;
        }
        for (auto &u : G.nodes()) {
            if (fabs(tmp[u] - pr[u]) > eps) changed = true;
            pr[u] = tmp[u];
        }
    }
    return pr.count(word) ? pr[word] : 0.0;
}

// 功能 6：随机游走
std::string Lab1::randomWalk(const DirectedGraph &G, int maxSteps) {
    auto ns = G.nodes();
    if (ns.empty()) return "";
    std::random_device rd;
    std::mt19937 gen(rd());
    // 从第一个节点开始
    std::string cur = ns[0];
    std::vector<std::string> seq;
    seq.push_back(cur);
    std::unordered_set<std::string> seen;
    for (int i = 0; i < maxSteps; ++i) {
        auto &outs = G.outgoing(cur);
        if (outs.empty()) break;
        // 按权重随机选边
        int total = 0;
        for (auto &e : outs) total += e.second;
        std::uniform_int_distribution<> dis(0, total-1);
        int r = dis(gen), c = 0;
        std::string next;
        for (auto &e : outs) {
            c += e.second;
            if (r < c) { next = e.first; break; }
        }
        std::string edgeId = cur + "->" + next;
        if (seen.count(edgeId)) break;
        seen.insert(edgeId);
        seq.push_back(next);
        cur = next;
    }
    std::ostringstream oss;
    for (size_t i = 0; i < seq.size(); ++i) {
        if (i) oss << " -> ";
        oss << seq[i];
    }
    return oss.str();
}

// 可选功能 1：将有向图保存为图形文件
static void saveGraphAsImage(const DirectedGraph &G, const std::string &outputDir) {
    // 创建输出目录
    std::filesystem::create_directories(outputDir);
    std::string dotPath = outputDir + "/graph.dot";
    std::ofstream ofs(dotPath);
    ofs << "digraph G {\n";
    for (auto &u : G.nodes()) {
        ofs << "  \"" << u << "\";\n";
    }
    for (auto &u : G.nodes()) {
        for (auto &e : G.outgoing(u)) {
            ofs << "  \"" << u << "\" -> \"" << e.first << "\" [label=\"" << e.second << "\"];\n";
        }
    }
    ofs << "}\n";
    ofs.close();
    // 调用 Graphviz 生成 PNG
    std::string cmd = "dot -Tpng " + dotPath + " -o " + outputDir + "/graph.png";
    system(cmd.c_str());
    std::cout << "Graph image saved to " << outputDir << "/graph.png\n";
}

// 可选功能 2：交互式随机游走并保存到文件
static void interactiveRandomWalk(const DirectedGraph &G, int maxSteps) {
    std::filesystem::create_directories("output");
    std::ofstream ofs("output/random_walk.txt");
    auto ns = G.nodes();
    if (ns.empty()) {
        std::cout << "图为空，无法执行随机游走。\n";
        return;
    }
    std::random_device rd;
    std::mt19937 gen(rd());
    // 随机选择起始节点
    std::uniform_int_distribution<> startDis(0, ns.size() - 1);
    std::string cur = ns[startDis(gen)];
    ofs << cur;
    std::cout << "起始节点: " << cur << "\n";
    for (int i = 0; i < maxSteps; ++i) {
        const auto &outs = G.outgoing(cur);
        if (outs.empty()) {
            std::cout << "节点 " << cur << " 无出边，随机游走结束。\n";
            break;
        }
        int total = 0;
        for (auto &e : outs) total += e.second;
        std::uniform_int_distribution<> dis(0, total - 1);
        int r = dis(gen), cum = 0;
        std::string next;
        for (auto &e : outs) {
            cum += e.second;
            if (r < cum) { next = e.first; break; }
        }
        std::cout << "下一个节点: " << next << "，按 Enter 继续，输入 q 回车退出...";
        std::string input;
        std::getline(std::cin, input);
        if (!input.empty() && (input[0]=='q' || input[0]=='Q')) {
            std::cout << "用户退出随机游走。\n";
            break;
        }
        ofs << " -> " << next;
        cur = next;
    }
    ofs.close();
    std::cout << "随机游走路径已保存为 output/random_walk.txt\n";
}

#ifndef GTEST
int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::cout << "请输入文本文件路径：";
    std::string path;
    std::getline(std::cin, path);
    std::string text;
    if (!Lab1::readFile(path, text)) {
        std::cerr << "读取文件失败！\n";
        return 1;
    }

    auto G = Lab1::buildGraph(text);
    std::cout << "有向图已生成，共 " << G.nodeCount()
              << " 个节点，" << G.edgeCount() << " 条有向边。\n";

    while (true) {
        std::cout << "\n选择功能:\n"
             << "1. 展示有向图\n"
             << "2. 查询桥接词\n"
             << "3. 根据桥接词生成新文本\n"
             << "4. 计算最短路径（输入一或两个单词）\n"
             << "5. 计算 PageRank\n"
             << "6. 随机游走\n"
             << "7. 导出图形文件\n"
             << "0. 退出\n"
             << ">> ";
        std::string cmd;
        std::getline(std::cin, cmd);
        if (cmd=="7") {
            saveGraphAsImage(G, "output");
        }
        else if (cmd=="0") break;
        else if (cmd=="1") Lab1::showDirectedGraph(G);
        else if (cmd=="2") {
            std::cout << "word1 = ";
            std::string w1,w2;
            std::cin >> w1 >> w2;
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            std::cout << Lab1::queryBridgeWords(G,w1,w2) << "\n";
        }
        else if (cmd=="3") {
            std::cout << "请输入一行文本：";
            std::string line;
            std::getline(std::cin, line);
            std::cout << Lab1::generateNewText(G,line) << "\n";
        }
        else if (cmd=="4") {
            // 可选功能：单个或两个单词
            std::cout << "请输入一个单词，或两个单词（以空格分隔）：";
            std::string line;
            std::getline(std::cin, line);
            std::istringstream iss(line);
            std::vector<std::string> parts;
            std::string w;
            while (iss >> w) parts.push_back(w);
            if (parts.empty()) {
                std::cout << "输入不能为空。\n";
            } else if (parts.size() == 1) {
                std::string src = parts[0];
                if (!G.hasNode(src)) {
                    std::cout << "节点 " << src << " 不在图中。\n";
                } else {
                    for (auto &dst : G.nodes()) {
                        if (dst == src) continue;
                        std::cout << Lab1::calcShortestPath(G, src, dst) << "\n";
                    }
                }
            } else {
                std::cout << Lab1::calcShortestPath(G, parts[0], parts[1]) << "\n";
            }
        }
        else if (cmd=="5") {
            std::cout << "单词 = ";
            std::string w;
            std::cin >> w;
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            double pr = Lab1::calPageRank(G,w);
            std::cout << w << " 的 PageRank = " << pr << "\n";
        }
        else if (cmd=="6") {
            interactiveRandomWalk(G, 1000);
        }
        else {
            std::cout << "无效选项\n";
        }
    }

    std::cout << "程序结束。\n";
    return 0;
}
#endif