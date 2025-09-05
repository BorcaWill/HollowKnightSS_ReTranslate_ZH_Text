"""
批量翻译流程脚本（使用时请删除命令前的#号）

1. 批量导出csv：
	# 作用：将ZH文件夹下所有ZH_xxx.txt与EN/EN_xxx.txt配对，批量导出为csv/xxx.csv，便于人工或机器翻译。

2. 批量英译中：
	# 作用：对csv文件夹下所有csv文件批量进行英译中，自动填充/覆盖ZH列。

3. 批量把csv转换为txt：
	# 作用：将csv/xxx.csv中的ZH列内容批量写回ZH/ZH_xxx.txt，实现批量生成翻译文本。
"""

# 1. 批量导出csv
# python3 converter.py export

# 2. 批量英译中
# python3 MT.py

# 3. 批量把csv文件夹内的所有csv转换为txt
python3 converter.py import