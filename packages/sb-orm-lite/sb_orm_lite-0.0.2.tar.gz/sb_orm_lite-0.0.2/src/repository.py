from typing import List

from sb_db_common import Session


class Repository(object):
    entity_type: type = None

    def __init__(self, entity_type: type):
        self.entity_type = entity_type

    def fetch_all(self, session: Session) -> List[object]:
        return self._fetch_many(session, self.entity_type.__select__)

    def fetch_one(self, session: Session, where_clause: str | None, id: dict):
        if where_clause is None:
            where_clause = self.entity_type.__where_id__
        with session.fetch(self.entity_type.__select__ + where_clause, id) as cursor:
            row = cursor.fetchone()
            if row is None:
                return None

            item = self.entity_type()
            item.map_row(row)
            return item

    def _fetch_many(self, session: Session, sql: str, params: dict = None):
        with session.fetch(sql, params) as cursor:
            result: List[object] = []
            rows = cursor.fetchall()
            for row in rows:
                item = self.entity_type()
                item.map_row(row)
                result.append(item)

            return result

    def insert(self, session: Session, item: object):
        item.add(session)

    def update(self, session: Session, item: object):
        item.update(session)

    def delete(self, session: Session, item: object):
        item.delete(session)
