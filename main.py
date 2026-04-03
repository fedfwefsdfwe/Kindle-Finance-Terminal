from flask import Flask, make_response
import yfinance as yf
import datetime
import requests

app = Flask(__name__)

# ================= 配置区域 =================
# 请在此处修改你的地理坐标（可通过地图工具获取）
LAT = "32.29"   # 纬度示例
LON = "118.31"  # 经度示例
# ===========================================

def get_weather():
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current_weather=true"
        r = requests.get(url, timeout=5)
        data = r.json()['current_weather']
        return f"{data['temperature']}°C"
    except:
        return "N/A"

@app.route('/')
def dashboard():
    try:
        # 定义监控的指数符号 (Yahoo Finance 格式)
        market_data = {
            "China & HK": {
                "000001.SS": "上证指数",
                "399001.SZ": "深证成指",
                "^HSI": "恒生指数"
            },
            "US Indices": {
                "^DJI": "道琼斯",
                "^IXIC": "纳指100",
                "^GSPC": "标普500"
            },
            "Futures": {
                "YM=F": "道指期货",
                "NQ=F": "纳指期货",
                "ES=F": "标普期货"
            }
        }
        
        weather = get_weather()
        # 顶部标题栏
        res = f"<div style='border-bottom:2px solid black; padding-bottom:8px; margin-bottom:15px; height:55px; line-height:55px;'>"
        res += f"<span style='font-size:42px; font-weight:bold; float:left;'>Kindle Terminal</span>"
        res += f"<span style='font-size:28px; float:right; background:#000; color:#fff; padding:0 12px; margin-top:5px;'>{weather}</span>"
        res += f"<div style='clear:both;'></div></div>"

        # 数据展示区域
        res += f"<div style='text-align:center;'>"
        for section, items in market_data.items():
            res += f"<div style='background-color:#eee; padding:4px; font-size:20px; margin:12px auto 8px auto; width:90%;'><b>{section}</b></div>"
            for symbol, name in items.items():
                t = yf.Ticker(symbol)
                info = t.fast_info
                price, prev = info['last_price'], info['previous_close']
                change = ((price - prev) / prev) * 100 if prev else 0
                
                res += f"<div style='margin-bottom:6px; border-bottom:1px solid #f2f2f2; padding:5px 0; white-space:nowrap;'>"
                res += f"<span style='font-size:24px;'>{name}: </span>"
                res += f"<span style='font-size:26px;'><b>{price:.2f}</b></span> "
                res += f"<span style='font-size:20px;'>({change:+.2f}%)</span>"
                res += f"</div>"
        res += f"</div>"

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        res += f"<p style='text-align:center; font-size:14px; color:gray; margin-top:15px; border-top:1px solid #ccc; padding-top:8px;'>Updated: {now}</p>"
        
        # 核心：设置 300 秒（5分钟）自动刷新
        response = make_response(f"<html><head><meta charset='utf-8'><meta http-equiv='refresh' content='300'></head><body style='padding:15px; font-family:sans-serif; background-color:white;'>{res}</body></html>")
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return response
    except Exception as e:
        return f"<html><head><meta http-equiv='refresh' content='30'></head><body><h2>Syncing...</h2></body></html>"

if __name__ == '__main__':
    # 默认端口 3721
    app.run(host='0.0.0.0', port=3721)
