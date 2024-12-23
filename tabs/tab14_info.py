import gradio as gr
from openai import OpenAI
import os


# OpenAI API 客户端
baseURL = os.environ.get('OPEN_BASE_URL')
apiKEY = os.environ.get('OPEN_API_KEY')


client = OpenAI(
    api_key=apiKEY,
    base_url=baseURL
)


# 提示词模版
template = """
###
提示词1：
'''
{}
'''

提示词2：
'''
{}
'''
###

请将上面提供的多个提示词合并，要求对各个提示词进行分析，找出它们的核心要点和关键意图。然后，将这些核心元素以逻辑清晰、简洁明了的方式组合起来，去除重复冗余的部分，在合并过程中，要确保新的提示词能够准确涵盖原来多个提示词所期望的任务或结果，并且表达尽量精准，避免模糊不清或产生歧义
"""
# 功能: 合并优化提示词


def optimize_prompts(prompts1, prompts2):

    prompts = template.format(prompts1, prompts2)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个擅长提示词优化的助手。"},
                {"role": "user", "content": prompts}
            ]
        )
        # 提取三个优化后的提示词
        optimized_prompts = response.choices[0].message.content
        return optimized_prompts  # 返回前三个结果
    except Exception as e:
        return [f"优化失败: {str(e)}"]

# Gradio 界面



def func():
    with gr.Row():
        # 左侧输入框
        with gr.Column():
            prompts1 = gr.Textbox(
                label="提示词 1", placeholder="输入提示词 1", lines=5)
            prompts2 = gr.Textbox(
                label="提示词 2", placeholder="输入提示词 2", lines=5)
            optimize_button = gr.Button("合并并优化",variant="primary")

        # 右侧显示优化结果
        with gr.Column():
            optimized_prompt = gr.TextArea(
                label="优化结果", interactive=False)
   

        # 按钮点击时合并并优化提示词
        optimize_button.click(
            optimize_prompts,
            inputs=[prompts1, prompts2],
            outputs=[optimized_prompt]
        )

