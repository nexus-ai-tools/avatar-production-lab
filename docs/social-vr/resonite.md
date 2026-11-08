# Resonite への持ち込み

確認日: 2026-11-07。数値は [facts.yaml](facts.yaml) にもまとめた。

## 前提条件

| 項目 | 内容 | 出典 |
|---|---|---|
| OS | Windows と Linux（Steam 配布）。**macOS は無い**。Linux は Windows より一部機能が欠ける | [Installing Resonite（2026-04-06 編集）](https://wiki.resonite.com/Installing_Resonite) |
| 料金 | 個人利用は無料（直近12か月の売上 10万USD 未満）。クラウド保存 1 GB。保存を増やすのは有料（Patreon/公式の支援プラン） | [Plans and Pricing](https://resonite.com/licensing) |
| アップロード権 | VRChat のような Trust Rank は無い。ログインして、Builder 権限のあるワールド（自分の Cloud Home など）で作業する | [Avatar creation tutorial](https://wiki.resonite.com/Tutorial:Avatar_creation) |
| Unity | **不要**。アプリ内で取り込み・設定まで完結する。Unity は変換経路の1つとして任意 | [Guide for VRChat users](https://wiki.resonite.com/Guide_for_VRChat_users) |

配信や VTuber 活動に個人無料プランを使ってよいかは、料金ページに明記なし（未確認。収益が出るなら Yellow Dog Man に確認）。

## 持ち込み経路（3つ）

| 経路 | 向いている場合 | 引き継がれるもの | 出典 |
|---|---|---|---|
| A. **ファイルを直接ドラッグ**（glTF/GLB 推奨、FBX、.blend、VRM 0.x を .glb に改名） | VRoid/Blender から直接。Unity を使わない | メッシュ・骨・ブレンドシェイプ・テクスチャ。揺れもの・表情操作はアプリ内で付け直す | [Avatar Importing Guide（2026-07-22 編集）](https://wiki.resonite.com/Avatar_Importing_Guide) |
| B. **ResoPon VRM**（VRM → ResonitePackage 変換、Windows 用コミュニティツール） | VRM をそのまま楽に入れたい | マテリアル・揺れもの（DynamicBone）・視点・拡縮・ツール位置まで変換 | [ResoPon VRM（2026-07-16 編集）](https://wiki.resonite.com/ResoPon_VRM) |
| C. **Unity から Modular Avatar - Resonite support**（実験機能） | VRChat 用 Unity プロジェクトが既にある | 視点、ブレンドシェイプの口パク、PhysBones→DynamicBone（設定の多くは引き継がない）。トグル・メニュー・Constraint は未対応 | [MA Resonite support](https://modular-avatar.nadena.dev/docs/experimental-features/resonite-support) |

使わない方がよいもの:
- **ResoniteImportHelper**: 2026-01-01 にアーカイブ（凍結）。作者は経路 C を推奨。出典: [GitHub](https://github.com/KisaragiEffective/ResoniteImportHelper)
- **Resonite UnitySDK**（Yellow-Dog-Man 製、v0.0.8 時点の記事）: PhysBones・トグル・アニメーション・Poiyomi 等は移らない。wiki 側も手順が作りかけ。出典: [Tutorial:UnitySDK（2026-06-29 編集）](https://wiki.resonite.com/Tutorial:UnitySDK)

## 経路 A の手順（直接ドラッグ）

1. Blender などで書き出す。**メートル単位**、**Draco 圧縮なし**。ブレンドシェイプでエラーが出たら Blender の glTF 書き出しで「Use Sparse Accessor if Better」を外す。
2. テクスチャは 2048px 程度に縮めてから（保存容量を食うため）。webp か png。
3. 自分の Cloud Home など Builder 権限のあるワールドに入る（Local Home は不可）。
4. ファイルをウィンドウにドラッグ → 「3D Model」→「Regular / Avatar」→ 必要なら Auto Humanoid Height。材質は PBS（Prefer Specular）推奨、トゥーン調なら **XiexeToon** が lilToon/Poiyomi に一番近い。
5. **取り込んだ直後にモデルを掴まない**（T/A ポーズの対称性が崩れ手の位置合わせが狂う。掴んだら Undo か再取り込み）。
6. Dash メニュー → Home → **Avatar Creator** を出し、ヘッドセット模型を頭に合わせる（Align Head Forward/Up/Right → Center Head Position → Try Align Hands）。
7. 必要なら Setup Volume Meter、Setup Face Tracking、**Protect Avatar**（他人が着る・保存するのを防ぐ）を選ぶ。
8. **Create → すぐ Inventory に保存** → 着る。保存前に別アバターを着ると未保存の変更が消える。
9. 揺れもの（DynamicBoneChain）、口パク（VisemeAnalyzer / DirectVisemeDriver）、目（EyeManager）、表情（Avatar Expression Editor）、トグル（ProtoFlux）はアプリ内で足す。

出典: [Avatar Importing Guide](https://wiki.resonite.com/Avatar_Importing_Guide)、[Avatar creation tutorial（2026-09-28 編集）](https://wiki.resonite.com/Tutorial:Avatar_creation)、[Avatar Hub](https://wiki.resonite.com/Avatar_Hub)

## リグ（骨）の条件

| 項目 | 条件 |
|---|---|
| ポーズ・向き | T ポーズか A ポーズ、正面が +Z |
| 体幹 | Hips（上向き1本）→ Spine → Chest → Neck → Head。UpperChest は可（その場合 Spine は IK で無視） |
| 腕・脚 | 左右を L/R で区別（大小文字は無視）。Shoulder→UpperArm→LowerArm→Hand、UpperLeg→LowerLeg→Foot→Toes |
| 指 | 3本以上・各2〜4節・親指が分かること。名前は `index1.L` のように根元から番号 |
| 目・顎 | 目の骨は任意だが自動視線とアイトラッキングに必要。顎は任意（ブレンドシェイプが主流） |
| IK から外す | 骨名のどこかに `<NoIK>` を入れる（髪・服・ねじれ骨など） |

VRoid/VRM の人型骨は概ねこの条件を満たす（自動判定されやすい）。ただし本資料での実機確認ではない。
出典: [Humanoid Rig Requirements for IK（2026-04-21 編集）](https://wiki.resonite.com/Humanoid_Rig_Requirements_for_IK)

## VRChat との違いで迷いやすい点

- **シェーダーは持ち込めない**。Resonite 内蔵の材質（PBS、XiexeToon など）に置き換わる。見た目は Resonite で調整し直す前提。
- **アニメーター（表情・トグル）は移らない**。ProtoFlux とコンポーネントで作り直す。
- アバターは自分のインベントリに保存され、容量（無料 1 GB）を使う。
- Protect Avatar（SimpleAvatarProtection）は「完全ではない」と wiki 自身が書いている。

出典: [Guide for VRChat users（2026-05-21 編集）](https://wiki.resonite.com/Guide_for_VRChat_users)
