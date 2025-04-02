class semester_date_mapping:

    def __init__(self, db_wrapper):
        self.db = db_wrapper

    def insert(self, date_start, date_end, name):
        query = """
            INSERT INTO semester_date_range (semester_part_name, date_start, date_end)
            VALUES (%(name)s, %(date_start)s, %(date_end)s)
            ON CONFLICT DO NOTHING
            RETURNING *;
        """
        params = {
            "name": name,
            "date_start": date_start,
            "date_end": date_end
        }

        result = self.db.execute(query, params, isSELECT=True)

        return result if result else None  # Returns inserted row or None if conflict occurred

    def insert_all(self, start_dates, end_dates, names):
        if not (len(start_dates) == len(end_dates) == len(names)):
            return (False, "Mismatched input list lengths.")

        values = [
            {
                "name": names[i],
                "date_start": start_dates[i],
                "date_end": end_dates[i]
            }
            for i in range(len(names)) if names[i] and not names[i].isspace()
        ]

        if not values:  # If the filtered list is empty, return success
            return (True, None)

        query = """
            INSERT INTO semester_date_range (semester_part_name, date_start, date_end)
            VALUES (%(name)s, %(date_start)s, %(date_end)s)
            ON CONFLICT (semester_part_name)
            DO UPDATE SET date_start = EXCLUDED.date_start, date_end = EXCLUDED.date_end
            RETURNING *;
        """

        try:
            result = self.db.executemany(query, values)
            return (True, result)
        except Exception as e:
            return (False, str(e))