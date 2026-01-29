import json
from pathlib import Path
from copy import deepcopy

def load(p: Path):
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)

def save(p: Path, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def dict_diff(base, cur):
    """
    返回一个 overlay（dict）：只包含 cur 相对 base 的新增/变更键。
    - 若 base 没有该键：视为新增
    - 若值不同：视为变更（若是 dict 则递归）
    - 不处理删除（如需删除可扩展为 JSON Patch）
    """
    out = {}
    for k, v in cur.items():
        if k not in base:
            out[k] = deepcopy(v)
        else:
            bv = base[k]
            if isinstance(bv, dict) and isinstance(v, dict):
                sub = dict_diff(bv, v)
                if sub:
                    out[k] = sub
            else:
                if bv != v:
                    out[k] = deepcopy(v)
    return out

def main():
    runtime = Path(__file__).resolve().parents[1]  # deploy/runtime

    # 你要管理的 defaults 文件名
    targets = [
        "MSPT IPH_None.json",
        "MSPT IPH_Single Owner.json",
        "MSPT IPH_LCOH Calculator.json",
    ]

    # “基准文件”放这里（只放一份干净版，不要改它）
    baseline_dir = runtime / "baseline_defaults"
    # 你的本地正在改的 defaults（SAM 运行直接读取的）
    working_dir = runtime / "defaults"
    # 输出 overlay
    overlay_dir = runtime / "patches" / "defaults"

    baseline_dir.mkdir(parents=True, exist_ok=True)
    overlay_dir.mkdir(parents=True, exist_ok=True)

    for name in targets:
        base_p = baseline_dir / name
        cur_p = working_dir / name
        out_p = overlay_dir / name.replace(".json", ".overlay.json")

        if not base_p.exists():
            print(f"[INIT] baseline not found, copy current as baseline: {base_p.name}")
            # 第一次：你需要把“官方干净版”放进 baseline_defaults
            # 这里先提示，不自动复制，避免你把已经改过的当 baseline
            print(f"       Please put an upstream/clean copy into: {base_p}")
            continue

        if not cur_p.exists():
            print(f"[SKIP] current not found: {cur_p}")
            continue

        base = load(base_p)
        cur = load(cur_p)
        overlay = dict_diff(base, cur)
        save(out_p, overlay)
        print(f"[OK] overlay generated: {out_p} (keys={len(overlay)})")

    print("\nDone.")

if __name__ == "__main__":
    main()
