#!/user/bin/env python3
#  -*- coding: utf-8 -*-
from pathlib import Path
from traceback import format_exc
from flask import jsonify, request, Flask

from deepseek import chat
from utils.logger import Log

os_file_name = Path(__file__).name

app = Flask(__name__)


@app.route("/chat/deepseek", methods=["POST"])
def chat_with_deepseek():
    try:
        # 获取参数
        request_params = request.get_json(force=True)
        question = request_params["question"]
        Log().info(os_file_name,  f"问题: {question}")
        # 反射获取方法
        try:
            # import module, func
            result = chat(question)
            think = result.split("</think>")[0]
            answer = result.split("</think>")[1]
        except (ModuleNotFoundError, AttributeError) as e:
            Log().info(os_file_name,  repr(e))
            return jsonify(result=1, resultNote=f"服务器繁忙……")
        # 返回执行结果
        return jsonify(result=0, resultNote="chat success", think=think, answer=answer)

    except Exception as e:
        Log().error(os_file_name,  repr(e))
        Log().error(os_file_name,  format_exc())
        return jsonify(result=2, resultNote="服务内部异常")


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False, port=8080)
