# VRChat 用に Unity でやる作業

確認日: 2026-11-07。数値は [facts.yaml](facts.yaml) にもまとめた。

## 前提条件

| 項目 | 内容 | 出典 |
|---|---|---|
| OS | VRChat PC版と Creator Companion（VCC）は Windows 前提。Mac から上げる非公式手段（ALCOM 等）はここでは扱わない | [VCC Getting Started](https://vcc.docs.vrchat.com/guides/getting-started/) |
| Unity | **2022.3.22f1 固定**（2025-10-03 更新）。Unity 6 にプロジェクトを上げると動かない（VRChat の警告、2026-09 時点。クライアントの Quest 版 beta は Unity 6 だが制作側は 2022 のまま。移行日は未発表） | [Current Unity Version](https://creators.vrchat.com/sdk/upgrade/current-unity-version/)、[MIXED 2026-09-23](https://mixed-news.com/en/vrchat-quest-open-beta-unity-6-creators-stay-unity-2022/) |
| Unity の利用料 | Unity Personal は無料。売上＋資金調達が年 20万USD まで | [Unity pricing updates](https://unity.com/en/products/pricing-updates) |
| VRChat SDK | 3.x 系。確認時点の最新は 3.10.6（3.10.3 は 2026-04-16）。VCC で入れると自動で更新管理される | [Release 3.10.3](https://creators.vrchat.com/releases/release-3-10-3) |
| アップロード権 | Trust Rank「New User」以上。それ前でも Build & Test（自分だけのローカル試験）は可 | [Why can't I upload…](https://help.vrchat.com/hc/en-us/articles/360062658813-Why-can-t-I-upload-avatars-or-worlds-yet) |

## 手順（VRM から始める場合）

1. **VCC を入れる** → VCC の案内で Unity Hub と Unity 2022.3.22f1 を入れる。Quest/iOS も出すなら、Unity Hub で Android Build Support と iOS Build Support のモジュールも入れる。
2. **Avatar プロジェクトを作る**（VCC の「Create New Project」→ Avatars）。
3. **変換ツールを VCC に足す**。VRM の版で選ぶ（下表）。
4. **シェーダーを入れる**（PC は lilToon が定番。VCC にリポジトリを足して入れる）。
5. **VRM を Unity に入れて変換** → 出来たアバターをシーンに置く。
6. **VRC Avatar Descriptor を確認**: View Position（目と目の間・やや前）、Lip Sync（Viseme Blend Shape）、Eye Look（瞬き・視線）。
7. **揺れもの**: VRM の SpringBone は PhysBones に変換される（変換ツールしだい）。足りない所は VRC PhysBone を手で足す。
8. **VRChat SDK > Show Control Panel > Builder** で警告を潰し、**Build & Test** で自分だけ試す。
9. New User になったら **Build & Publish**。初回で Blueprint ID が振られる。
10. 他機種（Android=Quest、iOS）用は、同じ Blueprint ID のまま build target を切り替えて別ビルドを上げる（後述）。

## VRM → VRChat 変換ツールの選び方

| ツール | 対象 VRM | 価格 | 状態（2026-11-07 確認） | 出典 |
|---|---|---|---|---|
| VRM Converter for VRChat（esperecyan） | **VRM 0.x**（VRM 1.0 の記載なし） | 無料（任意の支援 ¥1,000） | VCC にコミュニティリポジトリ `https://esperecyan.github.io/VRMConverterForVRChat/registry.json` を足して入れる | [BOOTH](https://pokemori.booth.pm/items/1025226) |
| VRM1.0 to VRChat Converter（fatdesign） | **VRoid Studio 書き出しの VRM 1.0** のみ。ツールで加工した VRM1 は非対応の可能性 | 無料 | v0.3045（2026-06-10）。開発停止・後継 VRM2VRC あり（後継の詳細は未確認） | [BOOTH](https://booth.pm/ja/items/8294490) |
| V2V: VRoid to VRChat | VRoid 由来 | BOOTH 参照 | 代替候補。版・対応は未確認 | [BOOTH](https://booth.pm/ja/items/4600425) |

迷ったら **VRoid から VRM 0.0 で書き出し → VRM Converter for VRChat**。Resonite でも VRM 0.x の方が通りやすいので、両対応では 0.x にそろえるのが安全（[vrm-to-both.md](vrm-to-both.md)）。

## シェーダー

| 用途 | 候補 | メモ |
|---|---|---|
| PC | lilToon（MIT・無料） | 日本の VRChat アバターの定番。VRM の MToon から変換するツールが多い | 
| PC | Poiyomi | 海外で定番。Resonite には持ち込めない（Resonite は独自シェーダー不可） |
| Quest / iOS | `VRChat/Mobile` 系のみ（Toon Standard、Toon Lit、Standard Lite など） | Toon Standard は SDK 3.10.3 で Color Mask が追加。lilToon・Poiyomi・MToon は使えない |

出典: [Quest Content Limitations](https://creators.vrchat.com/platforms/android/quest-content-limitations/)、[lilToon（BOOTH）](https://booth.pm/ja/items/3087170)、[Release 3.10.3](https://creators.vrchat.com/releases/release-3-10-3)

## 性能ランク（PC、2026-10-21 更新）

| 項目 | Excellent | Good | Medium | Poor |
|---|---|---|---|---|
| 三角形 | 32,000 | 70,000 | 70,000 | 70,000 |
| テクスチャメモリ | 40 MB | 75 MB | 110 MB | 150 MB |
| Skinned Mesh | 1 | 2 | 8 | 16 |
| マテリアル枠 | 4 | 8 | 16 | 32 |
| PhysBone 部品数 | 4 | 8 | 16 | 32 |
| PhysBone が動かす骨 | 16 | 64 | 128 | 256 |
| 骨 | 75 | 150 | 256 | 400 |

モバイル（Quest/iOS）は三角形 7,500/10,000/15,000/20,000、テクスチャ 10/18/25/40 MB、マテリアル 1/1/2/4 と桁違いに厳しい。全表は [facts.yaml](facts.yaml)。
出典: [Performance Ranks](https://creators.vrchat.com/avatars/avatar-performance-ranking-system/)

**サイズ上限**（2026-10-07 更新）: PC はダウンロード 200 MB／展開後 500 MB、Android は 10 MB／40 MB。iOS の値はページに無し（未確認）。出典: [Avatar Size Limits](https://creators.vrchat.com/avatars/avatar-size-limits)

VRoid 標準の書き出しは服・髪の作り次第で三角形・マテリアル数が多くなりがち。まず PC の Good〜Medium を目標にし、AAO Avatar Optimizer（MIT）のような非破壊最適化で減らす。

## 他機種（Quest/Android・iOS）

- 同じ Blueprint ID のまま、SDK の Builder で Platforms を Android/iOS に切り替えてビルドする。初回切替は再インポートで遅い。
- **頭・手・足など主要な骨の階層（パス）と、ルートの回転・拡縮を PC 版と同じにする**。補助の骨は削ってよい。
- iOS 版が無く Android 版がある場合、iOS で Android 版を読む試験的な代替がある。どちらも無い機種では **Impostor**（アップロード時に自動生成される軽量代役、人型のみ、1日10回まで再生成）が表示される。
- iOS ビルドに Mac が要るかは公式に記載なし（未確認）。

出典: [Cross-Platform Setup（2026-09-15 更新）](https://creators.vrchat.com/platforms/android/cross-platform-setup)、[Impostors（VRChat Wiki）](https://wiki.vrchat.com/wiki/Impostors)、[iOS Platform FAQ](https://help.vrchat.com/hc/en-us/articles/45880051153939-iOS-Platform-FAQ)

## よく使う追加ツール（すべて VCC から入る非破壊ツール）

| ツール | 役割 |
|---|---|
| Modular Avatar（NDMF） | 服・小物を「着せる」非破壊合成。Resonite 書き出し（実験機能）もある |
| AAO Avatar Optimizer | ビルド時にメッシュ統合・不要骨削除で性能ランクを上げる |

## 完了条件の例

- Builder の Error が 0、Warning は理由を説明できる。
- Build & Test で鏡を見て、視点・口パク・瞬き・揺れものが動く。
- 性能ランクを記録する（目標ランクと実測を並べる）。
