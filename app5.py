import streamlit as st
import streamlit.components.v1 as components
import json
import random
import os

# ==========================================
# 1. 基础配置
# ==========================================
st.set_page_config(page_title="唐诗宋词大会", layout="wide", page_icon="📜")

# 隐藏 Streamlit 默认元素 & 样式
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stApp {background-color: #f0f2f6;} 
        div[data-testid="stToolbar"] {display: none;}
        
        .login-container {
            text-align: center; padding: 50px; background: white;
            border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            max-width: 500px; margin: 100px auto;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 用户登录逻辑
# ==========================================
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

if not st.session_state.current_user:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.title("📜 青庭诗词大会")
        st.info("请留下大侠尊姓大名，即可开启挑战。")
        user_input = st.text_input("大侠尊姓大名：", placeholder="李太白")
        if st.button("开始挑战", type="primary", use_container_width=True):
            if user_input.strip():
                st.session_state.current_user = user_input
                st.rerun()
            else:
                st.error("请务必输入名字！")
    st.stop()

current_user_name = st.session_state.current_user

# ==========================================
# 3. 数据准备 (读取真实 JSON 文件)
# ==========================================
data_file = 'app_data.json'
poets_data = []

if not os.path.exists(data_file):
    # 简单的 fallback 数据，防止没有文件时报错
    poets_data = [
        {"名字": "测试诗", "作者": "系统", "朝代": "唐", "content_1": "请先上传app_data.json", "content_2": "才能看到真实数据", "content_3": "床前明月光", "content_4": "疑是地上霜", "备注": ""}
    ] * 10
    st.toast("⚠️ 提示：使用测试数据中，请上传 app_data.json", icon="⚠️")
else:
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            poets_data = json.load(f)
        if len(poets_data) > 1000:
            poets_data = random.sample(poets_data, 1000)
    except Exception as e:
        st.error(f"数据读取失败: {e}")
        st.stop()

poets_json = json.dumps(poets_data, ensure_ascii=False)

# ==========================================
# 4. 前端代码块 (CSS 紧凑优化版)
# ==========================================
html_code = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>唐诗宋词挑战</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=Noto+Serif+SC:wght@400;700&display=swap');
        :root {{ --ink-black: #2c2c2c; --paper-bg: #fdfbf7; --accent-red: #b22c2c; --accent-green: #2e7d32; }}
        * {{ box-sizing: border-box; user-select: none; -webkit-tap-highlight-color: transparent; }}
        body {{
            margin: 0; padding: 0; background-color: #e6e6e6;
            background-image: url('https://www.transparenttextures.com/patterns/rice-paper-2.png');
            font-family: 'Noto Serif SC', serif;
            display: flex; justify-content: center; align-items: center;
            min-height: 100vh; color: var(--ink-black); overflow: hidden;
        }}
        
        /* === 调整 1: 容器高度改为 92vh，留出一点余地 === */
        .app-container {{
            width: 100%; max-width: 600px; height: 92vh; background: var(--paper-bg);
            border-radius: 12px; box-shadow: 0 0 20px rgba(0,0,0,0.2);
            display: flex; flex-direction: column; position: relative; border: 2px solid #d4d4d4;
        }}
        
        /* === 调整 2: 状态栏 Padding 减小 === */
        .status-bar {{ padding: 10px 15px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #ddd; background: rgba(255,255,255,0.8); font-weight: bold; font-size: 0.95rem; }}
        .player-info {{ font-family: 'Ma Shan Zheng', cursive; color: #555; }}
        
        /* === 调整 3: 游戏区域 Padding 减小 === */
        .game-area {{ flex: 1; display: flex; flex-direction: column; align-items: center; padding: 10px 15px; overflow-y: auto; justify-content: center; }}
        
        /* === 调整 4: 卡片高度从 220px -> 170px，Margin 减小 === */
        .card-container {{ width: 100%; height: 170px; perspective: 1000px; margin-bottom: 15px; cursor: pointer; flex-shrink: 0; }}
        .card {{ width: 100%; height: 100%; position: relative; transform-style: preserve-3d; transition: transform 0.8s; box-shadow: 0 8px 20px rgba(0,0,0,0.12); border-radius: 10px; }}
        .card.flipped {{ transform: rotateY(180deg); }}
        .card-face {{
            position: absolute; width: 100%; height: 100%; backface-visibility: hidden;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            border: 2px solid #333; background-color: #fffaf0; padding: 15px; text-align: center; border-radius: 10px;
        }}
        
        /* === 调整 5: 卡片字体调小 1.8rem -> 1.5rem === */
        .card-front {{ font-family: 'Ma Shan Zheng', cursive; font-size: 1.5rem; line-height: 1.3; }} 
        .card-back {{ transform: rotateY(180deg); background-color: #333; color: #fdfbf7; }}
        .card-back h2 {{ margin: 5px 0; font-size: 1.4rem; }}
        .card-back p {{ margin: 2px 0; font-size: 1rem; }}
        
        /* === 调整 6: 选项 Grid 间距从 15px -> 8px === */
        .options-grid {{ width: 100%; display: grid; gap: 8px; flex-shrink: 0; }}
        
        /* === 调整 7: 选项按钮 Padding 15px -> 12px，字体 1.1rem -> 1.0rem === */
        .option-btn {{
            background: white; border: 1px solid #888; padding: 12px; border-radius: 8px;
            font-size: 1.0rem; cursor: pointer; display: flex; align-items: center;
            min-height: 48px; /* 保证触控区域 */
        }}
        .option-tag {{ width: 22px; height: 22px; border-radius: 50%; background: #333; color: white; text-align: center; margin-right: 10px; flex-shrink: 0; line-height: 22px; font-size: 0.8rem; }}
        .option-btn.correct {{ background: #e8f5e9; border-color: var(--accent-green); color: var(--accent-green); }}
        .option-btn.wrong {{ background: #ffebee; border-color: var(--accent-red); color: var(--accent-red); }}
        
        .control-bar {{ padding: 10px 15px; background: #f4f4f4; display: flex; justify-content: space-around; border-top: 1px solid #ccc; }}
        .ctrl-btn {{ padding: 8px 18px; background: var(--ink-black); color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 0.95rem; }}
        .ctrl-btn:disabled {{ opacity: 0.5; }}
        .ctrl-btn.review {{ background: var(--accent-red); }}

        /* 模态框样式维持原样 */
        .modal {{ display: none; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); z-index: 100; justify-content: center; align-items: center; padding: 20px; }}
        .modal-content {{ background: var(--paper-bg); padding: 25px; border-radius: 10px; width: 100%; max-height: 85vh; overflow-y: auto; text-align: center; border: 4px double var(--ink-black); }}
        .result-table {{ margin: 10px auto; width: 100%; border-collapse: collapse; font-size: 0.9rem; }}
        .result-table td {{ padding: 6px; border-bottom: 1px solid #ccc; text-align: left; }}
        .result-key {{ font-weight: bold; width: 35%; color: #666; }}
        .result-val {{ font-weight: bold; color: var(--ink-black); }}
        .review-item {{ border-bottom: 1px dashed #ccc; padding: 8px 0; text-align: left; font-size: 0.9rem; }}
        .review-wrong {{ color: var(--accent-red); text-decoration: line-through; }}
        .review-right {{ color: var(--accent-green); }}
    </style>
</head>
<body>

<div class="app-container">
    <div class="status-bar">
        <div class="player-info">👤 {current_user_name}</div>
        <div>得分: <span id="score" style="color:var(--accent-red)">0</span> / <span id="total-q">30</span></div>
    </div>
    <div style="text-align:center; background:#eee; font-size:0.75rem; padding: 2px;" id="timer">00:00</div>

    <div class="game-area">
        <!-- 卡片区域 -->
        <div class="card-container" onclick="flipCard()">
            <div class="card" id="card">
                <div class="card-face card-front">
                    <div id="question-text">加载中...</div>
                    <div style="font-size:0.75rem; color:#666; margin-top:8px;" id="question-type-hint"></div>
                </div>
                <div class="card-face card-back">
                    <h2 id="meta-title"></h2>
                    <p id="meta-author"></p>
                    <p id="meta-dynasty"></p>
                </div>
            </div>
        </div>
        <!-- 选项区域 -->
        <div class="options-grid" id="options-container"></div>
    </div>

    <div class="control-bar">
        <button class="ctrl-btn" onclick="prevQuestion()" id="btn-prev" disabled>上一题</button>
        <button class="ctrl-btn review" onclick="finishGame()">交卷 / 复盘</button>
        <button class="ctrl-btn" onclick="nextQuestion()" id="btn-next">下一题</button>
    </div>

    <!-- 模态框 -->
    <div class="modal" id="review-modal">
        <div class="modal-content">
            <h2 style="font-family:'Ma Shan Zheng'; margin: 5px 0 15px 0;">📜 金榜题名</h2>
            <table class="result-table">
                <tr><td class="result-key">选手姓名:</td><td class="result-val">{current_user_name}</td></tr>
                <tr><td class="result-key">网络 IP:</td><td class="result-val" id="result-ip">获取中...</td></tr>
                <tr><td class="result-key">通关时间:</td><td class="result-val" id="end-time"></td></tr>
                <tr><td class="result-key">最终得分:</td><td class="result-val" id="final-score" style="color:var(--accent-red); font-size:1.2em;"></td></tr>
                <tr><td class="result-key">答题耗时:</td><td class="result-val" id="final-time"></td></tr>
            </table>
            <hr style="margin: 10px 0;">
            <h3 style="margin: 5px 0;">错题复盘</h3>
            <div id="review-list"></div>
            <br>
            <div style="display:flex; justify-content: space-around;">
                <button class="ctrl-btn" onclick="location.reload()">再来一局</button>
                <button class="ctrl-btn" onclick="closeModal()">关闭</button>
            </div>
        </div>
    </div>
</div>

<script>
    const poetsDB = {poets_json};
    const MAX_QUESTIONS = 30;
    const MAX_LINES = 20; 
    let clientIP = "未知";

    let gameState = {{
        questions: [], currentIndex: 0, score: 0, 
        startTime: null, timerInterval: null, isFinished: false
    }};

    function fetchClientIP() {{
        fetch('https://api.ipify.org?format=json')
            .then(res => res.json())
            .then(data => clientIP = data.ip)
            .catch(e => clientIP = "获取失败");
    }}

    function initGame() {{
        generateQuestions();
        gameState.startTime = Date.now();
        gameState.timerInterval = setInterval(updateTimer, 1000);
        renderQuestion();
        updateStats();
        fetchClientIP();
    }}

    function getPoemLines(poem) {{
        let lines = [];
        for(let i=1; i<=MAX_LINES; i++) {{
            let c = poem[`content_${{i}}`];
            if(c && c.trim()) lines.push(c);
        }}
        return lines;
    }}

    function generateQuestions() {{
        let qCount = 0, safety = 0;
        while(qCount < MAX_QUESTIONS && safety < 3000) {{
            safety++;
            let pIdx = Math.floor(Math.random() * poetsDB.length);
            let lines = getPoemLines(poetsDB[pIdx]);
            if(lines.length < 2) continue;
            
            let lIdx = Math.floor(Math.random() * lines.length);
            let qStr = lines[lIdx];
            
            let type = -1;
            if (lIdx === 0) type = 1;
            else if (lIdx === lines.length - 1) type = 0;
            else type = Math.random() > 0.5 ? 1 : 0;
            
            let aStr = (type === 0) ? lines[lIdx - 1] : lines[lIdx + 1];
            let hint = (type === 0) ? "选上一句" : "选下一句";
            
            let dists = [];
            let sd = 0;
            while(dists.length < 3 && sd < 100) {{
                sd++;
                let rp = poetsDB[Math.floor(Math.random()*poetsDB.length)];
                let rLine = getPoemLines(rp)[0];
                if(rLine !== aStr && rLine !== qStr && !dists.includes(rLine)) dists.push(rLine);
            }}
            
            gameState.questions.push({{
                id: qCount, poemIndex: pIdx, qStr, aStr, hint, 
                options: [...dists, aStr].sort(()=>Math.random()-0.5), 
                userAnswer: null, isCorrect: false
            }});
            qCount++;
        }}
    }}

    function renderQuestion() {{
        let q = gameState.questions[gameState.currentIndex];
        let p = poetsDB[q.poemIndex];
        document.getElementById('question-text').innerText = q.qStr;
        document.getElementById('question-type-hint').innerHTML = q.hint;
        document.getElementById('meta-title').innerText = p["名字"];
        document.getElementById('meta-author').innerText = p["作者"];
        document.getElementById('meta-dynasty').innerText = p["朝代"];
        document.getElementById('card').classList.remove('flipped');
        
        let c = document.getElementById('options-container');
        c.innerHTML = "";
        let abc = ['A','B','C','D'];
        q.options.forEach((opt, i) => {{
            let btn = document.createElement('div');
            btn.className = 'option-btn';
            btn.innerHTML = `<span class="option-tag">${{abc[i]}}</span> ${{opt}}`;
            if(q.userAnswer !== null) {{
                if(opt === q.aStr) btn.classList.add('correct');
                else if(opt === q.userAnswer) btn.classList.add('wrong');
                btn.style.pointerEvents = 'none';
            }} else {{
                btn.onclick = () => handleAnswer(opt, btn);
            }}
            c.appendChild(btn);
        }});
        
        document.getElementById('btn-prev').disabled = (gameState.currentIndex === 0);
        document.getElementById('btn-next').innerText = (gameState.currentIndex === MAX_QUESTIONS - 1) ? "交卷" : "下一题";
        updateStats();
    }}

    function handleAnswer(opt, btn) {{
        if(gameState.isFinished) return;
        let q = gameState.questions[gameState.currentIndex];
        q.userAnswer = opt;
        q.isCorrect = (opt === q.aStr);
        if(q.isCorrect) {{
            gameState.score++;
            btn.classList.add('correct');
        }} else {{
            btn.classList.add('wrong');
            if(navigator.vibrate) navigator.vibrate(200);
            document.querySelectorAll('.option-btn').forEach(b => {{
                if(b.innerHTML.includes(q.aStr)) b.classList.add('correct');
            }});
        }}
        updateStats();
        document.querySelectorAll('.option-btn').forEach(b => b.style.pointerEvents = 'none');
        setTimeout(() => {{
            if(gameState.currentIndex < MAX_QUESTIONS - 1) {{
                gameState.currentIndex++;
                renderQuestion();
            }} else finishGame();
        }}, 800);
    }}

    function updateStats() {{
        document.getElementById('score').innerText = gameState.score;
        document.getElementById('total-q').innerText = MAX_QUESTIONS;
    }}
    
    function updateTimer() {{
        if(gameState.isFinished) return;
        let d = Math.floor((Date.now() - gameState.startTime)/1000);
        let m = Math.floor(d/60).toString().padStart(2,'0');
        let s = (d%60).toString().padStart(2,'0');
        document.getElementById('timer').innerText = `${{m}}:${{s}}`;
    }}
    
    function flipCard() {{ document.getElementById('card').classList.toggle('flipped'); }}
    function prevQuestion() {{ if(gameState.currentIndex>0){{ gameState.currentIndex--; renderQuestion(); }} }}
    function nextQuestion() {{ if(gameState.currentIndex<MAX_QUESTIONS-1){{ gameState.currentIndex++; renderQuestion(); }} }}

    function finishGame() {{
        gameState.isFinished = true;
        clearInterval(gameState.timerInterval);
        
        let now = new Date();
        let y = now.getFullYear(), mo = String(now.getMonth()+1).padStart(2,'0'), d = String(now.getDate()).padStart(2,'0');
        let h = String(now.getHours()).padStart(2,'0'), mi = String(now.getMinutes()).padStart(2,'0'), s = String(now.getSeconds()).padStart(2,'0');
        document.getElementById('end-time').innerText = `${{y}}-${{mo}}-${{d}} ${{h}}:${{mi}}:${{s}}`;

        document.getElementById('final-score').innerText = gameState.score;
        document.getElementById('final-time').innerText = document.getElementById('timer').innerText;
        document.getElementById('result-ip').innerText = clientIP;
        
        let list = document.getElementById('review-list');
        list.innerHTML = "";
        let wrong = 0;
        gameState.questions.forEach((q, i) => {{
            if(!q.isCorrect) {{
                wrong++;
                let item = document.createElement('div');
                item.className = 'review-item';
                let uAns = q.userAnswer ? q.userAnswer : "未作答";
                item.innerHTML = `<div>${{i+1}}. ${{q.qStr}}</div><div style="font-size:0.9em">❌ <span class="review-wrong">${{uAns}}</span><br>✅ <span class="review-right">${{q.aStr}}</span></div>`;
                list.appendChild(item);
            }}
        }});
        if(wrong===0) list.innerHTML = "<p style='color:green'>🎉 全对！太棒了！</p>";
        
        document.getElementById('review-modal').style.display = 'flex';
    }}
    
    function closeModal() {{ document.getElementById('review-modal').style.display = 'none'; }}
    
    initGame();
</script>
</body>
</html>
"""

# 减小 iframe 高度，防止底部有大片空白
components.html(html_code, height=720, scrolling=False)