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

using namespace std;

// 有向图类
class DirectedGraph {
public:
    // 添加节点
    void addNode(const string &u) {
        out[u]; in[u];
    }
    // 添加边 u->v，权重自增
    void addEdge(const string &u, const string &v) {
        addNode(u); addNode(v);
        out[u][v]++;
        in[v][u]++;
    }
    bool hasNode(const string &u) const {
        return out.count(u);
    }
    vector<string> nodes() const {
        vector<string> vs;
        vs.reserve(out.size());
        for (auto &p : out) vs.push_back(p.first);
        return vs;
    }
    int nodeCount() const {
        return out.size();
    }
    // 出边映射 v->weight
    const unordered_map<string,int>& outgoing(const string &u) const {
        static const unordered_map<string,int> empty;
        auto it = out.find(u);
        return it==out.end() ? empty : it->second;
    }
    // 入边映射 v->weight
    const unordered_map<string,int>& incoming(const string &u) const {
        static const unordered_map<string,int> empty;
        auto it = in.find(u);
        return it==in.end() ? empty : it->second;
    }
    // 边数（权重和）
    int edgeCount() const {
        int sum = 0;
        for (auto &p : out)
            for (auto &e : p.second)
                sum += e.second;
        return sum;
    }

private:
    unordered_map<string, unordered_map<string,int>> out, in;
};

// 将原始文本预处理：转小写、非字母替换为空格、分词
vector<string> preprocess(const string &raw) {
    vector<string> words;
    string t;
    for (char c : raw) {
        if (isalpha(c)) t += tolower(c);
        else t += ' ';
    }
    istringstream iss(t);
    while (iss >> t) words.push_back(t);
    return words;
}

// 从文件读入整个文本
bool readFile(const string &path, string &out) {
    ifstream ifs(path);
    if (!ifs) return false;
    ostringstream oss;
    oss << ifs.rdbuf();
    out = oss.str();
    return true;
}

// 构建图
DirectedGraph buildGraph(const string &text) {
    auto ws = preprocess(text);
    DirectedGraph G;
    string prev;
    for (auto &w : ws) {
        G.addNode(w);
        if (!prev.empty()) G.addEdge(prev, w);
        prev = w;
    }
    return G;
}

// 功能 1：展示有向图
void showDirectedGraph(const DirectedGraph &G) {
    // Determine column widths
    size_t nameWidth = 0;
    for (auto &u : G.nodes()) {
        nameWidth = max(nameWidth, u.size());
    }
    // Header border
    string border = "+" + string(nameWidth + 2, '-') + "+" + string(50, '-') + "+";
    cout << border << "\n";
    // Title row
    string title = " 有向图结构 ";
    size_t totalWidth = nameWidth + 2 + 50 + 2;
    size_t padLeft = (totalWidth - title.size()) / 2;
    cout << "|" << string(padLeft - 1, ' ') << title
         << string(totalWidth - padLeft - title.size() + 1, ' ')
         << "|\n";
    cout << border << "\n";
    // Each node
    for (auto &u : G.nodes()) {
        auto &outs = G.outgoing(u);
        // First line for node
        ostringstream cell;
        cell << " " << setw(nameWidth) << left << u << " ";
        if (outs.empty()) {
            cout << "|" << cell.str() << "|" << string(50, ' ') << "|\n";
        } else {
            bool first = true;
            for (auto &e : outs) {
                ostringstream edge;
                if (first) {
                    edge << "-> " << e.first << " (权重=" << e.second << ")";
                    first = false;
                } else {
                    edge << "   " << e.first << " (权重=" << e.second << ")";
                }
                string edgeStr = edge.str();
                // pad edgeStr to width 50
                if (edgeStr.size() < 50) edgeStr += string(50 - edgeStr.size(), ' ');
                cout << "|" << cell.str() << "|" << edgeStr << "|\n";
                // clear cell for subsequent lines
                cell.str("");
                cell.clear();
                cell << " " << setw(nameWidth) << left << "" << " ";
            }
        }
        cout << border << "\n";
    }
}

// 功能 2：查询桥接词
string queryBridgeWords(const DirectedGraph &G,
                        const string &w1, const string &w2) {
    string a = w1, b = w2;
    // 已在 preprocess 中是小写
    if (!G.hasNode(a) || !G.hasNode(b))
        return "No word1 or word2 in the graph!";
    unordered_set<string> bridges;
    for (auto &e : G.outgoing(a)) {
        const string &mid = e.first;
        if (G.outgoing(mid).count(b))
            bridges.insert(mid);
    }
    if (bridges.empty())
        return "No bridge words from " + a + " to " + b + "!";
    ostringstream oss;
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
string generateNewText(const DirectedGraph &G, const string &input) {
    auto words = preprocess(input);
    vector<string> out;
    random_device rd;
    mt19937 gen(rd());
    for (size_t i = 0; i < words.size(); ++i) {
        out.push_back(words[i]);
        if (i+1 < words.size()) {
            vector<string> bridges;
            // 找出 words[i] -> mid -> words[i+1]
            for (auto &e : G.outgoing(words[i])) {
                const string &mid = e.first;
                if (G.outgoing(mid).count(words[i+1]))
                    bridges.push_back(mid);
            }
            if (!bridges.empty()) {
                uniform_int_distribution<> dis(0, bridges.size()-1);
                out.push_back(bridges[dis(gen)]);
            }
        }
    }
    // 合并输出
    ostringstream oss;
    for (size_t i = 0; i < out.size(); ++i) {
        if (i) oss << ' ';
        oss << out[i];
    }
    return oss.str();
}

// 功能 4：最短路径（Dijkstra）
string calcShortestPath(const DirectedGraph &G,
                        const string &src, const string &dst) {
    if (!G.hasNode(src) || !G.hasNode(dst))
        return "No such nodes in graph!";
    const int INF = numeric_limits<int>::max();
    unordered_map<string,int> dist;
    unordered_map<string,string> prev;
    for (auto &u : G.nodes()) dist[u] = INF;
    dist[src] = 0;
    // 小顶堆 (dist, node)
    using P = pair<int,string>;
    auto cmp = [](P &a, P &b){ return a.first > b.first; };
    priority_queue<P, vector<P>, decltype(cmp)> pq(cmp);
    pq.push({0, src});
    while (!pq.empty()) {
        auto [d,u] = pq.top(); pq.pop();
        if (d > dist[u]) continue;
        if (u == dst) break;
        for (auto &e : G.outgoing(u)) {
            const string &v = e.first;
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
    vector<string> path;
    for (string at = dst; !at.empty(); at = prev[at]) {
        path.push_back(at);
        if (at == src) break;
    }
    reverse(path.begin(), path.end());
    ostringstream oss;
    oss << "Path: ";
    for (size_t i = 0; i < path.size(); ++i) {
        if (i) oss << " -> ";
        oss << path[i];
    }
    oss << "\nLength: " << dist[dst];
    return oss.str();
}

// 功能 5：PageRank
double calPageRank(const DirectedGraph &G, const string &word) {
    int N = G.nodeCount();
    if (!N) return 0.0;
    const double d = 0.85, eps = 1e-6;
    unordered_map<string,double> pr, tmp;
    double init = 1.0 / N;
    for (auto &u : G.nodes()) pr[u] = init;
    bool changed = true;
    while (changed) {
        changed = false;
        for (auto &u : G.nodes()) {
            double sum = 0;
            for (auto &e : G.incoming(u)) {
                const string &v = e.first;
                sum += pr[v] / G.outgoing(v).size();
            }
            tmp[u] = (1-d)/N + d*sum;
        }
        for (auto &u : G.nodes()) {
            if (fabs(tmp[u] - pr[u]) > eps) changed = true;
            pr[u] = tmp[u];
        }
    }
    return pr.count(word) ? pr[word] : 0.0;
}

// 功能 6：随机游走
string randomWalk(const DirectedGraph &G, int maxSteps=1000) {
    auto ns = G.nodes();
    if (ns.empty()) return "";
    random_device rd;
    mt19937 gen(rd());
    // 从第一个节点开始
    string cur = ns[0];
    vector<string> seq;
    seq.push_back(cur);
    unordered_set<string> seen;
    for (int i = 0; i < maxSteps; ++i) {
        auto &outs = G.outgoing(cur);
        if (outs.empty()) break;
        // 按权重随机选边
        int total = 0;
        for (auto &e : outs) total += e.second;
        uniform_int_distribution<> dis(0, total-1);
        int r = dis(gen), c = 0;
        string next;
        for (auto &e : outs) {
            c += e.second;
            if (r < c) { next = e.first; break; }
        }
        string edgeId = cur + "->" + next;
        if (seen.count(edgeId)) break;
        seen.insert(edgeId);
        seq.push_back(next);
        cur = next;
    }
    ostringstream oss;
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

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cout << "请输入文本文件路径：";
    string path;
    getline(cin, path);
    string text;
    if (!readFile(path, text)) {
        cerr << "读取文件失败！\n";
        return 1;
    }

    auto G = buildGraph(text);
    cout << "有向图已生成，共 " << G.nodeCount()
         << " 个节点，" << G.edgeCount() << " 条有向边。\n";

    while (true) {
        cout << "\n选择功能:\n"
             << "1. 展示有向图\n"
             << "2. 查询桥接词\n"
             << "3. 根据桥接词生成新文本\n"
             << "4. 计算最短路径（输入一或二个单词）\n"
             << "5. 计算 PageRank\n"
             << "6. 随机游走\n"
             << "7. 导出图形文件\n"
             << "0. 退出\n"
             << ">> ";
        string cmd;
        getline(cin, cmd);
        if (cmd=="7") {
            saveGraphAsImage(G, "output");
        }
        else if (cmd=="0") break;
        else if (cmd=="1") showDirectedGraph(G);
        else if (cmd=="2") {
            cout << "word1 = ";
            string w1,w2;
            cin >> w1 >> w2;
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            cout << queryBridgeWords(G,w1,w2) << "\n";
        }
        else if (cmd=="3") {
            cout << "请输入一行文本：";
            string line;
            getline(cin, line);
            cout << generateNewText(G,line) << "\n";
        }
        else if (cmd=="4") {
            // 可选功能：单个或两个单词
            cout << "请输入一个单词，或两个单词（以空格分隔）：";
            string line;
            getline(cin, line);
            istringstream iss(line);
            vector<string> parts;
            string w;
            while (iss >> w) parts.push_back(w);
            if (parts.empty()) {
                cout << "输入不能为空。\n";
            } else if (parts.size() == 1) {
                string src = parts[0];
                if (!G.hasNode(src)) {
                    cout << "节点 " << src << " 不在图中。\n";
                } else {
                    for (auto &dst : G.nodes()) {
                        if (dst == src) continue;
                        cout << calcShortestPath(G, src, dst) << "\n";
                    }
                }
            } else {
                cout << calcShortestPath(G, parts[0], parts[1]) << "\n";
            }
        }
        else if (cmd=="5") {
            cout << "单词 = ";
            string w;
            cin >> w;
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            double pr = calPageRank(G,w);
            cout << w << " 的 PageRank = " << pr << "\n";
        }
        else if (cmd=="6") {
            cout << "随机游走结果：\n"
                 << randomWalk(G) << "\n";
        }
        else {
            cout << "无效选项\n";
        }
    }

    cout << "程序结束。\n";
    return 0;
}
