from flask import Flask, jsonify, request, render_template, send_from_directory
import pyautogui
import time

app = Flask(__name__)

# 配置静态文件的根路径
@app.route('/')
@app.route('/<path:path>')
def serve_static(path='index.html'):
    return send_from_directory(app.static_folder, path)

@app.route('/api/move_mouse', methods=['POST'])
def move_mouse():
    data = request.get_json()
    x = data.get('x', 0)
    y = data.get('y', 0)
    print(x, y)

    # 使用 pyautogui 移动鼠标
    pyautogui.moveTo(x, y, duration=0.3)
    1
    return jsonify({"status": "success", "message": f"Moved mouse to ({x}, {y})"})

@app.route('/api/mouse_position', methods=['GET'])
def get_mouse_position():
    # 获取当前鼠标的坐标
    x, y = pyautogui.position()

    return jsonify({"status": "success", "data": {"x": x, "y": y}})

@app.route('/api/run_start', methods=['POST'])
def run_start():
    data = request.get_json()
    if not isinstance(data, list):
        return jsonify({"status": "error", "message": "Invalid data format, expected a list."}), 400

    for action in data:
        action_type = action.get('type')

        if action_type == 'moveTo':
            x = action.get('x', 0)
            y = action.get('y', 0)
            pyautogui.moveTo(x, y, duration=0.3)

        elif action_type == 'delay':
            delay_time = action.get('time', 0) / 1000  # 转换为秒
            time.sleep(delay_time)

        elif action_type == 'click':
            key = action.get('key', 'left')
            pyautogui.click(button=key)

        else:
            return jsonify({"status": "error", "message": f"Unknown action type: {action_type}"}), 400

    return jsonify({"status": "success", "message": "Actions executed successfully."})

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
