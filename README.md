# インクメモ

スプラトゥーン3 の日報に書くための、スマホ用のメモ（PWA）。その日の次の 3 つだけを記録する。

- ウデマエポイント（マイナスも可。± ボタンか先頭に「-」）
- XP（小数 1 桁）
- ルールごとの勝敗（ナワバリ・エリア・ヤグラ・ホコ・アサリから選んで WIN / LOSE をタップ）

「日報用にコピー」で次の形の文がコピーされる。XP2500 ロードマップの日報に転記する。

```
【インクメモ 2026-11-09】
ウデマエ: 120pt
XP: 1650.4
エリア: 5勝3敗
ホコ: 1勝2敗
合計: 6勝5敗（55%）
```

## 仕様

- 記録はその端末のブラウザ（localStorage、キー `ink-memo-v1`）だけに保存する。サーバーには送らない。
- 朝 4 時までは前の日として記録する（`DAY_START_HOUR`）。
- 「全データをコピー」で JSON をクリップボードに出せる（機種変更や消去に備えたバックアップ）。
- オフラインでも開ける（`sw.js`）。画面はネット優先で取り直すので、更新は次に開いたときに反映される。

## ファイル

| ファイル | 内容 |
| --- | --- |
| `index.html` | 画面・スタイル・処理のすべて |
| `manifest.webmanifest`, `sw.js` | PWA の設定と Service Worker |
| `icons/` | アイコン。`python tools/make_icons.py` で作り直せる（Pillow が必要） |
| `.github/workflows/deploy.yml` | main への push で GitHub Pages に公開 |

## 手元で確かめる

```bash
python -m http.server 8765 --directory .
```

http://localhost:8765/ を開く。Service Worker は `file://` では動かない。
