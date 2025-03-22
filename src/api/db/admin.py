class Admin:

	def __init__(self, db_conn):
		self.db_conn = db_conn
		self.interface_name = 'admin_info'

	def get_semester_default(self):
		# NOTE: COALESCE takes first non-null vaue from the list
		result, error = self.db_conn.execute("""
			SELECT admin.semester FROM admin_settings admin
			UNION ALL
			SELECT si.semester FROM semester_info si WHERE si.public=true::boolean
			LIMIT 1
		""", None, True)

		if error:
            return None, error

		# Get first row safely, or default to None
        default_semester = result[0]['semester'] if result else None

		return default_semester, None



	def set_semester_default(self, semester):
		try:
			cmd = """
				WITH deleted AS (DELETE FROM admin_settings)
				INSERT INTO admin_settings(semester)
				VALUES (%s)
				ON CONFLICT (semester) DO UPDATE SET semester = EXCLUDED.semester
			"""
			response, error = self.db_conn.execute(cmd, [semester], False)

		if error:
			self.db_conn.rollback()
			return (False, e)

		return bool(response), None  #response check

		except Exception as e:
        	self.db_conn.rollback()  # Ensure rollback in case of exception
        	return False, str(e)     # Return string message for debugging
