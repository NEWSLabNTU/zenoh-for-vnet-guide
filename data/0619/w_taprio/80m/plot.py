import re
import argparse
import matplotlib.pyplot as plt

def main(port):
    # 初始化一个列表来存储Reliability值
    reliabilities = []

    # 遍历文件名
    for i in range(1, 11):
        filename = f'exp{i}.txt'
        
        with open(filename, 'r') as file:
            content = file.read()
            
            # 使用正则表达式查找指定Port的Reliability值
            pattern = rf'Port {port}:\s+Received packets: \d+\s+Jitter: [\d.]+ seconds\s+Reliability: ([\d.]+) %'
            match = re.search(pattern, content)
            if match:
                reliability = float(match.group(1))
                reliabilities.append(reliability)

    # 计算平均数
    average_reliability = sum(reliabilities) / len(reliabilities)

    # 绘制折线图
    plt.plot(range(1, 11), reliabilities, marker='o', linestyle='-', color='b', label='Reliability')
    plt.axhline(y=average_reliability, color='r', linestyle='--', label=f'Average Reliability ({average_reliability:.2f}%)')
    plt.xlabel('Experiment Number')
    plt.ylabel('Reliability (%)')
    plt.title(f'Control Message Reliability')
    plt.ylim(50, 100)
    plt.xticks(range(1, 11))  # 设置x轴刻度
    plt.legend()
    plt.grid(True)
    plt.savefig(f'port{port}.png')
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot Reliability for a specific Port.')
    parser.add_argument('port', type=int, help='The port number to analyze.')
    
    args = parser.parse_args()
    main(args.port)
