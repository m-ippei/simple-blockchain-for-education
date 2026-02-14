# 02-PARTICIPANTS-TRANSACTION - 参加者管理とトランザクション機能

## 指示タイプ
**FIRST_CODING** - 基礎モジュールの新規実装

## 目的
ブロックチェーンの最小単位である「トランザクション」と、その送受信者である「参加者」の管理機能を実装する。

---

## 前提条件

- `01-SETUP.md` が完了していること
- `data/participants.json` が存在すること

---

## 実装ファイル

### 1. src/simple_blockchain/participants.py

**責務:** 参加者データの読み込みと検証

**実装する関数:**

#### `load_participants() -> list[str]`

**処理内容:**
1. `data/participants.json` を読み込み
2. JSON をパースして list[str] として返す
3. ファイルが存在しない場合は例外を発生させる

**実装例:**
```python
import json
import os

def load_participants() -> list[str]:
    """
    参加者リストをJSONファイルから読み込む
    
    Returns:
        list[str]: 参加者名のリスト
        
    Raises:
        FileNotFoundError: participants.jsonが存在しない場合
    """
    filepath = "data/participants.json"
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"{filepath} が見つかりません")
    
    with open(filepath, "r", encoding="utf-8") as f:
        participants = json.load(f)
    
    return participants
```

#### `is_valid_address(address: str) -> bool`

**処理内容:**
1. address が3〜5文字であることを確認
2. participants.json に登録されているかを確認
3. 両方を満たす場合のみ True

**実装例:**
```python
def is_valid_address(address: str) -> bool:
    """
    アドレスが有効かどうかを判定する
    
    Args:
        address: 検証するアドレス
        
    Returns:
        bool: 有効なら True
    """
    # 長さチェック
    if not (3 <= len(address) <= 5):
        return False
    
    # 登録済みかチェック
    participants = load_participants()
    return address in participants
```

#### `display_participants()`

**処理内容:**
1. 参加者一覧を読み込み
2. 見やすい形式で表示

**実装例:**
```python
def display_participants():
    """
    参加者一覧を表示する
    """
    print("\n" + "="*40)
    print(" 登録済み参加者一覧")
    print("="*40)
    
    participants = load_participants()
    for i, name in enumerate(participants, 1):
        print(f"{i}. {name}")
    
    print("="*40 + "\n")
```

---

### 2. src/simple_blockchain/transaction.py

**責務:** トランザクションの作成、保存、読み込み

**実装する関数:**

#### `create_transaction()`

**処理内容:**
1. 送信元 (from) を入力
2. 送信先 (to) を入力
3. 金額 (amount) を入力
4. バリデーション実行
5. タイムスタンプ付与
6. ファイル保存

**実装例:**
```python
import json
import time
import os
from . import participants

def create_transaction():
    """
    対話的にトランザクションを作成する
    """
    print("\n" + "="*40)
    print(" トランザクション作成")
    print("="*40)
    
    # 入力
    from_address = input("送信元 (from): ").strip()
    to_address = input("送信先 (to): ").strip()
    
    try:
        amount = int(input("金額 (amount): ").strip())
    except ValueError:
        print("❌ エラー: 金額は整数で入力してください")
        return
    
    # バリデーション
    if not participants.is_valid_address(from_address):
        print(f"❌ エラー: '{from_address}' は登録されていません")
        return
    
    if not participants.is_valid_address(to_address):
        print(f"❌ エラー: '{to_address}' は登録されていません")
        return
    
    if amount <= 0:
        print("❌ エラー: 金額は正の整数である必要があります")
        return
    
    if from_address == to_address:
        print("❌ エラー: 送信元と送信先が同じです")
        return
    
    # トランザクションデータ作成
    transaction = {
        "from": from_address,
        "to": to_address,
        "amount": amount,
        "timestamp": int(time.time())
    }
    
    # ファイル保存
    os.makedirs("data/transactions", exist_ok=True)
    
    # ファイル名: transaction-0001.json 形式
    existing_files = [f for f in os.listdir("data/transactions") if f.startswith("transaction-")]
    next_id = len(existing_files) + 1
    filename = f"data/transactions/transaction-{next_id:04d}.json"
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(transaction, f, indent=2, ensure_ascii=False)
    
    print(f"✅ トランザクション作成成功: {filename}")
    print(f"   {from_address} → {to_address}: {amount}")
    print("="*40 + "\n")
```

#### `get_pending_transactions() -> list[dict]`

**処理内容:**
1. `data/transactions/` 内のすべての .json ファイルを読み込み
2. トランザクションのリストとして返す

**実装例:**
```python
def get_pending_transactions() -> list[dict]:
    """
    未処理のトランザクション一覧を取得
    
    Returns:
        list[dict]: トランザクションのリスト
    """
    transactions = []
    transaction_dir = "data/transactions"
    
    if not os.path.exists(transaction_dir):
        return transactions
    
    for filename in sorted(os.listdir(transaction_dir)):
        if filename.endswith(".json"):
            filepath = os.path.join(transaction_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                transaction = json.load(f)
                transactions.append(transaction)
    
    return transactions
```

#### `display_pending_transactions()`

**処理内容:**
1. 未処理トランザクションを取得
2. 見やすい形式で表示

**実装例:**
```python
def display_pending_transactions():
    """
    未処理トランザクション一覧を表示
    """
    print("\n" + "="*40)
    print(" 未処理トランザクション")
    print("="*40)
    
    transactions = get_pending_transactions()
    
    if not transactions:
        print("未処理のトランザクションはありません")
    else:
        for i, tx in enumerate(transactions, 1):
            print(f"{i}. {tx['from']} → {tx['to']}: {tx['amount']}")
            print(f"   タイムスタンプ: {tx['timestamp']}")
    
    print("="*40 + "\n")
```

#### `clear_pending_transactions()`

**処理内容:**
1. `data/transactions/` 内のすべての .json ファイルを削除
2. マイニング後に呼び出される

**実装例:**
```python
def clear_pending_transactions():
    """
    未処理トランザクションをすべて削除
    （マイニング完了後に使用）
    """
    transaction_dir = "data/transactions"
    
    if not os.path.exists(transaction_dir):
        return
    
    for filename in os.listdir(transaction_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(transaction_dir, filename)
            os.remove(filepath)
```

---

## コーディング規約

1. **型ヒント:** すべての関数に型ヒントを付ける
2. **docstring:** 各関数にdocstringを記述
3. **エラーメッセージ:** 初心者にわかりやすく明示
4. **視覚的な区切り:** `print("="*40)` で視認性向上
5. **import順序:** 標準ライブラリ → 相対import

---

## テスト方法

### participants.py のテスト

```python
# ファイル末尾に追加
if __name__ == "__main__":
    print("=== 参加者管理モジュール テスト ===\n")
    
    # 参加者一覧表示
    display_participants()
    
    # アドレス検証テスト
    test_addresses = ["Alice", "Bob", "Unknown", "X"]
    for addr in test_addresses:
        result = is_valid_address(addr)
        print(f"{addr}: {'✅ 有効' if result else '❌ 無効'}")
```

実行:
```bash
python src/simple_blockchain/participants.py
```

### transaction.py のテスト

```python
# ファイル末尾に追加
if __name__ == "__main__":
    print("=== トランザクション管理モジュール テスト ===\n")
    
    # トランザクション作成テスト
    create_transaction()
    
    # 未処理トランザクション表示
    display_pending_transactions()
```

実行:
```bash
python src/simple_blockchain/transaction.py
```

---

## 完了条件

✅ `participants.py` に3つの関数が実装されている  
✅ `transaction.py` に4つの関数が実装されている  
✅ 各関数にdocstringが記述されている  
✅ テストコードが動作する  
✅ エラーハンドリングが適切

---

## 動作確認例

```bash
# 参加者一覧表示
python src/simple_blockchain/participants.py

# トランザクション作成
python src/simple_blockchain/transaction.py
# 入力例:
#   送信元: Alice
#   送信先: Bob
#   金額: 100

# ファイル確認
ls data/transactions/
cat data/transactions/transaction-0001.json
```

---

## トラブルシューティング

**Q: ModuleNotFoundError が出る**  
A: `src/simple_blockchain/__init__.py` が存在するか確認

**Q: participants.json が読めない**  
A: カレントディレクトリが `simple-blockchain/` であるか確認

**Q: 相対importでエラー**  
A: `from . import participants` ではなく `import participants` に変更

---

## 次のステップ

実装とテストが完了したら:

```
Please follow the instructions in ./instructions/03-BLOCK-MINER.md
```
