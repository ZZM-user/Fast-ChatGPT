import gradio as gr


def talk_methods(message, history):
    if message.endswith("?"):
        return "Yes"
    else:
        return "Ask me anything!"


gr.ChatInterface(
    talk_methods,
    chatbot = gr.Chatbot(height = 300),
    textbox = gr.Textbox(placeholder = "此时此刻，请你说", container = False, scale = 7),
    title = "Fast Chat",
    description = "可能我会帮助你推荐一些你需要的书籍……",
    theme = "soft",
    examples = ["我喜欢看大主宰", "有天蚕土豆的作品吗？", "我想看都市一类的小说"],
    cache_examples = True,
    retry_btn = None,
    undo_btn = "撤回",
    clear_btn = "清空",
).launch()

if __name__ == '__main__':
    gr.load()
