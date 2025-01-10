from flask import Flask, jsonify, request, render_template, send_from_directory
import pyautogui
import time
import threading
from pynput import keyboard
import pydirectinput


app = Flask(__name__)
stop_script = threading.Event()  # 用于控制脚本运行的事件


# 后台线程监听键盘
def listen_keyboard():
    def on_press(key):
        try:
            if key == keyboard.Key.esc:  # 按下 Esc 键停止脚本
                print("Esc 键被按下，停止脚本运行")
                stop_script.set()
        except Exception as e:
            print(f"键盘监听错误: {e}")

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


# 配置静态文件的根路径
@app.route('/')
@app.route('/<path:path>')
def serve_static(path='index.html'):
    return send_from_directory(app.static_folder, path)


@app.route('/api/mouse_position', methods=['GET'])
def get_mouse_position():
    # 获取当前鼠标的坐标
    x, y = pyautogui.position()

    return jsonify({"status": "success", "data": {"x": x, "y": y}})

@app.route('/api/run_start', methods=['POST'])
def run_start():
    body = request.get_json()

    # 验证 body 格式
    if not isinstance(body, dict) or 'data' not in body or 'speed' not in body:
        return jsonify({"status": "error", "message": "Invalid body format. Expected 'speed' and 'data' fields."}), 400

    speed = body.get('speed', 1.0)
    data = body.get('data')
    loop_count = body.get('loop_count', 1)  # 新增循环次数参数，默认值为1

    if not isinstance(data, list):
        return jsonify({"status": "error", "message": "Invalid 'data' format, expected a list."}), 400

    if speed < 0.2 or speed > 5.0:
        return jsonify({"status": "error", "message": "Speed must be between 0.2 and 5.0."}), 400

    if not isinstance(loop_count, int) or loop_count < -1:
        return jsonify({"status": "error", "message": "Loop count must be an integer >= -1."}), 400

    # 调整速度的因子：速度越大，操作时间越短
    speed_factor = 1 / speed

    stop_script.clear()  # 重置停止事件
    current_loop = 0  # 当前执行的循环次数

    while loop_count == -1 or current_loop < loop_count:
        current_loop += 1
        for action in data:
            if stop_script.is_set():  # 检查是否需要停止
                return jsonify({"status": "stopped", "message": "Script was stopped."})

            action_type = action.get('type')

            if action_type == 'moveTo':
                x = action.get('x', 0)
                y = action.get('y', 0)
                pyautogui.moveTo(x, y, duration=0.15 * speed_factor)

            elif action_type == 'delay':
                delay_time = action.get('time', 0) / 1000  # 转换为秒
                time.sleep(delay_time * speed_factor)

            elif action_type == 'click':
                key = action.get('key', 'left')
                # pyautogui.click(button=key)
                pydirectinput.mouseDown(button=key)
                time.sleep(0.005)
                pydirectinput.mouseUp(button=key)
                time.sleep(0.01)

            elif action_type == 'keyPress':
                key = action.get('key', None)
                if key:
                    pydirectinput.keyDown('a')  # 按下并释放键
                else:
                    return jsonify({"status": "error", "message": "Key is required for keyPress action."}), 400
                
            elif action_type == 'continuousMoveClick':
            # 获取参数
                x = action.get('x', 0)
                y = action.get('y', 0)
                spacing = action.get('spacing', 50)  # 间距，默认值为 50
                count = action.get('count', 7)  # 点击次数，默认值为 7

                for i in range(count):
                    if stop_script.is_set():  # 检查是否需要停止
                        return jsonify({"status": "stopped", "message": "Script was stopped."})

                    current_x = x + (spacing * i)
                    pyautogui.moveTo(current_x, y, duration=0.1 * speed_factor)
                    time.sleep(0.005)
                    pydirectinput.mouseDown(button='left')
                    time.sleep(0.005)
                    pydirectinput.mouseUp(button='left')
                    time.sleep(0.005)


            else:
                return jsonify({"status": "error", "message": f"Unknown action type: {action_type}"}), 400

    return jsonify({"status": "success", "message": f"Actions executed successfully {current_loop} time(s)."})


if __name__ == '__main__':
    # 启动键盘监听器线程
    keyboard_listener = threading.Thread(target=listen_keyboard, daemon=True)
    keyboard_listener.start()

    app.run(debug=True)
