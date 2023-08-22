# 會把區間內的錯誤數量總和之後做紀錄
import pandas as pd
import matplotlib.pyplot as plt
# 引入時間相觀模組，比大小的時候會用到
import time
formats = "%Y/%m/%d"
# 引入時間區間(跟累積使用時數的區間相同)
targets = ['2022/5/4','2022/6/2','2022/6/30', '2022/7/30','2022/8/15','2022/9/1',
'2022/9/28','2022/10/31','2022/11/28','2022/12/28','2023/2/6']
# 引入資料
datas = pd.read_csv(f"./2023全國智慧製造大數據分析競賽_初賽訓練數據公告資料/anomaly_train.csv", encoding="utf-8")
# 定義要用的ovens
ovens_id = ['2B0','2C0','2D0','2E0','2G0']
# 定義要用的function
# 把str轉成time物件可以接受的型式
def change_format(dates: str) -> str:
    din = dates.split('/')
    if int(din[1]) < 10:
        din[1] = "0"+str(din[1])
    if int(din[2]) < 10:
        din[2] = "0" + str(din[2])
    return "/".join(din)
# 判斷要插入到哪裡
def insert_into_where(dates:list, date: str):
    formats = "%Y/%m/%d"
    # print(dates)
    date = time.strptime(change_format(date), formats)
    dates = [time.strptime(x, formats) for x in dates]
    # print(dates)
    if date < dates[0]:
        return None
    for d in dates[1:]:
        if date <= d:
            return time.strftime(formats, d)

def main():
    flag = 0
    for oven in ovens_id:
        # 目前在分析那個爐子
        current = datas[datas['oven_id'] == oven]
        # 分析當前有哪些日期
        dates = set(datas['date'])
        # 紀錄爐子的錯誤發生
        dsum = {}
        for d in dates:
            dsum[d] = current[current['date'] == d]['anomaly_total_number'].sum()
        # 初始化紀錄的容器
        accumulation = {'2022/05/04':0}
        for x in targets[1:]:
            accumulation[change_format(x)] = 0
        # 進行容器的建置
        for d, v in dsum.items():
            answer = insert_into_where(targets, d)
            if answer:
                accumulation[answer] += v
        if not flag:
            df = pd.DataFrame({
                'oven_id' : [f'{oven}' for _ in range(len(targets))],
                'dates' : list(accumulation.keys()),
                'error_num' : list(accumulation.values())
            })
            flag = 1
        else :
            new_df = pd.DataFrame({
                'oven_id' : [f'{oven}' for _ in range(len(targets))],
                'dates' : list(accumulation.keys()),
                'error_num' : list(accumulation.values())
            })
            df = pd.concat([df, new_df], ignore_index=True) 
        x = list(accumulation.keys())
        y = list(accumulation.values())
        plt.plot(x, y)
        plt.savefig(f"{oven}_errors")
        plt.close()
    return df
if __name__ == '__main__':
    df = main()
    df.to_csv('test_errornumber.csv')
