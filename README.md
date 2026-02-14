# Simple Blockchain - 学習用ブロックチェーン実装

## 概要

Pythonでブロックチェーンの基本構造を理解するための教育用プロジェクトです。
トランザクション、ブロック、ハッシュチェーン、改ざん検知の仕組みを実際のコードで学べます。

**対象者:** Pythonの基礎を理解している学習者  
**学習時間:** 実装 2-3時間、理解 1-2時間

## クイックスタート

```bash
# 1. プロジェクトのセットアップ
cd simple-blockchain

# 2. CLIの起動
python src/simple_blockchain/cli.py

# 3. 操作例
# [2] トランザクション作成
# [4] マイニング実行
# [5] チェーン表示
# [6] チェーン検証
# [7] ブロック改ざん（学習用）
# [6] 再検証 → 改ざんが検出される
```

## 学べること

- ✅ トランザクションの構造
- ✅ ブロックの連鎖構造（previous_hash）
- ✅ Proof of Work（簡易版）
- ✅ ハッシュによる改ざん検知
- ✅ ブロックチェーンの不変性

## プロジェクト構造

```
simple-blockchain/
├── README.md                      # このファイル
├── AGENTS.md                      # LLM実装者向けガイド
├── instructions/                  # 段階的実装指示
│   ├── 01-SETUP.md
│   ├── 02-PARTICIPANTS-TRANSACTION.md
│   ├── 03-BLOCK-MINER.md
│   ├── 04-BLOCKCHAIN.md
│   └── 05-CLI-INTEGRATION.md
├── src/
│   └── simple_blockchain/         # メインコード
│       ├── participants.py
│       ├── transaction.py
│       ├── block.py
│       ├── miner.py
│       ├── blockchain.py
│       └── cli.py
└── data/                          # データファイル
    ├── participants.json
    ├── transactions/
    └── blocks/
```

## 実装方法

### Agentic Coding で実装する場合

```bash
# Phase 1: セットアップ
# 指示: "Please follow the instructions in ./instructions/01-SETUP.md"

# Phase 2: 基本モジュール
# 指示: "Please follow the instructions in ./instructions/02-PARTICIPANTS-TRANSACTION.md"

# Phase 3: ブロック機能
# 指示: "Please follow the instructions in ./instructions/03-BLOCK-MINER.md"

# Phase 4: チェーン管理
# 指示: "Please follow the instructions in ./instructions/04-BLOCKCHAIN.md"

# Phase 5: CLI統合
# 指示: "Please follow the instructions in ./instructions/05-CLI-INTEGRATION.md"
```

### 手動で実装する場合

1. `AGENTS.md` - 実装原則を確認
2. `要件整理書.md` - 何を作るかを理解
3. `基本設計.md` - 全体構造を理解
4. `詳細設計.md` - 各モジュールの仕様を確認
5. `instructions/` - 段階的に実装

## 動作確認

```bash
# トランザクション作成
python src/simple_blockchain/cli.py
# メニューで [2] を選択

# マイニング実行
# メニューで [4] を選択
# nonce探索の様子が表示される

# チェーン検証
# メニューで [6] を選択
# すべて正常ならOK

# 改ざんテスト
# メニューで [7] を選択
# ブロックのamountを変更

# 再検証
# メニューで [6] を選択
# 改ざんが検出される
```

## 技術仕様

- **言語:** Python 3.8+
- **依存:** 標準ライブラリのみ
- **ハッシュ:** SHA256
- **難易度:** 先頭"00"一致（固定）
- **永続化:** JSON ファイル

## 学習の進め方

1. **まず動かす:** CLIで全機能を体験
2. **コードを読む:** 各モジュールの実装を確認
3. **改ざんしてみる:** data/blocks/ のJSONを直接編集
4. **検証する:** チェーン検証でエラーを確認
5. **改造する:** difficulty変更、機能追加など

## 非対応機能（意図的に省略）

- ❌ 公開鍵暗号・電子署名
- ❌ P2P ネットワーク
- ❌ マークルツリー
- ❌ UTXOモデル
- ❌ スマートコントラクト

**理由:** 本プロジェクトは「チェーン構造の理解」に特化しています。

## トラブルシューティング

**Q: マイニングが終わらない**  
A: difficulty が高すぎる可能性。miner.py の difficulty を "0" に変更

**Q: ブロックが見つからない**  
A: data/blocks/ にファイルがあるか確認

**Q: トランザクションが作れない**  
A: data/participants.json に参加者が登録されているか確認

## ライセンス

MIT License - 自由に学習・改変してください

## 参考資料

- [ビットコイン原論文](https://bitcoin.org/bitcoin.pdf)
- [Blockchain Demo](https://andersbrownworth.com/blockchain/)
- Python ハッシュライブラリ: `hashlib`

---

**開発者向け:** 詳細な設計書は `要件整理書.md`, `基本設計.md`, `詳細設計.md` を参照
