import random

def generate_random_sequences(num_sequences, min_length, max_length, value_range):
    """隨機生成多個序列，每個序列的長度和值範圍可控"""
    sequences = []
    for _ in range(num_sequences):
        length = random.randint(min_length, max_length)
        sequence = [random.randint(value_range[0], value_range[1]) for _ in range(length)]
        sequences.append(sequence)
    return sequences

def write_sequences_to_file(sequences, file_path):
    """將序列寫入文件，每個序列一行"""
    with open(file_path, 'w', encoding='utf-8') as f:
        for sequence in sequences:
            f.write(str(len(sequence))+' ')
            f.write(' '.join(map(str, sequence)) + '\n\n')

def write_sums_to_file(sequences, file_path):
    """計算每個序列的總和並寫入文件，每個總和一行"""
    with open(file_path, 'w', encoding='utf-8') as f:
        for sequence in sequences:
            f.write(str(sum(sequence)) + '\n\n')

def main():
    # 配置參數
    num_sequences = 500  # 要生成的序列數量
    min_length = 100      # 每個序列的最小長度
    max_length = 100000     # 每個序列的最大長度
    value_range = (-200000, 200000)  # 序列中值的範圍

    # 文件路徑
    input_file = 'in.txt'
    output_file = 'out.txt'

    # 生成序列
    sequences = generate_random_sequences(num_sequences, min_length, max_length, value_range)

    # 將序列寫入 in.txt
    write_sequences_to_file(sequences, input_file)

    # 計算總和並寫入 out.txt
    write_sums_to_file(sequences, output_file)

    print(f"Generated {num_sequences} sequences and wrote to {input_file} and {output_file}.")

if __name__ == '__main__':
    main()
