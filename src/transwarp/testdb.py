import _mysql
db = _mysql.connect('localhost','root','123456','awesome')
db.query("SELECT * FROM `users`")
r = db.use_result()
print r.fetch_row()