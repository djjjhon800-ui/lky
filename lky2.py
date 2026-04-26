import tkinter as tk
import random
import time
import math
from threading import Thread

# 自定义文字内容（可按需修改）
texts = [
    "我想你了！", "天冷了多穿衣服哦", "好喜欢你", "❤️",
    "好想抱抱你", "永远爱你", "我的宝贝", "❤️❤️❤️",
    "想你想到心疼", "好喜欢你哦", "好好爱自己", "别熬夜"
]


class FloatingWindow:
    def __init__(self, root, text, x, y, is_heart_mode=False):
        self.window = tk.Toplevel(root)
        self.window.overrideredirect(True)
        self.window.attributes('-topmost', True)
        self.window.configure(bg='white')  # 改为白色背景，和示例效果一致

        # 弹窗颜色（使用示例中的柔和色系）
        color_list = ['lightblue', 'lightgreen', 'lightpink', 'lemonchiffon', 'white']
        bg_color = random.choice(color_list)
        text_color = random.choice(['black', '#FF1493', '#FF69B4'])

        # 文字大小（爱心模式用统一大小，更整齐）
        size = 14 if is_heart_mode else random.randint(16, 28)

        self.label = tk.Label(
            self.window, text=text,
            font=("微软雅黑", size, "bold"),
            fg=text_color, bg=bg_color,
            padx=10, pady=6
        )
        self.label.pack()

        self.window.geometry(f"+{x}+{y}")
        self.window.attributes('-alpha', 0.95)

        # 运动参数（爱心模式固定为0，不移动；飘字模式随机速度）
        if is_heart_mode:
            self.dx = 0
            self.dy = 0
            self.is_heart_mode = True
        else:
            self.dx = random.uniform(-3.5, 3.5)
            self.dy = random.uniform(-4.5, 1.5)
            self.is_heart_mode = False

        self.life = 0
        self.animate()

    def animate(self):
        try:
            # 爱心模式：弹窗固定位置，仅做轻微呼吸效果
            if self.is_heart_mode:
                self.life += 1
                alpha = 0.9 + 0.1 * math.sin(self.life / 20)
                self.window.attributes('-alpha', alpha)
                self.window.after(100, self.animate)
                return

            # 飘字模式：正常自由移动
            x = self.window.winfo_x()
            y = self.window.winfo_y()
            sw = self.window.winfo_screenwidth()
            sh = self.window.winfo_screenheight()

            self.life += 1
            new_x = int(x + self.dx + math.sin(self.life / 15) * 2)
            new_y = int(y + self.dy)

            # 边界反弹
            if new_x < 20 or new_x > sw - 220:
                self.dx = -self.dx
            if new_y < 30 or new_y > sh - 100:
                self.dy = -self.dy * 0.9
                if new_y > sh - 80:
                    new_y = random.randint(50, 200)

            # 透明度呼吸效果
            alpha = 0.75 + 0.25 * math.sin(self.life / 10)
            self.window.attributes('-alpha', alpha)

            self.window.geometry(f"+{new_x}+{new_y}")
            self.window.after(35, self.animate)
        except:
            pass


def create_fullscreen_floating(root, total=70):
    """第一阶段：先执行满屏飘字效果"""
    print("✨ 第一阶段：满屏飘字启动...")
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()

    for i in range(total):
        text = random.choice(texts)
        x = random.randint(30, sw - 220)
        y = random.randint(30, sh // 2)
        FloatingWindow(root, text, x, y, is_heart_mode=False)
        time.sleep(0.025)


def create_heart_stack(root, total=80):
    """第二阶段：飘字结束后，弹出固定位置的爱心弹窗"""
    print("❤️ 第二阶段：爱心堆叠启动...")
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()

    for i in range(total):
        # 心形坐标公式（保证弹窗位置正确组成爱心）
        t = i / total * math.pi * 2
        scale = 165
        x = int(sw * 0.5 + scale * 16 * math.pow(math.sin(t), 3))
        y_base = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        target_y = int(sh * 0.55 - scale * 0.82 * y_base)

        # 直接在目标位置生成弹窗，不做移动动画
        text = random.choice(texts)
        FloatingWindow(root, text, x, target_y, is_heart_mode=True)

        # 轮流弹出延迟，让爱心慢慢成型
        time.sleep(0.06 if i < 40 else 0.04)

    print("✅ 爱心弹窗已全部弹出！")


def main():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    print("浪漫双阶段爱心弹窗启动中...\n")

    # 第一阶段：先启动满屏飘字
    Thread(target=create_fullscreen_floating, args=(root, 70), daemon=True).start()

    # 第二阶段：飘字结束后启动爱心堆叠（延迟10秒，可按需调整）
    def start_second_phase():
        time.sleep(10)
        create_heart_stack(root, 80)

    Thread(target=start_second_phase, daemon=True).start()

    root.mainloop()


if __name__ == "__main__":
    main()
zz