from db.model import *

class User(Model):
    def __init__(self):
        super().__init__()

    def get_user(self, uid=None, name=None, email=None, phone=None, password=None, major=None, degree=None, enable=True):
        base_query = """
            SELECT user_id, name, email, phone, password, major, degree, enable, admin, super_admin
            FROM public.user_account
        """
        conditions = []
        args = {}

        if uid is not None:
            conditions.append("user_id::text = %(uid)s")
            args["uid"] = str(uid)
        if name is not None:
            conditions.append("name ILIKE %(name)s")
            args["name"] = f"%{name}%"
        if email is not None:
            conditions.append("email ILIKE %(email)s")
            args["email"] = f"%{email}%"
        if phone is not None:
            conditions.append("phone LIKE %(phone)s")
            args["phone"] = f"%{phone}%"
        if password is not None:
            conditions.append("password LIKE %(password)s")
            args["password"] = f"%{password}%"
        if major is not None:
            conditions.append("major LIKE %(major)s")
            args["major"] = f"%{major}%"
        if degree is not None:
            conditions.append("degree LIKE %(degree)s")
            args["degree"] = f"%{degree}%"
        if enable is not None:
            conditions.append("enable IS %(enable)s")
            args["enable"] = enable

        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)

        return self.db.execute(base_query, args, isSELECT=True)[0]


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
