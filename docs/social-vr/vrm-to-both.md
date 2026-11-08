# VRoid/VRM の体を VRChat と Resonite の両方で使う

確認日: 2026-11-07。前提: 体・顔・髪・服は VRoid Studio で作り、小物だけ Blender で足す流れ。

## 全体の流れ

```
VRoid Studio ──VRM 0.0 で書き出し──▶ 正本 VRM（0.x）
                                       │
                 （小物を足すなら）Blender + VRM アドオン ──▶ 正本 VRM（0.x, 小物入り）
                                       │
           ┌───────────────────────────┴───────────────────────────┐
           ▼                                                       ▼
 【VRChat】Windows + Unity 2022.3.22f1                【Resonite】Windows/Linux のアプリ内
  VCC → VRM Converter for VRChat → lilToon             ResoPon VRM で変換 か .glb に改名してドラッグ
  → PhysBones/Viseme 確認 → Build & Test → Publish      → Avatar Creator → Inventory に保存
```

## 判断ポイント

| 決めること | 推奨 | 理由 | 出典 |
|---|---|---|---|
| VRoid の書き出し版 | **VRM 0.0** | VRM Converter for VRChat は 0.x 対応、Resonite の .glb 改名取り込みも 0.x のみ。VRM 1.0 は非対応アプリで使えない（VRoid 公式） | [VRoid notice v1.20.2](https://vroid.com/en/studio/notice/62qSFvhlfsQMgFY7xzqeIH)、[Avatar Importing Guide](https://wiki.resonite.com/Avatar_Importing_Guide) |
| 正本をどこに置くか | VRoid の `.vroid` ＋書き出した VRM（＋小物を足した Blender 原本） | Unity 側・Resonite 側の加工は書き出し先ごとの派生物。正本に戻さない | — |
| どちらを先にやるか | **Resonite を先に試す**と早い（Unity 不要・ランク待ち不要） | VRChat はアップロードに New User ランクが要る。待つ間に Resonite で見た目と骨を確認できる | [Trust 条件](https://help.vrchat.com/hc/en-us/articles/360062658813-Why-can-t-I-upload-avatars-or-worlds-yet) |
| Unity プロジェクトから Resonite も出すか | 小物や服を Modular Avatar で着せる段階になってから検討 | MA の Resonite 対応は実験機能で、トグル・メニューは未対応 | [MA Resonite support](https://modular-avatar.nadena.dev/docs/experimental-features/resonite-support) |

## 両対応で崩れやすい点

| 項目 | VRChat | Resonite | 対策 |
|---|---|---|---|
| シェーダー | lilToon 等が使える（PC）。Quest は Mobile 系のみ | 独自シェーダー不可。XiexeToon/PBS に置き換え | 「色はテクスチャに焼く」を基本にし、シェーダー頼みの表現（グラデ・リム・発光の凝った設定）を減らす |
| 揺れもの | PhysBones | DynamicBoneChain | VRM の SpringBone を両方の変換元にする。変換後に各アプリで強さを調整 |
| 口パク | Avatar Descriptor の Viseme（ブレンドシェイプ） | VisemeAnalyzer など | VRoid の口ブレンドシェイプ（あ・い・う・え・お）を消さない・名前を変えない |
| 表情切替・小物の出し入れ | Animator＋Expression Menu | ProtoFlux／Avatar Expression Editor | 両方で別々に作る前提。ブレンドシェイプとオブジェクトの分け方だけ共通にしておく |
| 小物の付け方 | 骨の子にする／Modular Avatar | 骨の子にする | Blender で**頭や手の骨の子**にして VRM に入れる。別骨を足すなら Resonite 用に `<NoIK>` を意識（髪・耳など揺れる骨） |
| 面数・容量 | PC Good=7万三角形、Quest は2万が上限 | 明確なランク制は無いが保存容量（無料 1 GB） | まず PC 向けで作り、Quest は別の軽量版 |
| 作業 OS | Windows のみ（Unity・アップロード） | Windows / Linux | Mac は VRoid・Blender 担当、Windows で両アプリ |

## Blender で小物を足すときの注意

- VRM アドオン（VRM Add-on for Blender）で読み込み・書き出しする。**アドオンの対応 Blender 版を先に確認**（版が合わないと書き出しできない）。
- 書き出しは VRM 0.x を選ぶ。人型の骨の名前・階層は変えない。
- 小物は新しいマテリアル1つ・テクスチャ1枚にまとめると、VRChat のマテリアル枠と Resonite の容量の両方に効く。
- Resonite に .glb で直接出す場合は Draco なし・メートル単位・必要なら Sparse Accessor を外す。

## 完了条件の例

- 同じ正本 VRM から両アプリに入り、鏡で視点・口パク・瞬き・揺れものが動く。
- どちらも「どのファイル（版・日付）から作ったか」を記録してある。
