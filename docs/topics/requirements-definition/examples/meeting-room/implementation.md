# 実例：実装とテストコード

架空の「会議室予約システム」の、予約登録処理の実装と、そのテストコードです。

- 実装したのは、処理の中心部分（[設計書](design.md) の DD-01、DD-02）だけです。画面（SCR-01）と API（API-01）は実装していません。
- コメントに、設計書やテスト仕様書の ID を書いています。
- コードは AI が書いたものです。テストは実際に実行し、8件すべて成功しました。

## 実装

ファイル：`examples/meeting-room/src/reservation.py`

```python
--8<-- "docs/topics/requirements-definition/examples/meeting-room/src/reservation.py"
```

## テストコード

ファイル：`examples/meeting-room/src/test_reservation.py`

[テスト仕様書](test-spec.md) の単体テスト（UT-01〜04）と結合テスト（IT-01〜04）を、コードにしたものです。

```python
--8<-- "docs/topics/requirements-definition/examples/meeting-room/src/test_reservation.py"
```

## 動かし方

Python 3 があれば動きます。追加で入れるものはありません。

```bash
cd docs/topics/requirements-definition/examples/meeting-room/src
python3 -m unittest -v
```
