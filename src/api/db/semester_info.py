class semester_info:

    def __init__(self, db_wrapper):
        self.db = db_wrapper

    def upsert(self, semester, isPublic):
        self.db.execute("""
            INSERT INTO semester_info (semester, public)
            VALUES (%(semester_name)s, %(is_public)s)
            ON CONFLICT ON CONSTRAINT semester_info_pkey
            DO UPDATE
            SET public = = EXCLUDED.public;
        """,
        {
            "semester_name": semester,
            "is_public": isPublic
        }, 
        isSELECT=False)

    def is_public(self, semester):
        """
        @param: semester name
        @returns: Boolean indicating if the semester is publicly viewable
        """
        data, error = self.db.execute("""
            SELECT public FROM semester_info WHERE semester=%s LIMIT 1;
        """, [semester], isSELECT=True)
        
        if error:  # Handle query execution errors
            return False

        return next(iter(data), {}).get('public', False)