from db.model import *

class User(Model):
    def __init__(self):
        super().__init__()

    def get_user(self, uid=None, name=None, email=None, phone=None, password=None, major=None, degree=None, enable=True):
        sql = """
            SELECT user_id, name, email, phone, password, major, degree, enable, admin, super_admin
            FROM public.user_account
            WHERE (%(uid)s IS NULL OR user_id::text = %(uid)s)
              AND (%(name)s IS NULL OR name ILIKE %(name)s)
              AND (%(email)s IS NULL OR email ILIKE %(email)s)
              AND (%(phone)s IS NULL OR phone LIKE %(phone)s)
              AND (%(password)s IS NULL OR password LIKE %(password)s)
              AND (%(major)s IS NULL OR major LIKE %(major)s)
              AND (%(degree)s IS NULL OR degree LIKE %(degree)s)
              AND enable IS %(enable)s
        """

        args = {
            "uid": uid,
            "name": f"%{name}%" if name else None,
            "email": f"%{email}%" if email else None,
            "phone": f"%{phone}%" if phone else None,
            "password": f"%{password}%" if password else None,
            "major": f"%{major}%" if major else None,
            "degree": f"%{degree}%" if degree else None,
            "enable": enable
        }

        return self.db.execute(sql, args, True)[0]


    def add_user(self, args):

        sql = """
            INSERT INTO public.user_account (
                name,
                email,
                phone,
                password,
                major,
                degree,
                enable
            ) VALUES (
                %(name)s,
                %(email)s,
                %(phone)s,
                %(password)s,
                %(major)s,
                %(degree)s,
                %(enable)s
            )
            RETURNING user_id;
        """

        return self.db.execute(sql, args, True)[0]  # Returns the new user ID

    def delete_user(self, uid):
        try:
            sql = """
                BEGIN;
                DELETE FROM student_course_selection WHERE user_id = %(uid)s;
                DELETE FROM public.user_account WHERE user_id = %(uid)s;
                COMMIT;
            """
            args = {"uid": uid}

            self.db.execute(sql, args, False)
            return {"success": True, "message": f"User {uid} deleted successfully."}
        
        except Exception as e:
            return {"success": False, "error": str(e)}


    def update_user(self, args):
        sql = """   UPDATE
                        public.user_account
                    SET
                        name        = %(Name)s,
                        email       = %(Email)s,
                        phone       = %(Phone)s,
                        password    = %(Password)s,
                        major       = %(Major)s,
                        degree      = %(Degree)s
                    WHERE
                        user_id = %(UID)s;
                    """
        return self.db.execute(sql, args, False)[0]
