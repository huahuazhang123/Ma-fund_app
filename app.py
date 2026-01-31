import streamlit as st
import requests
import time
import re
import json

# 页面配置
st.set_page_config(page_title="我的基金看板", page_icon="📈", layout="centered")

def get_fund_data(code):
    t = int(time.time() * 1000)
    url = f"http://fundgz.1234567.com.cn/js/{code}.js?rt={t}"
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=1)
        if res.status_code == 200:
            match = re.search(r'jsonpgz\((.*?)\);', res.text)
            if match:
                return json.loads(match.group(1))
    except:
        return None
    return None

st.title("📱 专属基金盯盘助手")
st.write(f"最后刷新: {time.strftime('%H:%M:%S')}")

# 侧边栏输入
with st.sidebar:
    st.header("⚙️ 基金管理")
    default_funds = "161725,005827,110011"
    user_input = st.text_area("输入代码(逗号隔开)", value=default_funds)

# 主界面显示
fund_codes = user_input.replace("，", ",").split(",")
if st.button('🔄 立即刷新', use_container_width=True):
    st.rerun()

for code in fund_codes:
    code = code.strip()
    if not code: continue
    data = get_fund_data(code)
    if data:
        name = data['name']
        gsz = data['gsz']
        rate = float(data['gszzl'])
        st.metric(label=f"{name} ({code})", value=gsz, delta=f"{rate}%")
        st.divider()
    else:
        st.warning(f"代码 {code} 无法获取")
