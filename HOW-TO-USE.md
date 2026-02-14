# 📚 Simple Blockchain - 実装ガイドセット 使い方

## 📦 このパッケージについて

学習用ブロックチェーンを実装するための完全なドキュメントセットです。
Agentic Coding（LLM自動実装）と人間による手動実装の両方に対応しています。

---

## 📁 ファイル構成

```
simple-blockchain/
├── README.md                          # プロジェクト概要（最初に読む）
├── AGENTS.md                          # 実装者向けガイド
├── DESIGN.md                          # 統合設計書（要件+基本+詳細）
├── instructions/                      # 段階的実装指示書
    ├── 01-SETUP.md
    ├── 02-PARTICIPANTS-TRANSACTION.md
    ├── 03-BLOCK-MINER.md
    ├── 04-BLOCKCHAIN.md
    └── 05-CLI-INTEGRATION.md

```

---

## 🚀 クイックスタート

### パターンA: Agentic Coding（推奨）

```bash
# 1. プロジェクトディレクトリ作成
mkdir simple-blockchain
cd simple-blockchain

# 2. このドキュメントセットを配置
# （simple-blockchain/ をコピー）

# 3. LLMに順次指示
"Please follow the instructions in ./instructions/01-SETUP.md"

"Please follow the instructions in ./instructions/02-PARTICIPANTS-TRANSACTION.md"

"Please follow the instructions in ./instructions/03-BLOCK-MINER.md"

"Please follow the instructions in ./instructions/04-BLOCKCHAIN.md"

"Please follow the instructions in ./instructions/05-CLI-INTEGRATION.md"
```

### パターンB: 人間による実装

```bash
# 1. まず全体像を把握
README.md を読む（5分）
DESIGN.md を読む（15分）
AGENTS.md を読む（10分）

# 2. 段階的に実装
instructions/01-SETUP.md → 実装 → テスト
instructions/02-PARTICIPANTS-TRANSACTION.md → 実装 → テスト
instructions/03-BLOCK-MINER.md → 実装 → テスト
instructions/04-BLOCKCHAIN.md → 実装 → テスト
instructions/05-CLI-INTEGRATION.md → 実装 → テスト

# 3. 動作確認
python src/simple_blockchain/cli.py
```

---

## 📖 各ファイルの役割

### README.md
**対象:** すべての人（最初に読むべき）  
**内容:**
- プロジェクト概要
- 学べること
- クイックスタート手順
- 基本的な使い方

**読むタイミング:** 最初

---

### AGENTS.md
**対象:** LLM実装者、開発者  
**内容:**
- 実装原則（可読性、1ファイル1責務など）
- コーディング規約
- タスク分解
- トラブルシューティング
- 学習の進め方

**読むタイミング:** 実装開始前

---

### DESIGN.md
**対象:** 設計を理解したい人  
**内容:**
- 要件定義（目的、スコープ、機能要件）
- システム設計（ディレクトリ構成、モジュール構成）
- モジュール詳細設計（全関数の仕様）
- データ設計（JSON構造）
- UI設計

**読むタイミング:** 実装中の参照、またはコードレビュー時

---

### instructions/ ディレクトリ
**対象:** 実装者（LLM/人間）  
**内容:**
段階的な実装指示。各ファイルは独立しており、順番に実行する。

| ファイル | 内容 | 所要時間 |
|---------|------|---------|
| 01-SETUP.md | ディレクトリ構造とデータファイル | 5分 |
| 02-PARTICIPANTS-TRANSACTION.md | 参加者管理、トランザクション | 30分 |
| 03-BLOCK-MINER.md | ブロック、マイニング | 40分 |
| 04-BLOCKCHAIN.md | チェーン管理、検証 | 30分 |
| 05-CLI-INTEGRATION.md | CLI統合、完成 | 40分 |

**読むタイミング:** 実装の各フェーズ

---

## 🎯 実装の進め方（詳細）

### Phase 1: セットアップ（5分）

```bash
# instructionsに従ってディレクトリ作成
01-SETUP.md を実行
→ data/participants.json 作成
→ ディレクトリ構造完成
```

**確認:**
```bash
ls -R simple-blockchain/
# data/participants.json が存在するか
```

---

### Phase 2: 基本モジュール（30分）

```bash
# instructionsに従って実装
02-PARTICIPANTS-TRANSACTION.md を実行
→ participants.py 実装
→ transaction.py 実装
→ テスト実行
```

**確認:**
```bash
python src/simple_blockchain/participants.py
python src/simple_blockchain/transaction.py
```

---

### Phase 3: ブロック機能（40分）

```bash
03-BLOCK-MINER.md を実行
→ block.py 実装
→ miner.py 実装
→ テスト実行
```

**確認:**
```bash
python src/simple_blockchain/block.py
python src/simple_blockchain/miner.py
# マイニングが動作するか確認
```

---

### Phase 4: チェーン管理（30分）

```bash
04-BLOCKCHAIN.md を実行
→ blockchain.py 実装
→ 検証機能実装
→ テスト実行
```

**確認:**
```bash
python src/simple_blockchain/blockchain.py
# ブロックが保存・読み込みできるか確認
```

---

### Phase 5: CLI統合（40分）

```bash
05-CLI-INTEGRATION.md を実行
→ cli.py 実装
→ すべての機能統合
→ 統合テスト
```

**確認:**
```bash
python src/simple_blockchain/cli.py
# メニューが表示され、すべての機能が動作するか確認
```

---

## ✅ 完成チェックリスト

実装完了後、以下をすべて確認してください：

### 機能確認
- [ ] CLIが起動する
- [ ] 参加者一覧が表示される
- [ ] トランザクションが作成できる
- [ ] マイニングが実行できる
- [ ] チェーンが表示される
- [ ] チェーン検証が通る
- [ ] ブロック改ざんが検出される

### コード品質
- [ ] すべての関数にdocstringがある
- [ ] エラーメッセージが明確
- [ ] 各モジュールが単体実行可能
- [ ] import が正しく動作する

### 理解度
- [ ] トランザクションとは何か説明できる
- [ ] ブロックの連鎖構造を説明できる
- [ ] ハッシュの役割を説明できる
- [ ] 改ざん検知の仕組みを説明できる

---

## 🐛 トラブルシューティング

### Q: どのファイルから読めばいいかわからない

A: 以下の順番で読んでください：
1. README.md（5分） - 全体像把握
2. AGENTS.md（10分） - 実装方針理解
3. instructions/01-SETUP.md - 実装開始

---

### Q: Agentic Coding と手動実装のどちらがいい？

A: 
- **Agentic Coding:** 速く実装したい、LLMの能力を試したい
- **手動実装:** 深く理解したい、学習重視

両方試すのもおすすめです。

---

### Q: instructions はどの順番で実行すべき？

A: 必ず番号順（01 → 02 → 03 → 04 → 05）で実行してください。
各フェーズは前のフェーズに依存しています。

---

## 🎓 学習のヒント

### 実装前にやること
1. README.md で全体像を把握
2. AGENTS.md で実装原則を理解
3. DESIGN.md で設計を確認（ざっと目を通す程度でOK）

### 実装中にやること
1. instructions/ を順番に実行
2. 各フェーズでテストを実行
3. わからないところは DESIGN.md を参照

### 実装後にやること
1. トランザクション → マイニング → 検証の一連の流れを試す
2. ブロックを改ざんして検証機能を確認
3. コードを読み返して理解を深める
4. difficulty を変更して挙動を観察

---

## 📞 サポート

### うまく動かない場合

1. instructions/ の「トラブルシューティング」セクションを確認
2. AGENTS.md の「トラブルシューティング」セクションを確認
3. エラーメッセージをよく読む
4. テストコードで動作確認

### 理解が深まらない場合

1. コードにコメントを追加しながら読む
2. 各関数を単体で実行して動作を確認
3. DESIGN.md の関数仕様を読み直す
4. 実際にブロックを改ざんして挙動を観察

---

## 🎉 完成したら

おめでとうございます！以下を試してみましょう：

### 基本
1. 10件のトランザクションを作成してマイニング
2. 5ブロックのチェーンを作る
3. 途中のブロックを改ざんして検証

### 発展
1. difficulty を変更して試行回数の違いを観察
2. 残高管理機能を追加
3. トランザクション検索機能を追加
4. ビットコインのホワイトペーパーを読む

---

**このドキュメントセットで、ブロックチェーンの理解が深まることを願っています！**

質問や改善提案があれば、プロジェクトのissueまでお願いします。
