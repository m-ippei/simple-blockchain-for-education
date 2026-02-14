"""
トランザクション管理モジュール

ブロックチェーン上の取引（トランザクション）を管理する。
- トランザクションの作成
- 未処理トランザクションの保存・読み込み・削除
"""

import json
import time
import os
import participants


def create_transaction():
    """
    対話的にトランザクションを作成する

    ユーザーから入力を受け取り、検証後にJSONファイルとして保存する。
    """
    print("\n" + "=" * 40)
    print(" トランザクション作成")
    print("=" * 40)

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
        "timestamp": int(time.time()),
    }

    # ファイル保存
    os.makedirs("data/transactions", exist_ok=True)

    # ファイル名: transaction-0001.json 形式
    existing_files = [
        f for f in os.listdir("data/transactions") if f.startswith("transaction-")
    ]
    next_id = len(existing_files) + 1
    filename = f"data/transactions/transaction-{next_id:04d}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(transaction, f, indent=2, ensure_ascii=False)

    print(f"✅ トランザクション作成成功: {filename}")
    print(f"   {from_address} → {to_address}: {amount}")
    print("=" * 40 + "\n")


def get_pending_transactions() -> list[dict]:
    """
    未処理のトランザクション一覧を取得

    data/transactions/ ディレクトリ内のすべてのJSONファイルを読み込む。

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


def display_pending_transactions():
    """
    未処理トランザクション一覧を表示
    """
    print("\n" + "=" * 40)
    print(" 未処理トランザクション")
    print("=" * 40)

    transactions = get_pending_transactions()

    if not transactions:
        print("未処理のトランザクションはありません")
    else:
        for i, tx in enumerate(transactions, 1):
            print(f"{i}. {tx['from']} → {tx['to']}: {tx['amount']}")
            print(f"   タイムスタンプ: {tx['timestamp']}")

    print("=" * 40 + "\n")


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


if __name__ == "__main__":
    print("=== トランザクション管理モジュール テスト ===\n")

    # トランザクション作成テスト
    create_transaction()

    # 未処理トランザクション表示
    display_pending_transactions()
