import subprocess
import sys
import os
import time

response=[]
x=[]
y=[]
logs=[]

def read_file(file_path):
    """讀取文件內容，並根據空行切分成多個段落"""
    global logs
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content.strip().split('\n\n')
    except FileNotFoundError:
        logs.append(f"Error: File not found - {file_path}")
        sys.exit(1)
    except Exception as e:
        logs.append(f"Error reading file {file_path}: {str(e)}")
        sys.exit(1)

def run_cpp_program(executable, input_data):
    """執行指定的 C++ 可執行檔，並傳遞輸入資料"""
    try:
        start_time = time.time()  # 開始計時
        process = subprocess.run(
            [executable], 
            input=input_data.encode('utf-8'), 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            timeout=5
        )
        end_time = time.time()  # 結束計時
        elapsed_time = end_time - start_time  # 計算執行時間

        stdout = process.stdout.decode('utf-8').strip()
        stderr = process.stderr.decode('utf-8').strip()
        return stdout, stderr, elapsed_time
    except subprocess.TimeoutExpired:
        return "<Timeout>", None, 10.0  # 預設超時為 10 秒
    except Exception as e:
        return None, f"<Error: {str(e)}>", None

def main():
    global logs
    input_file, output_file = 'in.txt', 'out.txt'
    cpp_executable = './1.exe'

    # 檢查可執行檔是否存在
    if not os.path.isfile(cpp_executable):
        logs.append(f"Error: Executable not found - {cpp_executable}")
        sys.exit(1)

    # 讀取輸入和輸出
    inputs = read_file(input_file)
    expected_outputs = read_file(output_file)

    if len(inputs) != len(expected_outputs):
        logs.append("Error: Number of inputs and outputs do not match.")
        sys.exit(1)

    # 逐一測試
    passed = 0
    all = 0
    all_passed = True
    for i, (input_data, expected_output) in enumerate(zip(inputs, expected_outputs)):
        global x
        global y
        logs.append(f"Running test case {i + 1}...")
        actual_output, stderr, elapsed_time = run_cpp_program(cpp_executable, input_data)

        x.append(int(input_data.split(' ')[0]))
        y.append(elapsed_time)

        if stderr:
            logs.append(f"  Test case {i + 1} error: {stderr}")
            all_passed = False
            continue

        logs.append(f"  Execution time: {elapsed_time:.3f} seconds") # 顯示執行時間

        if actual_output == expected_output:
            logs.append(f"  Test case {i + 1}: PASSED")
            passed+=1
        else:
            all_passed = False
            logs.append(f"  Test case {i + 1}: FAILED")
            logs.append(f"    Input: {input_data}")
            logs.append(f"    Expected: {expected_output}")
            logs.append(f"    Actual: {actual_output}")
        all+=1

    if all_passed:
        logs.append("")
        logs.append("All test cases passed!")
    else:
        logs.append("")
        logs.append("Some test cases failed.")

    sorted_pairs = sorted(zip(x, y), key=lambda pair: pair[0])
    x_sorted, y_sorted = zip(*sorted_pairs)

    response.append(x_sorted)
    response.append(y_sorted)
    response.append(logs)
    response.append([passed, all])

if __name__ == '__main__':
    main()
