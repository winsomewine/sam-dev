import json
import glob
import os

RUNTIME = r"D:\dev\sam_dev\SAM\deploy\runtime"
DEFAULTS_DIR = os.path.join(RUNTIME, "defaults")

# 你新增的变量（注意 yh_dni_scale 是字符串，避免 TextEntry 类型冲突）
PATCH = {
    "yh_met_preprocess_enable": 0.0,
    "yh_dni_scale": "1.0"
}

# 只补到 MSPT IPH 的 defaults（你也可以把过滤条件改宽一点）
pattern = os.path.join(DEFAULTS_DIR, "MSPT IPH_*.json")
files = glob.glob(pattern)

if not files:
    raise SystemExit(f"没找到文件：{pattern}")

for fp in files:
    with open(fp, "r", encoding="utf-8") as f:
        data = json.load(f)

    changed = False
    for k, v in PATCH.items():
        if k not in data:
            data[k] = v
            changed = True

    if changed:
        # 备份
        bak = fp + ".bak"
        if not os.path.exists(bak):
            with open(bak, "w", encoding="utf-8") as f:
                json.dump(json.load(open(fp, "r", encoding="utf-8")), f, ensure_ascii=False, indent=2)

        with open(fp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[OK] patched: {os.path.basename(fp)}")
    else:
        print(f"[SKIP] already has keys: {os.path.basename(fp)}")

print("Done.")
