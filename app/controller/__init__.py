from flask import redirect, url_for, session


def verify(func):
	def wrapper(*args, **kw):
		if not session.get('userid'):
			return redirect(url_for('index'))

		return func(*args, **kw)
		
	return wrapper