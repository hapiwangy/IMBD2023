# 這個是把accumulation_hour裡面的東西畫成圖表
import pandas as pd
import matplotlib.pyplot as plt
import os

original_data = pd.read_csv(f"../2023全國智慧製造大數據分析競賽_初賽訓練數據公告資料/accumlation_hour.csv", encoding="utf-8")
dicts = {}
oven_ids = list(original_data["oven_id"])
# print(oven_ids)
for x in oven_ids:
    dicts[x] = original_data[original_data["oven_id"] == x]
# 每個layer、在不同時間(x)累積使用的時數(y)
# 定義劃一個oven中所有layer的函數
def drawOneLayer(ovenName: str, ):
    curpath = os.getcwd()
    if os.path.isfile(f"{curpath}/{ovenName}"):
        pass
    else:
        os.mkdir(ovenName)
    os.chdir(ovenName)
    oven = dicts[ovenName]
    layers = list(range(1, 20))
    for x in layers:
        slayer = oven[oven['layer_id'] == x]
        x_axis = list(slayer['date'])
        y_axis = list(slayer['accumulation_hour'])
        plt.plot(x_axis, y_axis)
        # plt.show()
        plt.savefig(f"layer_{x}.png")
    os.chdir(curpath)

# 依照爐子，把特定的累積使用時數整理起來
def deal_data(ovenName: str):
    # 2B0的話取用6、11、12、13、14、15、16、17、19
    layers = [6,11,12,13,14,15,16,17,19]
    oven = dicts[ovenName]

if __name__ == '__main__':
    for id in set(oven_ids):
        if id[0] == '2':
            drawOneLayer(id)
        else :
            pass
