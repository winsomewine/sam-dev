import json, glob, os

DEFAULTS_DIR = r"D:\dev\sam_dev\SAM\deploy\runtime\defaults"
for fp in glob.glob(os.path.join(DEFAULTS_DIR, "MSPT IPH_None.json")):
    with open(fp, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "yh_dni_scale" in data and isinstance(data["yh_dni_scale"], str):
        try:
            data["yh_dni_scale"] = float(data["yh_dni_scale"])
        except:
            data["yh_dni_scale"] = 1.0

    if "yh_met_preprocess_enable" in data and isinstance(data["yh_met_preprocess_enable"], str):
        data["yh_met_preprocess_enable"] = float(data["yh_met_preprocess_enable"])

    with open(fp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("fixed:", os.path.basename(fp))
