import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
from tqdm import tqdm

# 初期化
N = 1
# todo: 最終的には再生時間を指定して自動で調整する
# 絵が変わる間隔(s)
PLOT_INTERVAL = 0.1
# 座標を計算する間隔
POINT_INTERVAL = 0.1
# 小さい方の質量
M_1 = 100**N
M_2 = 1
# 初速度
V_1 = -1.
V_2 = 0.
# ブロックのサイズ
S_1 = round((N + 1) ** (1 / 2), 1)
S_2 = 1
# 左端の座標
X_1 = S_1 * 6
X_2 = S_1 * 4

BLOCK_INFO = {'mass': (M_1, M_2),
              'velocity': (V_1, V_2),
              'size': (S_1, S_2),
              'point': (X_1, X_2)}


def main():
    points = calc_coordinate(N, POINT_INTERVAL, BLOCK_INFO)
    # plot_graph(POINT_INTERVAL, points)
    ani = make_animation(BLOCK_INFO, PLOT_INTERVAL, points)
    plt.show()
    if input('save or plot: ')[0] == 's':
        ani.save('colliding_block_pi{:03}.gif'.format(N))


# ブロック同士衝突するまでの時間を計算する関数
def time_collide_blocks(x, v, s):
    time = (x[1] - x[0] + s[1]) / (v[0] - v[1])  # todo: s_2はグローバル変数なのでどうにかする
    return time


# 壁と衝突するまでの時間を計算する関数
def time_collide_wall(x, v):
    try:  # N = 0の時終了条件を満たした後もこの関数を呼び出してしまいエラーが出るため
        time = x[1] / -v[1]
    except ZeroDivisionError:
        time = None
    return time


# dt秒後の座標を返す関数
def point_update(x, v, dt):
    x0 = x[0] + v[0] * dt
    x1 = x[1] + v[1] * dt
    return x0, x1


# ブロック同士の衝突後の速度を計算する関数
def velocity_collide_blocks(v, r):
    v0 = ((r - 1) * v[0] + 2 * v[1]) / (r + 1)
    v1 = (2 * r * v[0] - (r - 1) * v[1]) / (r + 1)
    return v0, v1


# 壁とブロックの衝突後の速度を計算する関数
def velocity_collide_wall(v):
    return v[0], -v[1]


# 衝突後すぐにアニメーションが終了すると面白くなので数秒後までの座標を計算する関数
def lingering_point(v, interval, x_list, count_list, time=5):
    count = count_list[-1] + 1
    x = x_list[-1]
    for _ in range(int(time / interval)):
        x = point_update(x, v, interval)
        x_list.append(x)
        count_list.append(count)
    return x_list, count_list


def calc_coordinate(n, interval, block_info, print_info=False):
    v = block_info['velocity']
    x = block_info['point']
    s = block_info['size']
    r = 100 ** n
    count = 0  # 衝突回数
    x_list = []
    count_list = []
    flag = True  # 交互にブロックと壁の関数を呼ぶためのフラグ変数
    bar = tqdm(total=int(10 ** n * np.pi))  # tqdmを手動で動かすため

    time = time_collide_blocks(x, v, s)
    while not(0 <= v[1] <= v[0]):
        while time >= 0:  # intervalおきに座標を計算する
            if print_info:
                print('v0: {:.16f}  v1: {:.16f}  x0: {:.16f}  x1: {:.16f}  '
                      'count:{}'.format(v[0], v[1], x[0], x[1], count))
            x_list.append(x)
            count_list.append(count)
            x = point_update(x, v, interval)
            time -= interval
        x = point_update(x, v, time)  # 座標を補正
        if print_info:
            print('-'*30 + '補正' + '-'*30)
        if flag:
            v = velocity_collide_blocks(v, r)
            time = time_collide_wall(x, v)
        else:
            v = velocity_collide_wall(v)
            time = time_collide_blocks(x, v, s)
        count += 1
        flag = not flag
        bar.update(1)
    x_list, count_list = lingering_point(v, interval, x_list, count_list)

    return list(zip(x_list, count_list))


def plot_graph(interval, points):
    plt.plot(np.arange(0, interval * len(points[0]), interval),
             np.array(points[0])[:, 0], label='v0')
    plt.plot(np.arange(0, interval * len(points[0]), interval),
             np.array(points[0])[:, 1], label='v1')
    plt.show()


def init_animation(block_info):
    # グラフの初期化をする関数
    fig, ax = plt.subplots()
    b1 = patches.Rectangle(xy=(block_info['point'][0], 0),
                           width=block_info['size'][0],
                           height=block_info['size'][0],
                           facecolor='silver')
    b2 = patches.Rectangle(xy=(block_info['point'][1], 0),
                           width=block_info['size'][1],
                           height=block_info['size'][1],
                           facecolor='dimgray')
    ax.add_patch(b1)
    ax.add_patch(b2)
    ax.grid(True)
    length = block_info['point'][0] * 1.2
    ax.set_xlim(-1, length)
    ax.set_ylim(-1, length)
    ax.axhline(0)
    ax.axvline(0)
    ax.legend((b1, b2),
              (str(block_info['mass'][0]), str(block_info['mass'][1])))
    count_bar = ax.text(0.05, 0.9, 'Count: 0', transform=ax.transAxes)

    return fig, ax, (b1, b2), count_bar


def update(frame, ax, b, count_bar):
    # グラフの更新をする関数
    x, count = frame
    b1, b2 = b
    length = x[1] * 1.2
    ax.set_xlim(-1, length)
    ax.set_ylim(-1, length)
    b1.set_x(x[0])
    b2.set_x(x[1])
    count_bar.set_text('Count: ' + str(count))


def make_animation(block_info, plot_interval, frames):
    # 上二つとfuncAnimationを使ってアニメーションを作る関数
    fig, ax, b, count_bar = init_animation(block_info)
    ani = animation.FuncAnimation(fig, update, fargs=(ax, b, count_bar),
                                  interval=plot_interval, frames=frames)
    return ani


if __name__ == '__main__':
    main()
