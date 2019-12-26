import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tqdm import tqdm

# 初期化

N = 3

# 絵が変わる間隔(s)
INTERVAL = 0.05
#　小さい方の質量
m_1 = 100**N
m_2 = 1
# 初速度
v_1 = -1.
v_2 = 0.
#　ブロックのサイズ
s_1 = round((N + 1) ** (1 / 2), 1)
s_2 = 1
# 左端の座標
x_1 = s_1 * 6
x_2 = s_1 * 4

R = 100**N
v = v_1, v_2
x = x_1, x_2

# ブロック同士衝突するまでの時間を計算する関数
def time_collide_blocks(x, v):
    time = (x[1] - x[0] + s_2) / (v[0] - v[1])
    return time

# 壁と衝突するまでの時間を計算する関数
def time_collide_wall(x, v):
    try: # N = 0の時終了条件を満たした後もこの関数を呼び出してしまいエラーが出るため
        time = x[1] / -v[1]
    except ZeroDivisionError:
        time = None
    return time

# dt秒後の座標を返す関数
def point_update(x, v, dt):
    x0 = x[0] + v[0] * dt
    x1 = x[1] + v[1] * dt
    return x0, x1

point_update([1, 1], [-1, -1], 0.1)

# ブロック同士の衝突後の速度を計算する関数
def velocity_collide_blocks(v, R):
    v0 = ((R - 1) *  v[0] + 2 * v[1]) / (R + 1)
    v1 = (2 * R * v[0] -  (R - 1) * v[1]) / (R + 1)
    return v0, v1

# 壁とブロックの衝突後の速度を計算する関数
def velocity_collide_wall(v):
    return v[0], -v[1]

# 衝突後すぐにアニメーションが終了すると面白くなので数秒後までの座標を計算する関数
def lingering_point(v, INTERVAL,  x_list, count_list, time=3):
    count = count_list[-1]
    x = x_list[-1]
    for _ in range(int(time / INTERVAL)):
        x = point_update(x, v, INTERVAL)
        x_list.append(x)
        count_list.append(count)
    return x_list, count_list

def calc_coordinate(N, INTERVAL,  v, x, print_info=False):
    count = 0 # 衝突回数
    x_list = []
    count_list = []
    flag = True # 交互にブロックと壁の関数を呼ぶためのフラグ変数
    bar = tqdm(total=int(10 ** N * np.pi)) # tqdmを手動で動かすため

    time = time_collide_blocks(x, v)
    while not(0 <= v[1] <= v[0]):
        while time >= 0: # INTERVALおきに座標を計算する
            if print_info:
                print('v0: {:.16f}  v1: {:.16f}  x0: {:.16f}  x1: {:.16f}  count:{}'.format(v[0], v[1], x[0], x[1], count))
            x_list.append(x)
            count_list.append(count)
            x = point_update(x, v, INTERVAL)
            time -= INTERVAL
        x = point_update(x, v, time) # 座標を補正
        if print_info:
            print('-'*30 + '補正' + '-'*30)
        if flag:
            v = velocity_collide_blocks(v, R)
            time = time_collide_wall(x, v)
        else:
            v = velocity_collide_wall(v)
            time = time_collide_blocks(x, v)
        count += 1
        flag = not flag
        bar.update(1)
        # x_list, count_list = lingering_point(v, INTERVAL, x_list, count_list)
    return x_list, count_list

a = calc_coordinate(N, INTERVAL, v, x, 1)

plt.plot(np.arange(0, INTERVAL * len(a[0]), INTERVAL), np.array(a[0])[:, 0])
plt.plot(np.arange(0, INTERVAL * len(a[0]), INTERVAL), np.array(a[0])[:, 1])
plot.show
