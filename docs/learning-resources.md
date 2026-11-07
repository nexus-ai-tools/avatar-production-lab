# 学習資料・参考資料の一覧

資料確認日: 2026-11-07。VRoid → VRM → Blender で小物追加 → VRChat という流れで、別のキャラクターにも使える資料を集めた。各項目は配布元のページを検索・取得して確認した範囲の情報で、インストールや実機での動作確認ではない。版・対応状況・ライセンスは利用前に配布元で再確認する。

無料ツールの詳しい選定は [無料ツール](free-tools.md)、論文・実制作から借りる考え方は [研究メモ](research-notes.md) を参照する。

## まず読む順番

1. Blender の操作は [公式マニュアル（日本語）](https://docs.blender.org/manual/ja/latest/) で引く。通読はしない。
2. 基本操作は [Blender Studio の Training](https://studio.blender.org/training/) の Fundamentals 系で一周する。一部講座は有料会員向け。
3. VRM の読み書きは [VRM Add-on for Blender のドキュメント](https://vrm-addon-for-blender.info/) を見る。
4. 小物を付ける具体手順は、下の「記事」の 2・3 を見る。

## 公式リファレンス

| 名前 | 用途 | 確認できたこと |
| --- | --- | --- |
| [Blender 公式マニュアル（日本語）](https://docs.blender.org/manual/ja/latest/) | 機能・操作の辞書 | CC-BY-SA 4.0 |
| [Blender Python API](https://docs.blender.org/api/current/) | bpy スクリプトの辞書 | 版ごとに API が変わる。使う Blender と同じ版を読む |
| [VRM Add-on for Blender](https://extensions.blender.org/add-ons/vrm/)（[ドキュメント](https://vrm-addon-for-blender.info/)） | VRM の読み込み・書き出し | 4.10.4（2026-11-04）。Blender 4.2 LTS 以降、**5.3 以降は非対応**と記載。GPL-3.0-or-later と MIT |
| [VRM 仕様・MToon](https://vrm.dev/) | VRM の材質（MToon）と仕様 | MToon 0系と1.0系でパラメータが違う。出力先に合わせて読む |
| [VRoid Studio](https://vroid.com/studio) | VRoid 本体・公式情報 | 無料。Mac / Windows 版あり |
| [VRChat Creator Companion](https://vcc.docs.vrchat.com/guides/getting-started/) | VRChat 用 Unity プロジェクトの作成 | GUI は Windows 向け。Mac は CLI の一部機能のみ |
| [VRChat Creators](https://creators.vrchat.com/sdk/) | VRChat SDK・アバターの公式ドキュメント | — |
| [Modular Avatar（日本語）](https://modular-avatar.nadena.dev/ja/) | Unity 上で衣装・小物を非破壊で着け外しする | MIT（`Editor/images` 配下の画像を除く） |

## 学習サイト・まとめ

| 名前 | 内容 | 注意 |
| --- | --- | --- |
| [Blender Studio Training](https://studio.blender.org/training/) | 公式の動画講座 | 一部有料 |
| [CGbox「Blenderチュートリアルまとめ」](https://cgbox.jp/2023/05/02/blender-tutrial-sum/) | YouTube 58本の紹介（モデリング・背景・アニメ・材質など） | 2023年の記事。VRoid / VRM は扱っていない |
| [Blender Guru](https://www.blenderguru.com/) | 定番の初心者向けシリーズ（ドーナツ）など | 英語 |

## 記事（日本語、VRoid / VRM / VRChat 向け）

作業の順番に並べた。どれも本文に価格表示はなく、全文を閲覧できた。

| 順 | 記事 | 分かること |
| --- | --- | --- |
| 1 | [VroidVRMをBlenderで編集 大初心者つまづきメモ](https://note.com/ebina_amane/n/n72859a37ede3)（2025-12） | VRoid 製 VRM を Blender で触る時のつまづき。ペアレント（Ctrl+P）の種類の違い、Lit Color でのテクスチャ差し替え |
| 2 | [BlenderでVRoidにアクセサリーを付ける方法まとめ](https://note.com/yamazaki_yuumi/n/n716668bfb319)（2024-05, Blender 4.0） | 小物を VRoid の骨に付けて VRM で書き出すまで。簡易版（ボーンのウェイト）と通常版（頂点グループ） |
| 3 | [頭のボーンに顔のパーツを親子付けする方法メモ](https://note.com/yanbo_jp/n/n36c607895eda)（2022-05） | 頭の骨への親子付けのクリック順 |
| 4 | [【初心者向け】VRoid＞VRCアバター変換講座2024 ②](https://note.com/gasoko0150/n/n5d67cd94453c)（2025-11 まで更新） | Unity での変換からアップロードまで |
| 5 | [0円から始めるVRC向けモデリング](https://note.com/natsukisan1218/n/n5b566acf9fc4)（2026-10） | 無料 Blender アドオン14個の紹介 |

曲がらない小物（耳・ヘッドホン・眼鏡など）は、ウェイトを塗らずに頭の骨へ親子付けするだけで済む場合が多い（記事2の簡易版）。揺れ物や服は記事1・4を参照する。

## 動画

説明欄と紹介記事の情報だけで選んだ。本編は視聴していない。古い Blender の操作画面と違う場合がある。

| 動画 | 使いどころ |
| --- | --- |
| [アウトラインとトゥーンシェーダー（artist.B）](https://www.youtube.com/watch?v=tHKhErp408s) | アニメ調の見た目を Blender 上で確認する |
| [SF系ヘルメット（Emiliano Colantoni）](https://youtu.be/tjNjAT7X9gU) | ヘッドホンのような硬い小物の作り方（タイムラプス） |
| [ブーリアンを使わない穴あけ（Arijan）](https://youtu.be/ZrQIq6pCtPE) | スピーカー穴・ネジ穴をきれいに開ける |
| [抽象的オブジェクト（U.K Creations）](https://youtu.be/J3w1T9fxtP4) | 始めたばかりの人向けの基本操作 |

顔・髪の考え方の動画（2AM）は [研究メモ](research-notes.md) にある。

## GitHub・アドオン

| 名前 | 用途 | ライセンス・注意 |
| --- | --- | --- |
| [VRM Add-on for Blender](https://github.com/saturday06/VRM-Addon-for-Blender) | VRM の読み書き | 上の「公式リファレンス」参照。Blender 5.3 以降は非対応と記載 |
| [Mio3 UV](https://github.com/mio3io/mio3_uv) | UV 編集の補助 | GPL-3.0。v2 系は Blender 5 以降、Blender 4 なら v1.5 |
| [Modular Avatar](https://github.com/bdunderscore/modular-avatar) | Unity 上での非破壊な衣装・小物の着け外し | MIT（画像を除く） |
| [lilToon](https://github.com/lilxyzw/lilToon) / [AAO Avatar Optimizer](https://github.com/anatawa12/AvatarOptimizer) | VRChat 向けの材質・最適化 | MIT。[無料ツール](free-tools.md) 参照 |
| [BlenderMCP（mcp-for-blender）](https://github.com/ahujasid/blender-mcp) | AI クライアントから Blender を操作する | MIT。2026-09 の v2.0.0 で `mcp-for-blender` に改名、`uvx blender-mcp` は互換で動くと PyPI に記載 |
| [Khronos glTF Sample Assets](https://github.com/KhronosGroup/glTF-Sample-Assets) | glTF の見本モデル | モデルごとにライセンスが違う。各モデルの README で確認する |

## 無料素材

| 名前 | 中身 | ライセンス |
| --- | --- | --- |
| [Poly Haven](https://polyhaven.com/) | モデル・HDRI・テクスチャ | CC0。API 利用時は配布元の利用条件を確認する |
| [ambientCG](https://ambientcg.com/) | PBR テクスチャ・HDRI | CC0 |
| [Kenney](https://kenney.nl/assets) | ローポリの小物キット | CC0 |
| [Quaternius](https://quaternius.com/) | ローポリのキャラ・小物パック | CC0 |
| [Smithsonian 3D](https://3d.si.edu/) | 博物館所蔵品のスキャン | CC0 表示の作品のみ。作品ごとに確認する |

BOOTH などで配布されるアバター用素材は、無料でも作品ごとに利用規約が違う。改変・VRChat アップロード・再配布の可否を個別に確認する。

## 自動取得や利用を保留するもの

| 名前 | 理由 |
| --- | --- |
| [Objaverse-XL](https://huggingface.co/datasets/allenai/objaverse-xl) | 約1,000万件。データセット全体は ODC-By 1.0 だが、オブジェクトごとにライセンスが違う（CC-BY、MIT、GPL、無記載など）。作品に使うなら1件ずつ確認が必要 |
| Khronos のサンプルの一部 | DamagedHelmet は元モデルに CC-BY-NC が含まれ、Duck は SCEA Shared Source License で、どちらも CC0 ではない |
