import pyperclip
import pyperclipimg
import time
import requests
import base64
import subprocess

from flask import request_started

#CONFIG
machine_id = 1002
base_url = "http://127.0.0.1:5000" + "/"


def get_clipboard_image_b64():
    """
    使用 xclip 直接读取剪贴板的 image/png 数据。
    类似于 xsel，但支持图片。
    """
    try:
        # 1. 先用 xclip 极速检查是否有 image/png 类型的数据
        # -t TARGETS: 查看当前剪贴板支持的格式
        # -o: 输出
        # stderr=subprocess.DEVNULL: 静默错误输出
        check = subprocess.run(
            ['xclip', '-selection', 'clipboard', '-t', 'TARGETS', '-o'],
            capture_output=True, text=True, check=True
        )

        # 如果剪贴板里没有 png 格式，直接返回，不浪费时间读取数据
        if 'image/png' not in check.stdout:
            return None

        # 2. 确认有图片，开始读取二进制数据
        # -t image/png: 指定读取图片格式
        process = subprocess.run(
            ['xclip', '-selection', 'clipboard', '-t', 'image/png', '-o'],
            capture_output=True, check=True
        )

        image_data = process.stdout
        if not image_data:
            return None

        # 3. 拿到二进制数据后，在内存里转 Base64
        # 这一步是纯 CPU 计算，完全不涉及窗口焦点
        return "data:image/jpeg;base64,"+base64.b64encode(image_data).decode('utf-8')

    except subprocess.CalledProcessError:
        return None
    except Exception:
        return None


def copy_base64_to_clipboard(base64_string):
    """
    将 Base64 图片写入剪贴板。
    自动识别是 Wayland 还是 X11 (优先使用 wl-copy)。
    """

    # 1. 清洗数据：去掉 'data:image/png;base64,' 这样的头
    if ',' in base64_string:
        base64_string = base64_string.split(',', 1)[1]

    try:
        # 2. 解码为二进制图片数据
        image_data = base64.b64decode(base64_string)
    except Exception as e:
        print(f"Base64 解码失败: {e}")
        return

    # 3. 尝试写入 (优先 Wayland)
    try:
        # --- 方案 A: Wayland (Fedora 默认) ---
        # wl-copy 接受标准输入，--type 指定图片格式
        # 注意：这里假设是 PNG，如果是 JPEG 改为 image/jpeg
        subprocess.run(
            ['wl-copy', '--type', 'image/png'],
            input=image_data,
            check=True
        )
        print("已写入剪贴板 (Wayland/wl-copy)")
        return

    except FileNotFoundError:
        # 如果找不到 wl-copy，尝试 X11 工具
        pass
    except Exception as e:
        print(f"wl-copy 写入失败: {e}")

    try:
        # --- 方案 B: X11 (xclip) ---
        # -selection clipboard: 写入系统剪贴板
        # -t image/png: 指定类型
        # -i: 读取标准输入
        subprocess.run(
            ['xclip', '-selection', 'clipboard', '-t', 'image/png', '-i'],
            input=image_data,
            check=True
        )
        print("已写入剪贴板 (X11/xclip)")

    except FileNotFoundError:
        print("错误: 未找到 wl-copy 或 xclip，请安装 wl-clipboard 或 xclip")
    except Exception as e:
        print(f"xclip 写入失败: {e}")



pyperclip.set_clipboard("xsel")
clip_cache=""
while True:
    # try:
        clipb = pyperclip.paste() or get_clipboard_image_b64()
        # print(clipb)
        pushed = requests.get(base_url + "/check/"+ str(machine_id)).text
        if pushed == '0':
            print("syncing")
            _sync = requests.get(base_url + "/get_content/"+str(machine_id)).text
            print(_sync)
            if "data:image/jpeg;base64," in _sync:
                copy_base64_to_clipboard(_sync)
            else:
                pyperclip.copy(_sync)
        elif clipb != clip_cache:
            print("change detected")
            #update to server
            req = requests.post(base_url+"/update/"+str(machine_id),data={"data":clipb})
            clip_cache = clipb
        time.sleep(0.1)
    # except Exception:
    #     print("error")