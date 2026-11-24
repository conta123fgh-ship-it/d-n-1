import os, datetime, urllib.request, json

k = os.environ.get("GEMINI_API_KEY", "").strip()
u = "https://googleapis.com"generativelanguage.
p = "/v1beta/models/gemini-2.5-flash:generateContent"
url = f"{u}{p}?key={k}"

prompt = "Viết bản tin tóm tắt 3 mẹo lập trình hay hôm nay bằng tiếng Việt."

req = urllib.request.Request(
    url,
    data=json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

with urllib.request.urlopen(req) as res:
    result = json.loads(res.read().decode("utf-8"))
    ai_text = result["candidates"][0]["content"]["parts"][0]["text"]

today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
with open("ket-qua.md", "w", encoding="utf-8") as f:
    f.write(f"# Kết quả AI tự động ({today} UTC)\n\n{ai_text}\n")
