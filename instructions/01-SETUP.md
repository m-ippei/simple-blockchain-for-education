# 01-SETUP - プロジェクトセットアップ

## 指示タイプ
**INITIAL_SETUP** - プロジェクト構造とデータファイルの準備

## 目的
ブロックチェーン実装の土台となるディレクトリ構造とサンプルデータを作成する。

---

## 実装内容

### 1. ディレクトリ構造の作成

以下の構造を作成してください：

```
simple-blockchain/
├── src/
│   └── simple_blockchain/
│       └── __init__.py
└── data/
    ├── participants.json
    ├── transactions/
    │   └── .gitkeep
    └── blocks/
        └── .gitkeep
```

### 2. participants.json の作成

`data/participants.json` を以下の内容で作成：

```json
[
  "Alice",
  "Bob",
  "Carol",
  "Dave"
]
```

**仕様:**
- 参加者は4〜5文字の名前
- 配列形式
- ブロックチェーンに参加できるアドレスのリスト

### 3. __init__.py の作成

`src/simple_blockchain/__init__.py` を以下の内容で作成：

```python
"""
Simple Blockchain - 学習用ブロックチェーン実装
"""

__version__ = "0.1.0"
```

### 4. .gitkeep ファイル

空のディレクトリを Git で管理するため、以下のファイルを作成：
- `data/transactions/.gitkeep`
- `data/blocks/.gitkeep`

（内容は空でOK）

---

## 完了条件

以下が揃っていること：

✅ `src/simple_blockchain/` ディレクトリが存在  
✅ `data/participants.json` に4名の参加者データ  
✅ `data/transactions/` ディレクトリが存在  
✅ `data/blocks/` ディレクトリが存在  
✅ `__init__.py` が存在

---

## 確認方法

```bash
# ディレクトリ構造の確認
tree simple-blockchain/

# participants.json の確認
cat data/participants.json
```

---

## 次のステップ

セットアップ完了後、以下を実行：

```
Please follow the instructions in ./instructions/02-PARTICIPANTS-TRANSACTION.md
```
