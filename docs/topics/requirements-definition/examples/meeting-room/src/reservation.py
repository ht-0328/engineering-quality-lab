"""会議室予約（架空の題材）の予約登録処理。

設計書のどこを実装したかを、コメントの ID（DD-01 など）で示す。
"""

from dataclasses import dataclass
from datetime import datetime


class InvalidPeriod(Exception):
    """終了日時が開始日時より後になっていない。"""


class ReservationConflict(Exception):
    """同じ会議室に、時間帯が重なる予約がすでにある。"""


@dataclass(frozen=True)
class Reservation:
    """予約1件。設計書 TBL-01 の項目に対応する。"""

    room_id: str
    start_at: datetime
    end_at: datetime
    user_id: str


def overlaps(a_start: datetime, a_end: datetime, b_start: datetime, b_end: datetime) -> bool:
    """2つの時間帯が重なるかを返す。設計書 DD-01。

    片方の終了と、もう片方の開始が同じ時刻のときは、重ならない（BR-02）。
    """
    return a_start < b_end and b_start < a_end


class InMemoryReservationRepository:
    """予約の保存先。この実例ではメモリ上に持つ。"""

    def __init__(self) -> None:
        self._items: list[Reservation] = []

    def find_by_room(self, room_id: str) -> list[Reservation]:
        return [r for r in self._items if r.room_id == room_id]

    def add(self, reservation: Reservation) -> None:
        self._items.append(reservation)


class ReservationService:
    """予約登録処理。設計書 DD-02。"""

    def __init__(self, repository: InMemoryReservationRepository) -> None:
        self._repository = repository

    def reserve(self, room_id: str, start_at: datetime, end_at: datetime, user_id: str) -> Reservation:
        # DD-02 手順1：入力の確認（BR-03）
        if end_at <= start_at:
            raise InvalidPeriod("終了日時は、開始日時より後にしてください。")

        # DD-02 手順2〜3：同じ会議室の予約と、時間帯が重なるかを確かめる（BR-01）
        for existing in self._repository.find_by_room(room_id):
            if overlaps(start_at, end_at, existing.start_at, existing.end_at):
                # DD-02 手順4：重なりがあれば登録しない（UC-01 例外シナリオ1）
                raise ReservationConflict("この時間帯は、すでに予約されています。")

        # DD-02 手順5：登録する（UC-01 基本シナリオ）
        reservation = Reservation(room_id, start_at, end_at, user_id)
        self._repository.add(reservation)
        return reservation
