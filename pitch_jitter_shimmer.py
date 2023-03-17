"""
调用praat程序计算wav文件的pitch、jitter和shimmer参数
"""

__author__ = 'zej-luffy'
__date__ = '2018/4/10'

import os
import sys

# sys.path.append(os.path.join(os.path.dirname(__file__), './praat'))
print(sys.path)
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import parselmouth
import platform

path=r'C:\Users\user\Desktop\123\pitch_jitter_shimmer\test\ID17.wav'

__all__ = ['PitchJitterShimmer']


def is_os_window():
    """
    判断是window系统
    :return: True/False
    """
    sysstr = platform.system()
    if (sysstr.lower() == "windows"):
        return True
    elif (sysstr.lower() == "linux"):
        return False
    return False


class PitchJitterShimmer(object):
    def __init__(self, praat_file, praat_path='./praat'):
        """
        初始化
        :param praat_file: praat_file脚本文件的路径
        :param praat_path: praat可执行程序的路径
        """
        super(PitchJitterShimmer, self).__init__()
        exec_file = 'praat.exe' if is_os_window() else 'praat'
        if not os.path.exists(os.path.join(praat_path, exec_file)):
            print('Not found runnable praat. Exit.')
            exit(1)
        self.praat_file = praat_file
        self.praat_path = praat_path

    def calculate(self, voice_file, save_file=False):
        """
        开始计算
        :param voice_file: 声音文件
		:param save_file: 是否保留文件
        :return: pd.DataFrame
        """
        voice_file = os.path.abspath(voice_file)
        exec_file = os.path.join(os.path.abspath(self.praat_path), 'praat')
        command = '{} {} {}'.format(exec_file, self.praat_file, voice_file)
        os.system(command)
        # 读取文件
        csv_file = voice_file.replace('.wav', '.csv')
        df = pd.read_csv(csv_file)
        if not save_file:
            os.remove(csv_file)
        return df


def main():
    praat_file = './praat/praat.praat'
    praat_path = './praat'
    pjs = PitchJitterShimmer(praat_file, praat_path)
    voice_file = path
    print(pjs.calculate(voice_file, True))
    sns.set()
# Plot nice figures using Python's "standard" matplotlib library
    snd = parselmouth.Sound(path)
    plt.figure()
    plt.plot(snd.xs(), snd.values.T)
    plt.xlim([snd.xmin, snd.xmax])
    plt.xlabel("time [s]")
    plt.ylabel("amplitude")
# plt.plot(peaks, snd.xs()[peaks], "o")

    plt.show() # or plt.savefig("sound.png"), or plt.savefig("sound.pdf")



if __name__ == '__main__':
    main()
