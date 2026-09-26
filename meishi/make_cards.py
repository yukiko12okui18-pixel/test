"""名刺を作るスクリプト。

使い方:
    python3 make_cards.py              # data.json の全員分を作る
    python3 make_cards.py data.json    # 別のデータファイルを指定する

output/ フォルダに「氏名.html」ができるので、ブラウザで開いて印刷(PDF保存)してください。
"""
import html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
TEMPLATE = HERE / "template.html"
OUTPUT = HERE / "output"


def fill(template: str, values: dict) -> str:
    def replace(m):
        key = m.group(1)
        # 「◯◯_class」は、値が空なら項目ごと隠すための仕組み
        if key.endswith("_class"):
            return "" if values.get(key[:-6]) else "empty"
        if key not in values:
            raise KeyError(f"データに「{key}」がありません")
        return html.escape(str(values[key]))

    return re.sub(r"\{\{(.+?)\}\}", replace, template)


def main():
    data_path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "data.json"
    data = json.loads(data_path.read_text(encoding="utf-8"))
    template = TEMPLATE.read_text(encoding="utf-8")
    OUTPUT.mkdir(exist_ok=True)

    for person in data["people"]:
        values = {**data["company"], **person}
        out = OUTPUT / f"{person['氏名'].replace(' ', '').replace('　', '')}.html"
        out.write_text(fill(template, values), encoding="utf-8")
        print(f"作成しました: {out}")


if __name__ == "__main__":
    main()
