import os
import re
import random
import networkx as nx
import matplotlib.pyplot as plt

# 从文本文件中读取数据并创建有向图
def create_digraph_from_file(file_path):
    G = nx.DiGraph()
    with open(file_path, 'r') as file:
        for line in file:
            line = re.sub(r'[^\w\s]', ' ', line)  # 将标点符号替换为空格
            line = line.replace('\n', ' ')  # 将换行符替换为空格
            words = line.strip().split()  # 根据空格分割单词
            # print(type(words))
            for i in range(len(words) - 1):
                source, target = words[i], words[i + 1]
                if source != target:  # 避免自环
                    if G.has_edge(source, target):
                        G[source][target]['weight'] += 1
                    else:
                        G.add_edge(source, target, weight=1)
    return G

# 可视化有向图
def visualize_digraph(G):
    pos = nx.kamada_kawai_layout(G)
    edge_labels = {(source, target): G[source][target]['weight'] for source, target in G.edges()}
    nx.draw(G, pos, with_labels=True, arrows=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    Aplt.show()

def find_bridge_words(graph, word1, word2):
    if word1 not in graph.nodes or word2 not in graph.nodes:
        return "No word1 or word2 in the graph!"
    
    bridge_words = []
    # neighbors_word1_1 = set(graph.neighbors(word1))
    # neighbors_word1_2 = set(graph.predecessors(word1))
    # neighbors_word1 = neighbors_word1_1.union(neighbors_word1_2)
    # neighbors_word2_1 = set(graph.neighbors(word2))
    # neighbors_word2_2 = set(graph.predecessors(word2))
    # neighbors_word2 = neighbors_word2_1.union(neighbors_word2_2)
    # common_neighbors = neighbors_word1.intersection(neighbors_word2)
    # print(neighbors_word1)
    # print(neighbors_word2)
    # print(common_neighbors)
    neighbors_word1 = set(graph.neighbors(word1))
    neighbors_word2 = set(graph.predecessors(word2))
    common_neighbors = neighbors_word1.intersection(neighbors_word2)
    for bridge_word in common_neighbors:
        if bridge_word != word1 and bridge_word != word2:
            bridge_words.append(bridge_word)
    
    if len(bridge_words) == 0:
        print("No bridge words from {} to {}!".format(word1, word2))
    else:
        bridge_words_str = ", ".join(bridge_words)
        print("The bridge words from {} to {} are: {}.".format(word1, word2, bridge_words_str))
    return bridge_words
    

# 处理新文本并插入桥接词
def process_text_with_bridge_words(graph, text):
    words = re.findall(r'\w+', text)  # 提取文本中的单词
    new_text = []
    
    for i in range(len(words) - 1):
        word1, word2 = words[i], words[i + 1]
        new_text.append(word1)
        bridge_words = find_bridge_words(graph, word1, word2)
        # if type(bridge_words) == str:
        #     bridge_words = []
        # print(bridge_words)
        if bridge_words:
            random_bridge_word = random.choice(bridge_words)
            new_text.append(random_bridge_word)
    new_text.append(words[-1])  # 添加最后一个单词
    return ' '.join(new_text)

# 查找最短路径
def find_shortest_path(graph, word1, word2):
    try:
        shortest_path = nx.shortest_path(graph, source=word1, target=word2, weight='weight')
        return shortest_path
    except nx.NetworkXNoPath:
        return None
    
# 查找单词到图中其他任一单词的最短路径
def find_shortest_paths_to_other_words(graph, word):
    if word not in graph.nodes:
        return "单词 {} 不在图中，请重新输入。".format(word)
    
    shortest_paths = {}
    for target_word in graph.nodes:
        # print(target_word)
        if target_word != word:
            try:
                shortest_path = nx.shortest_path(graph, source=word, target=target_word, weight='weight')
                shortest_paths[target_word] = shortest_path
            except nx.NetworkXNoPath:
                shortest_paths[target_word] = "无法找到从 {} 到 {} 的路径".format(word, target_word)
        print(shortest_paths)
    return shortest_paths


# 将路径按指定格式输出
def format_path_as_string(path):
    return '→'.join(path)

# 随机遍历图
def random_traversal(graph):
    visited_nodes = []
    visited_edges = []
    current_node = random.choice(list(graph.nodes()))
    
    while True:
        visited_nodes.append(current_node)
        neighbors = list(graph.neighbors(current_node))
        
        if len(neighbors) == 0:
            break
        
        next_node = random.choice(neighbors)
        visited_edges.append((current_node, next_node))
        
        if next_node in visited_nodes:
            break
        
        current_node = next_node
    
    return visited_nodes, visited_edges

# 输出遍历结果到文本文件
def output_traversal_result(file_path, nodes, edges):
    with open(file_path, 'w') as file:
        file.write("遍历节点: {}\n".format(' '.join(nodes)))
        file.write("遍历边: {}\n".format(' '.join(map(str, edges))))

# 主函数
def main():
    # 从用户输入或命令行参数获取文件路径和文件名
    file_path = input("请输入文本文件的路径和文件名：")

    # file_path = "text_data.txt"  # 你的文本文件路径
    # 检查文件路径是否存在
    while not os.path.isfile(file_path):
        print("文件路径不存在，请重新输入。")
        file_path = input("请输入文本文件的路径和文件名：")
        
    
    
    # 创建有向图
    graph = create_digraph_from_file(file_path)
    print("成功创建有向图！")
    
    # 可视化有向图
    visualize_digraph(graph)

    # print("请输入工程代号以选择功能：\n1. 查找桥接词\n2. 处理新文本并插入桥接词\n3. 查找最短路径\n4. 随机遍历图\n5. 退出系统")
    while True:
        print("\n请输入工程代号以选择功能：\n1. 查找桥接词\n2. 处理新文本并插入桥接词\n3. 查找最短路径\n4. 随机遍历图\n5. 退出系统")
        choice = input("\n请输入选项：")
        choice_list = ['1', '2', '3', '4', '5']
        
        if choice not in choice_list:
            print("无效选项，请重新输入。")
            continue

        if choice == '1':
            # 输入两个单词
            word1 = input("请输入第一个单词：")
            word2 = input("请输入第二个单词：")
            
            if word1 not in graph.nodes or word2 not in graph.nodes:
                print("单词 {} 或 {} 不在图中，请重新操作。".format(word1, word2))
                continue
            # 查找桥接词
            # result = find_bridge_words(graph, word1, word2)
            # print(result)
            
        elif choice == '2':
            # 输入新文本
            new_text = input("请输入一行新文本：")
            # new_text = "sek new seek new"  # 你的新文本
            
            # 处理新文本并插入桥接词
            processed_text = process_text_with_bridge_words(graph, new_text)
            print("处理后的文本：", processed_text)
            
        elif choice == '3':
            # 输入两个单词
            word1 = input("请输入第一个单词：")
            word2 = input("请输入第二个单词：")

            if word1 not in graph.nodes:
                print("单词 {} 不在图中，请重新操作。".format(word1))
                continue

            if word1 in graph.nodes and word2 == '':
                shortest_paths = find_shortest_paths_to_other_words(graph, word1)
                if shortest_paths:
                    for key, value  in shortest_paths.items():
                        if type(value) == list:
                            print("{} : {}".format(key, format_path_as_string(value)))
                        else:
                            print("{} : {}".format(key, value))
                    continue
                else:
                    print("输入的两个单词不可达！")
                    continue

            # 查找最短路径
            shortest_path = find_shortest_path(graph, word1, word2)
            if shortest_path:
                print("最短路径为:", format_path_as_string(shortest_path))
            else:
                print("输入的两个单词不可达！")

        
        elif choice == '4':
            # 随机遍历图
            nodes, edges = random_traversal(graph)
            
            # 输出遍历结果到文本文件
            output_traversal_result("traversal_result.txt", nodes, edges)
            print("遍历结果已保存到 traversal_result.txt 文件中。")

        elif choice == '5':
            print("感谢使用文本处理系统，再见！")
            break


if __name__ == "__main__":
    main()
