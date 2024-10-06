import matplotlib.pyplot as plt

# 初始化變數
icmp_seq = []
times = []

# 讀取檔案
with open('ue.txt', 'r') as file:
    for line in file:
        # 解析每行數據
        parts = line.split()
        seq_num = int(parts[4].split('=')[1])
        time = float(parts[6].split('=')[1])
        
        # 將解析結果添加到列表
        icmp_seq.append(seq_num)
        times.append(time)

# 繪製折線圖
plt.plot(icmp_seq, times, linestyle='-', color='b')

# 添加標題和標籤
plt.title('Ping Response Times')
plt.xlabel('ICMP Sequence Number')
plt.ylabel('Time (ms)')

plt.ylim(0, 100)

# 顯示圖表
plt.grid(True)
plt.savefig('ue.png')
plt.show()
