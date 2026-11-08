# ソーシャルVR（VRChat・Resonite）へのアバター持ち込み

確認日: 2026-11-07。版・制限・料金は変わりやすいので、作業前に各文書の出典を見直す。
ここはキャラクター共通の方法だけを扱う。個別キャラクターの設定や判断は各制作リポジトリに置く。

## 読む順

| 文書 | 中身 |
|---|---|
| [vrm-to-both.md](vrm-to-both.md) | VRoid/VRM の体を VRChat と Resonite の両方で使う流れと、両対応で崩れやすい点 |
| [vrchat-unity.md](vrchat-unity.md) | VRChat 用に Unity でやる作業（VCC・SDK・シェーダー・性能ランク・アップロード・Quest/iOS） |
| [resonite.md](resonite.md) | Resonite への持ち込み（取り込み形式・リグ条件・Avatar Creator・保存・料金） |
| [facts.yaml](facts.yaml) | 上の文書で使った版・数値・制限を機械可読にまとめたもの（AI・スクリプトはここを先に読む） |

## 一番大事な違い（1行ずつ）

- **VRChat**: Unity（指定版 2022.3.22f1）と VRChat SDK で「ビルドしてアップロード」する。アップロードには Trust Rank「New User」以上が要る。作業は Windows。
- **Resonite**: アプリの中に 3D ファイル（glTF/GLB 推奨、FBX。VRM は 0.x を .glb に改名するか ResoPon VRM で変換）をドラッグして、アプリ内の Avatar Creator で着られる形にする。Unity は任意（Modular Avatar 経由の変換で使う）。Windows・Linux のみ。
- **両対応の基本**: 1つの「正本モデル」（VRM 0.x か Blender 原本）から、VRChat 用と Resonite 用を別々に書き出す。片方用に加工したデータをもう片方へ流用しない。

## 状態の区別

本資料は公開資料の確認であり、本リポジトリでの実機確認ではない。手順を実際に通したら、各制作リポジトリ側に「実機確認済み（日付・版）」として記録する。
