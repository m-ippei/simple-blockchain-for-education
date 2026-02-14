# AGENTS.md - LLM/開発者向け実装ガイド

## 📋 プロジェクト概要

**目的:**  
Pythonでブロックチェーンの最小構造を実装し、トランザクション・ブロック・ハッシュチェーン・改ざん検知の仕組みを学ぶ。

**対象者:**  
- LLMによる自動実装（Agentic Coding）
- 人間による段階的実装
- ブロックチェーンを学びたい開発者

**成果物:**  
対話的CLIで動作する学習用ブロックチェーン

---

## 🎯 実装原則

### 1. 可読性最優先

❌ 悪い例:
```python
def h(d): return sha256(dumps(d).encode()).hexdigest()
```

✅ 良い例:
```python
def compute_hash(block_data: dict) -> str:
    """
    ブロックデータからSHA256ハッシュを計算
    
    Args:
        block_data: ブロックの辞書データ
        
    Returns:
        str: 16進数表現のハッシュ値
    """
    json_string = json.dumps(block_data, sort_keys=True)
    return hashlib.sha256(json_string.encode()).hexdigest()
```

### 2. 1ファイル1責務

| ファイル | 責務 |
|---------|------|
| participants.py | 参加者管理のみ |
| transaction.py | トランザクション管理のみ |
| block.py | ブロック定義のみ |
| miner.py | マイニング処理のみ |
| blockchain.py | チェーン管理のみ |
| cli.py | UI統合のみ |

### 3. 暗号強度は不要

- SHA256を使用するが、学習目的
- 実運用レベルの安全性は対象外
- difficulty="00" 程度で十分

### 4. コメント・docstring必須

```python
def is_valid_address(address: str) -> bool:
    """
    アドレスが有効かどうかを判定
    
    検証項目:
    1. 長さが3〜5文字
    2. participants.jsonに登録済み
    
    Args:
        address: 検証するアドレス
        
    Returns:
        bool: 有効なら True
    """
    # 実装...
```

### 5. ブラックボックス禁止

- ライブラリに頼らない
- すべて明示実装
- 処理を省略しない

---

## 🛠️ 技術仕様

### 使用技術

- **言語:** Python 3.8+
- **依存:** 標準ライブラリのみ
- **データ形式:** JSON
- **ハッシュ:** SHA256
- **難易度:** 固定（"00"推奨）

### 禁止事項

❌ 外部ライブラリ（requests, numpy等）  
❌ フレームワーク（Flask, Django等）  
❌ データベース（SQLite, MongoDB等）  
❌ 不要な抽象化・デザインパターン  
❌ 非説明的な短縮コード

---

## 📦 実装タスク分解

### Phase 1: セットアップ
**ファイル:** 01-SETUP.md  
**内容:**
- ディレクトリ構造作成
- participants.json 準備
- 空ディレクトリ作成

**所要時間:** 5分

### Phase 2: 基本モジュール
**ファイル:** 02-PARTICIPANTS-TRANSACTION.md  
**内容:**
- participants.py 実装
- transaction.py 実装
- 単体テスト

**所要時間:** 30分

### Phase 3: ブロック機能
**ファイル:** 03-BLOCK-MINER.md  
**内容:**
- block.py 実装（Blockクラス）
- miner.py 実装（PoW）
- 単体テスト

**所要時間:** 40分

### Phase 4: チェーン管理
**ファイル:** 04-BLOCKCHAIN.md  
**内容:**
- blockchain.py 実装
- 検証機能
- 単体テスト

**所要時間:** 30分

### Phase 5: CLI統合
**ファイル:** 05-CLI-INTEGRATION.md  
**内容:**
- cli.py 実装
- すべての機能統合
- 総合テスト

**所要時間:** 40分

**総実装時間:** 約2〜3時間

---

## 🤖 LLMへの指示方法

### Agentic Coding の場合

段階的に実装する：

```bash
# Phase 1
"Please follow the instructions in ./instructions/01-SETUP.md"

# Phase 2
"Please follow the instructions in ./instructions/02-PARTICIPANTS-TRANSACTION.md"

# Phase 3
"Please follow the instructions in ./instructions/03-BLOCK-MINER.md"

# Phase 4
"Please follow the instructions in ./instructions/04-BLOCKCHAIN.md"

# Phase 5
"Please follow the instructions in ./instructions/05-CLI-INTEGRATION.md"
```

---

## ✅ 完了定義

### 機能要件

- [ ] CLI起動が可能
- [ ] トランザクション作成が可能
- [ ] マイニングが実行できる
- [ ] チェーン表示が可能
- [ ] チェーン検証が可能
- [ ] 改ざん検知が動作する

### 品質要件

- [ ] すべての関数にdocstringがある
- [ ] エラーメッセージが初心者にわかりやすい
- [ ] 各モジュールが単体で実行可能
- [ ] 視覚的な区切り線で見やすい
- [ ] コメントが学習者向けに丁寧

### テスト要件

- [ ] 正常フロー（トランザクション → マイニング → 検証）
- [ ] 改ざん検知（ブロック改ざん → 検証エラー）
- [ ] エラー処理（不正なアドレス、負の金額等）

---

## 🐛 トラブルシューティング

### import エラー

**症状:** `ModuleNotFoundError: No module named 'simple_blockchain'`

**原因:** パッケージ構造が不適切、または実行場所が間違っている

**解決策:**
```bash
# 方法1: プロジェクトルートから実行
cd simple-blockchain
python -m src.simple_blockchain.cli

# 方法2: 相対importを絶対importに変更
# from . import participants
# ↓
# import participants
```

### data ディレクトリが見つからない

**症状:** `FileNotFoundError: data/participants.json`

**原因:** カレントディレクトリがプロジェクトルートでない

**解決策:**
```bash
# プロジェクトルートに移動
cd simple-blockchain
python src/simple_blockchain/cli.py
```

### マイニングが終わらない

**症状:** マイニングが数分経っても終わらない

**原因:** difficulty が高すぎる

**解決策:**
```python
# miner.py の difficulty を変更
mined_block = mine(block, difficulty="0")  # "00" → "0"
```

---

## 📚 学習の進め方

### 1. まず動かす（30分）

```bash
# instructions に従って実装
# 各Phaseごとにテスト
```

### 2. コードを読む（30分）

```python
# 各モジュールを読んで理解
# 特に重要な部分:
# - Block.compute_hash() - ハッシュ計算
# - mine() - Proof of Work
# - verify_chain() - 改ざん検知
```

### 3. 改ざんしてみる（30分）

```bash
# 1. ブロック改ざん（CLI機能またはファイル直接編集）
# 2. チェーン検証
# 3. エラーメッセージ確認
```

### 4. 改造する（1時間〜）

**初級:**
- difficulty を変更して試行回数を観察
- トランザクション数を増やす
- 参加者を追加

**中級:**
- 残高管理機能の追加
- トランザクション検索機能
- ブロック詳細表示

**上級:**
- マークルツリー実装
- UTXOモデル実装
- フォーク処理の実装

---

## 🎓 理解度チェック

実装後、以下の質問に答えられるか確認：

### 基本レベル

- [ ] トランザクションとは何か？
- [ ] ブロックとは何か？
- [ ] ハッシュの役割は何か？
- [ ] previous_hash の役割は何か？

### 中級レベル

- [ ] なぜ改ざんが検知できるのか？
- [ ] Proof of Work の目的は何か？
- [ ] nonce とは何か？
- [ ] difficulty の意味は何か？

### 上級レベル

- [ ] なぜJSON文字列化時に sort_keys=True なのか？
- [ ] チェーンの途中のブロックを改ざんすると何が起こるか？
- [ ] ジェネシスブロックとは何か？
- [ ] ブロックチェーンの不変性とは何か？

---

## 🚀 最重要方針

> このプロジェクトは「理解すること」が目的。
> 
> 速さ・強さ・美しさよりも
> 
> **"構造が透けて見えること"** を優先する。

---

## 📖 参考資料

### 公式ドキュメント

- [Python hashlib](https://docs.python.org/3/library/hashlib.html)
- [Python json](https://docs.python.org/3/library/json.html)

### ブロックチェーン学習

- [Bitcoin Whitepaper](https://bitcoin.org/bitcoin.pdf)
- [Blockchain Demo（視覚化）](https://andersbrownworth.com/blockchain/)
- [Mastering Bitcoin](https://github.com/bitcoinbook/bitcoinbook)

---

## 📝 メンテナンス情報

**バージョン:** 0.1.0  
**最終更新:** 2026-02-14  
**ライセンス:** MIT

**変更履歴:**
- 2026-02-14: 初版作成
