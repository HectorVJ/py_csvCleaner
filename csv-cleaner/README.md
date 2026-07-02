# CSV 数据清洗与标准化工具

## 使用方法

```bash
python main.py -input sample/input.csv -output output/cleaned.csv
```

## 功能

- 列名标准化：去除空格、转小写、下划线替换
- 空行过滤：删除全为空的行
- 重复行去重：保留首次出现的数据
- 缺失值填充：空单元格填充为 `unknown`
- 输出统计：显示清洗前后行数和处理统计

## 参数说明

- `-input`：输入 CSV 文件路径（必需）
- `-output`：输出 CSV 文件路径（必需）

## 示例输出

```
Original rows: 8
Rows after cleaning: 6
Empty rows removed: 1
Duplicate rows removed: 1
Missing values filled: 3
Output file: output/cleaned.csv
```