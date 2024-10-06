import matplotlib.pyplot as plt

# 定義文件路徑
file_path = 'result.txt'

# 讀取文件並提取 Bitrate 數據
bitrates = []

with open(file_path, 'r') as file:
    for line in file:
        if 'Mbits/sec' in line:
            parts = line.split()
            bitrate_index = parts.index('Mbits/sec') - 1
            bitrates.append(float(parts[bitrate_index]))

# 計算平均 Bitrate
average_bitrate = sum(bitrates) / len(bitrates)

# 繪製折線圖
plt.figure(figsize=(10, 6))
plt.plot(bitrates, label='Bitrate', color='blue')

# 繪製紅色平均值線
plt.axhline(y=average_bitrate, color='red', linestyle='--', label=f'Average: {average_bitrate:.2f} Mbits/sec')

# 添加標題和標籤
plt.title('Bitrate Over Time')
plt.xlabel('Time(s)')
plt.ylabel('Bitrate (Mbits/sec)')
plt.legend()

# 保存並顯示圖像
plt.savefig('bitrate_plot.png')
plt.show()

