from transformers import AutoTokenizer
from bigdl.llm.transformers import AutoModel
from streamlit.components.v1 import html
import streamlit as st
import pandas as pd
import numpy as np
import torch

# 创建Streamlit应用
st.set_page_config(
    page_title="YCEE-定制你的旅游攻略",
    page_icon=":robot:"
)

# 初始化模型和tokenizer
@st.cache_resource
def get_model():
    model_path = "THUDM/chatglm2-6b"
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModel.from_pretrained(model_path, load_in_4bit=True, trust_remote_code=True)
    model = model.eval()
    return tokenizer, model

tokenizer, model = get_model()
st.markdown(
    """
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-uf99v8.e1g8pov65 > div.block-container.css-1y4p8pa.e1g8pov64 {
        font-size: 20px;
        text-align: center;
        font-family: '得意黑', serif;
        color: orange;
    }
    #ycee > div > span {
        font-size: 60px;
        color: #9c3400;
        font-family: Times New Roman; /* 设置文本的字体 */
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-uf99v8.e1g8pov65 > div.block-container.css-1y4p8pa.e1g8pov64 > div:nth-child(1) > div > div:nth-child(4) > div > div > p {
        font-size: 30px;
        color: orange;
        font-family: '得意黑'; /* 设置文本的字体 */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit组件
st.title("YCEE")
st.write("🛫在线定制属于你的旅游攻略")
df = pd.DataFrame(
    columns=['lat', 'lon']
)
st.map(df)
max_length = st.sidebar.slider(
    'max_length', 0, 32768, 8192, step=1
)
top_p = st.sidebar.slider(
    'top_p', 0.0, 1.0, 0.8, step=0.01
)
temperature = st.sidebar.slider(
    'temperature', 0.0, 1.0, 0.8, step=0.01
)
if 'history' not in st.session_state:
    st.session_state.history = []

# if 'past_key_values' not in st.session_state:
#     st.session_state.past_key_values = None

for i, (query, response) in enumerate(st.session_state.history):
    with st.chat_message(name="user", avatar="user"):
        st.markdown(query)
    with st.chat_message(name="assistant", avatar="assistant"):
        st.markdown(response)
with st.chat_message(name="user", avatar="user"):
    input_placeholder = st.empty()
with st.chat_message(name="assistant", avatar="assistant"):
    message_placeholder = st.empty()



# 定义prompt
prompt = """生成任务：将用户输入的旅游偏好生成旅游路线信息。

下面是一些范例:

大美新疆，五天简游，好看好吃好留恋。2023-10-02 出发,共1天，享受美食！  ->    城市：阜康>博乐>伊犁>乌鲁木齐  途经：天山天池>赛里木湖>那拉提草原  人均2400元
不辜负每一个夏天～10日自驾游  四川雅安➡️海南。2023-05-01 出发,共10天,闺蜜,穷游,美食，五一      ->    城市：陵水>三亚   途经：陵水阿罗哈别墅(清水湾大道8号)>呆呆岛>后海村>秦韵餐厅·三亚红树林度假世界   人均4000元
去长春，度一个25°的清爽夏日。2023-06-01 出发,共1天，美食，夏季      ->    城市：长春   途经：伪满皇宫博物院>一汽红旗文化展馆>长春水文化生态园>长影旧址博物馆>长春电影制片厂
【上海】松江︱魔都之根，云间风情，带来怎样的惊喜。2023-05-08 出发,共4天,独自一人,深度游      ->    城市：上海      途经：七宝老街>醉白池>曲水园>秋霞圃>豫园>古猗园>仓城历史文化风貌区>松江布展示馆    人均1280元

请对下述要求生成旅游路线信息：

xxxxxx ->
"""

user_input = st.text_area(label="用户命令输入", 
                          height=100, 
                          placeholder=prompt)

if st.button("生成旅游路线信息"):
    input_placeholder.markdown(user_input)
    history= st.session_state.history
    question = prompt.replace('xxxxxx', user_input)
    responses = []

    with torch.inference_mode():
        for response, history in model.stream_chat(tokenizer, question, history=[]):
            # responses.append(response)
            message_placeholder.markdown(response)

    # for response in responses:
    #     st.write(response)
    st.session_state.history = history
