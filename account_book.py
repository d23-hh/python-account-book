# -*- coding: utf-8 -*-
import json

# 全局变量
records = []
DATA_FILE = "account_data.json"

# 加载数据
def load_data():
    global records
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            records = json.load(f)
        print("数据加载成功！")
    except FileNotFoundError:
        print("未找到数据文件，将创建新文件。")
    except json.JSONDecodeError:
        print("数据文件损坏，将创建新文件。")

# 保存数据
def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=4)

# 显示主菜单
def show_menu():
    print("\n" + "="*30)
    print("      个人记账本 v1.1")
    print("1. 添加收支记录")
    print("2. 查询所有记录")
    print("3. 统计收支情况")
    print("4. 删除记录")
    print("5. 修改记录")
    print("0. 退出程序")
    print("="*30)

# 添加记录
def add_record():
    print("\n--- 添加收支记录 ---")
    date = input("请输入日期(格式:YYYY-MM-DD);")
    
    while True:
        type_ = input("请输入类型（收入/支出）：")
        if type_ in ["收入", "支出"]:
            break
        print("输入错误，请输入'收入'或'支出'!")
    
    while True:
        try:
            amount = float(input("请输入金额："))
            if amount > 0:
                break
            print("金额必须大于0，请重新输入！")
        except ValueError:
            print("输入错误，请输入数字！")
    
    category = input("请输入类别（如：餐饮、交通、工资）：")
    remark = input("请输入备注（可选）：")
    
    record = {
        "date": date,
        "type": type_,
        "amount": amount,
        "category": category,
        "remark": remark
    }
    records.append(record)
    save_data()
    print("记录添加成功！")

# 查询所有记录
def query_records():
    print("\n--- 所有收支记录 ---")
    if not records:
        print("暂无记录！")
        return
    
    print(f"{'序号':<4}{'日期':<12}{'类型':<8}{'金额':<10}{'类别':<10}{'备注'}")
    print("-"*55)
    
    for i, record in enumerate(records, 1):
        print(f"{i:<4}{record['date']:<12}{record['type']:<8}{record['amount']:<10.2f}{record['category']:<10}{record['remark']}")

# 统计收支
def statistics():
    print("\n--- 收支统计 ---")
    if not records:
        print("暂无记录，无法统计！")
        return
    
    total_income = 0.0
    total_expense = 0.0
    
    for record in records:
        if record["type"] == "收入":
            total_income += record["amount"]
        elif record["type"] == "支出":
            total_expense += record["amount"]
    
    balance = total_income - total_expense
    
    print(f"总收入：{total_income:.2f} 元")
    print(f"总支出：{total_expense:.2f} 元")
    print(f"当前结余：{balance:.2f} 元")

# 删除记录
def delete_record():
    print("\n--- 删除收支记录 ---")
    if not records:
        print("暂无记录可删除！")
        return
    
    print(f"{'序号':<4}{'日期':<12}{'类型':<8}{'金额':<10}{'类别':<10}{'备注'}")
    print("-"*55)
    for i, record in enumerate(records, 1):
        print(f"{i:<4}{record['date']:<12}{record['type']:<8}{record['amount']:<10.2f}{record['category']:<10}{record['remark']}")
    
    while True:
        try:
            index = int(input("\n请输入要删除的记录序号(输入0取消）："))
            if index == 0:
                print("已取消删除操作。")
                return
            if 1 <= index <= len(records):
                break
            print(f"序号无效！请输入1到{len(records)}之间的数字。")
        except ValueError:
            print("输入错误，请输入数字！")
    
    confirm = input(f"确定要删除第{index}条记录吗？(y/n)：")
    if confirm.lower() == "y":
        del records[index-1]
        save_data()
        print("记录删除成功！")
    else:
        print("已取消删除操作。")

# 修改记录
def modify_record():
    print("\n--- 修改收支记录 ---")
    if not records:
        print("暂无记录可修改！")
        return
    
    print(f"{'序号':<4}{'日期':<12}{'类型':<8}{'金额':<10}{'类别':<10}{'备注'}")
    print("-"*55)
    for i, record in enumerate(records, 1):
        print(f"{i:<4}{record['date']:<12}{record['type']:<8}{record['amount']:<10.2f}{record['category']:<10}{record['remark']}")
    
    while True:
        try:
            index = int(input("\n请输入要修改的记录序号（输入0取消）："))
            if index == 0:
                print("已取消修改操作。")
                return
            if 1 <= index <= len(records):
                break
            print(f"序号无效！请输入1到{len(records)}之间的数字。")
        except ValueError:
            print("输入错误，请输入数字！")
    
    record = records[index-1]
    print("\n--- 原记录内容 ---")
    print(f"日期：{record['date']}")
    print(f"类型：{record['type']}")
    print(f"金额：{record['amount']}")
    print(f"类别：{record['category']}")
    print(f"备注：{record['remark']}")
    print("\n提示：直接按回车保留原值")
    
    new_date = input(f"请输入新日期 [{record['date']}]：") or record['date']
    
    while True:
        new_type = input(f"请输入新类型（收入/支出） [{record['type']}]：") or record['type']
        if new_type in ["收入", "支出"]:
            break
        print("输入错误，请输入'收入'或'支出'！")
    
    while True:
        amount_input = input(f"请输入新金额 [{record['amount']}]：") or str(record['amount'])
        try:
            new_amount = float(amount_input)
            if new_amount > 0:
                break
            print("金额必须大于0，请重新输入！")
        except ValueError:
            print("输入错误，请输入数字！")
    
    new_category = input(f"请输入新类别 [{record['category']}]：") or record['category']
    new_remark = input(f"请输入新备注 [{record['remark']}]：") or record['remark']
    
    confirm = input("\n确定要修改这条记录吗？(y/n)：")
    if confirm.lower() == "y":
        record['date'] = new_date
        record['type'] = new_type
        record['amount'] = new_amount
        record['category'] = new_category
        record['remark'] = new_remark
        save_data()
        print("记录修改成功！")
    else:
        print("已取消修改操作。")

# 主程序入口（这是最关键的部分！）
if __name__ == "__main__":
    load_data()
    print("欢迎使用个人记账本！")
    
    while True:
        show_menu()
        choice = input("请输入您的选择：")
        
        if choice == "0":
            print("感谢使用，再见！")
            break
        elif choice == "1":
            add_record()
        elif choice == "2":
            query_records()
        elif choice == "3":
            statistics()
        elif choice == "4":
            delete_record()
        elif choice == "5":
            modify_record()
        else:
            print("输入错误，请重新选择！")