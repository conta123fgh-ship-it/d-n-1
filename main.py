import os, datetime, urllib.request, json

k = os.environ.get("GEMINI_API_KEY", "").strip()
u = "https://generativelanguage." + "googleapis.com"

# Tự động tìm model Gemini mới nhất khả dụng với API key
req_list = urllib.request.Request(f"{u}/v1beta/models?key={k}")
with urllib.request.urlopen(req_list) as r:
    models = json.loads(r.read().decode("utf-8")).get("models", [])

valid = [
    m["name"] for m in models
    if "generateContent" in m.get("supportedGenerationMethods", [])
    and "flash" in m["name"]
]
model_name = sorted(valid)[-1] if valid else "models/gemini-2.5-flash"

url = f"{u}/v1beta/{model_name}:generateContent?key={k}"
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
    f.write(f"# Kết quả AI tự động ({today} UTC - {model_name})\n\n{ai_text}\n")
