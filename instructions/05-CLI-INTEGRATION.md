# 05-CLI-INTEGRATION - CLIアプリケーション統合

## 指示タイプ
**FIRST_CODING + INTEGRATION** - すべてのモジュールを統合したCLIアプリケーション

## 目的
これまで実装したすべての機能を統合し、対話的なCLIアプリケーションを完成させる。

---

## 前提条件

- `04-BLOCKCHAIN.md` が完了していること
- すべてのモジュールが個別に動作すること

---

## 実装ファイル

### src/simple_blockchain/cli.py

**責務:** ユーザーインターフェースとすべての機能の統合

**実装する関数:**

#### `display_header()`

メインメニューのヘッダーを表示

**実装例:**

```python
def display_header():
    """
    CLIのヘッダーを表示
    """
    print("\n" + "="*60)
    print(" Simple Blockchain - 学習用ブロックチェーン")
    print("="*60)


def display_status():
    """
    現在の状態を表示
    """
    from . import blockchain, transaction
    
    status = blockchain.get_chain_status()
    pending_count = len(transaction.get_pending_transactions())
    
    print(f"\n現在のブロック数: {status['block_count']}")
    print(f"未処理トランザクション: {pending_count}")


def display_menu():
    """
    メニューを表示
    """
    print("\n" + "-"*60)
    print("[1] 参加者一覧")
    print("[2] トランザクション作成")
    print("[3] 未処理トランザクション表示")
    print("[4] マイニング実行")
    print("[5] チェーン表示")
    print("[6] チェーン検証")
    print("[7] ブロック改ざん（学習用）")
    print("[8] 終了")
    print("-"*60)
```

#### `handle_menu_1()` - 参加者一覧

```python
def handle_menu_1():
    """
    [1] 参加者一覧
    """
    from . import participants
    participants.display_participants()
```

#### `handle_menu_2()` - トランザクション作成

```python
def handle_menu_2():
    """
    [2] トランザクション作成
    """
    from . import transaction
    transaction.create_transaction()
```

#### `handle_menu_3()` - 未処理トランザクション表示

```python
def handle_menu_3():
    """
    [3] 未処理トランザクション表示
    """
    from . import transaction
    transaction.display_pending_transactions()
```

#### `handle_menu_4()` - マイニング実行

```python
def handle_menu_4():
    """
    [4] マイニング実行
    """
    from . import blockchain, transaction, miner
    from .block import Block
    
    # 未処理トランザクションを取得
    pending_txs = transaction.get_pending_transactions()
    
    if not pending_txs:
        print("\n⚠️  未処理トランザクションがありません")
        print("まずトランザクションを作成してください")
        return
    
    # 最後のブロックを取得
    last_block = blockchain.get_last_block()
    
    if last_block is None:
        # ジェネシスブロックを作成
        print("\n最初のブロック（ジェネシスブロック）を作成します...")
        genesis = miner.create_genesis_block()
        blockchain.add_block(genesis)
        
        # もう一度最後のブロックを取得
        last_block = blockchain.get_last_block()
    
    # 新しいブロックを作成
    new_index = last_block.index + 1
    new_block = Block(
        index=new_index,
        transactions=pending_txs,
        previous_hash=last_block.hash
    )
    
    # マイニング実行
    mined_block = miner.mine(new_block, difficulty="00")
    
    # チェーンに追加
    if blockchain.add_block(mined_block):
        print("✅ ブロックがチェーンに追加されました")
        
        # 未処理トランザクションをクリア
        transaction.clear_pending_transactions()
        print("✅ 未処理トランザクションをクリアしました")
    else:
        print("❌ ブロックの追加に失敗しました")
```

#### `handle_menu_5()` - チェーン表示

```python
def handle_menu_5():
    """
    [5] チェーン表示
    """
    from . import blockchain
    blockchain.display_chain()
```

#### `handle_menu_6()` - チェーン検証

```python
def handle_menu_6():
    """
    [6] チェーン検証
    """
    from . import blockchain
    blockchain.verify_chain()
```

#### `handle_menu_7()` - ブロック改ざん

```python
def handle_menu_7():
    """
    [7] ブロック改ざん（学習用）
    
    特定のブロックのデータを改ざんして、検証機能を体験する
    """
    import json
    import os
    from . import blockchain
    
    print("\n" + "="*60)
    print(" ブロック改ざん（学習用機能）")
    print("="*60)
    print("⚠️  この機能はブロックチェーンの改ざん検知を学ぶためのものです")
    
    # チェーンを読み込み
    chain = blockchain.load_blockchain()
    
    if not chain:
        print("\n❌ ブロックがありません")
        return
    
    # ブロック一覧表示
    print(f"\n現在のブロック数: {len(chain)}")
    for block in chain:
        print(f"  Block #{block.index}: {len(block.transactions)} トランザクション")
    
    # ブロック番号を入力
    try:
        block_index = int(input("\n改ざんするブロック番号: ").strip())
    except ValueError:
        print("❌ 無効な入力です")
        return
    
    # ブロックファイルを読み込み
    filename = f"data/blocks/block-{block_index:04d}.json"
    
    if not os.path.exists(filename):
        print(f"❌ Block #{block_index} が見つかりません")
        return
    
    with open(filename, "r", encoding="utf-8") as f:
        block_data = json.load(f)
    
    # トランザクション表示
    print(f"\nBlock #{block_index} のトランザクション:")
    for i, tx in enumerate(block_data["transactions"]):
        print(f"  {i}. {tx['from']} → {tx['to']}: {tx['amount']}")
    
    # 改ざんするトランザクション選択
    try:
        tx_index = int(input("\n改ざんするトランザクション番号: ").strip())
    except ValueError:
        print("❌ 無効な入力です")
        return
    
    if not (0 <= tx_index < len(block_data["transactions"])):
        print("❌ 無効なトランザクション番号です")
        return
    
    # 新しい金額を入力
    try:
        new_amount = int(input("新しい金額: ").strip())
    except ValueError:
        print("❌ 無効な入力です")
        return
    
    # データ改ざん
    old_amount = block_data["transactions"][tx_index]["amount"]
    block_data["transactions"][tx_index]["amount"] = new_amount
    
    # ファイルに保存
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(block_data, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*60)
    print("✅ ブロックを改ざんしました")
    print("="*60)
    print(f"Block #{block_index}")
    print(f"トランザクション #{tx_index}")
    print(f"  変更前の金額: {old_amount}")
    print(f"  変更後の金額: {new_amount}")
    print("\n💡 ヒント: [6] チェーン検証 で改ざんが検出されます")
    print("="*60)
```

#### `main()` - メインループ

```python
def main():
    """
    CLIアプリケーションのメインループ
    """
    while True:
        # ヘッダー表示
        display_header()
        
        # 状態表示
        display_status()
        
        # メニュー表示
        display_menu()
        
        # 入力受付
        try:
            choice = input("\n選択してください: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n終了します...")
            break
        
        # メニュー処理
        if choice == "1":
            handle_menu_1()
        elif choice == "2":
            handle_menu_2()
        elif choice == "3":
            handle_menu_3()
        elif choice == "4":
            handle_menu_4()
        elif choice == "5":
            handle_menu_5()
        elif choice == "6":
            handle_menu_6()
        elif choice == "7":
            handle_menu_7()
        elif choice == "8":
            print("\n終了します...")
            break
        else:
            print("\n❌ 無効な選択です")
        
        # 次の操作まで一時停止
        input("\nEnterキーを押して続行...")


if __name__ == "__main__":
    main()
```

---

## 完全なファイル構造

```python
"""
src/simple_blockchain/cli.py

学習用ブロックチェーンのCLIアプリケーション
"""

def display_header():
    # ...実装...

def display_status():
    # ...実装...

def display_menu():
    # ...実装...

def handle_menu_1():
    # ...実装...

def handle_menu_2():
    # ...実装...

def handle_menu_3():
    # ...実装...

def handle_menu_4():
    # ...実装...

def handle_menu_5():
    # ...実装...

def handle_menu_6():
    # ...実装...

def handle_menu_7():
    # ...実装...

def main():
    # ...実装...

if __name__ == "__main__":
    main()
```

---

## テスト方法

### 基本動作テスト

```bash
# CLIを起動
python src/simple_blockchain/cli.py

# または（プロジェクトルートから）
cd simple-blockchain
python -m src.simple_blockchain.cli
```

### シナリオテスト

#### シナリオ1: 正常フロー

```
1. [1] 参加者一覧 → 4名表示される
2. [2] トランザクション作成
   - from: Alice
   - to: Bob
   - amount: 100
3. [2] トランザクション作成（もう1件）
   - from: Bob
   - to: Carol
   - amount: 50
4. [3] 未処理トランザクション表示 → 2件表示
5. [4] マイニング実行 → ジェネシスブロック作成
6. [4] マイニング実行 → Block #1作成
7. [5] チェーン表示 → 2ブロック表示
8. [6] チェーン検証 → 正常
```

#### シナリオ2: 改ざん検知

```
1. [5] チェーン表示
2. [7] ブロック改ざん
   - ブロック番号: 1
   - トランザクション番号: 0
   - 新しい金額: 999
3. [6] チェーン検証 → 改ざん検出！
```

---

## 完了条件

✅ CLIアプリケーションが起動する  
✅ すべてのメニューが動作する  
✅ トランザクション → マイニング → 検証の流れが動く  
✅ 改ざん検知が動作する  
✅ エラーメッセージが適切に表示される

---

## トラブルシューティング

**Q: import エラーが出る**  
A: `src/simple_blockchain/__init__.py` が存在するか確認

**Q: 相対importでエラー**  
A: `python -m` で実行するか、絶対importに変更

**Q: data ディレクトリが見つからない**  
A: プロジェクトルートから実行しているか確認

---

## 完成チェックリスト

最終確認として、以下すべてが動作することを確認してください：

- [ ] CLIが起動する
- [ ] 参加者一覧が表示される
- [ ] トランザクションが作成できる
- [ ] 未処理トランザクションが表示される
- [ ] マイニングが実行できる（ジェネシスブロック）
- [ ] マイニングが実行できる（通常ブロック）
- [ ] チェーンが表示される
- [ ] チェーン検証が通る
- [ ] ブロック改ざんができる
- [ ] 改ざん後の検証で エラーが検出される
- [ ] 終了できる

---

## 次のステップ（実装完了後）

### 1. ドキュメント作成

プロジェクトの使い方をまとめた README.md を作成（任意）

### 2. 発展的な機能追加（任意）

- difficulty の動的変更機能
- トランザクション検索機能
- ブロック詳細表示機能
- チェーンのエクスポート/インポート機能
- 簡易的な残高管理機能

### 3. 学習の深化

- ビットコインのホワイトペーパーを読む
- Ethereumのスマートコントラクトについて学ぶ
- P2Pネットワークについて学ぶ
- 暗号学（公開鍵暗号、電子署名）について学ぶ

---

## おめでとうございます！

ブロックチェーンの基本構造の実装が完了しました。

このプロジェクトを通じて以下を学びました：

✅ トランザクションの構造  
✅ ブロックの連鎖構造  
✅ ハッシュによる改ざん検知  
✅ Proof of Work の仕組み  
✅ ブロックチェーンの不変性

---

**実装が完了したら、ぜひ以下を試してください：**

1. トランザクションを10件作成してマイニング
2. 複数ブロックを作成してチェーンを長くする
3. 途中のブロックを改ざんして、どのように検出されるか観察
4. difficulty を変更して、マイニング時間の変化を観察
5. コードを読み返して、各部分の役割を理解する

ブロックチェーン技術の理解が深まることを願っています！
