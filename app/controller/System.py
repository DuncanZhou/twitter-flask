import socket

from app.controller import verify
from app.models import Admin
from flask import request, render_template, jsonify, session, redirect, url_for

@verify
def pass_change():
	return render_template('pass_change.html')

@verify
def pass_change_submit():
	user = Admin.query.filter(Admin.userid == session['userid']).first()
	if user.password != request.form['password']:
		return jsonify({'status': 0})

	if request.form['new_password'] != request.form['confirm_password']:
		return jsonify({'status': 1})

	res = Admin.query.filter(Admin.userid == session['userid']).update({Admin.password: request.form['new_password'] })
	
	if res == None:
		return jsonify({'status': 2})
	else:
 		return jsonify({'status': 3})

@verify
def system_help():
	return render_template('system_help.html')

@verify
def main():
	server_name = socket.getfqdn(socket.gethostname(  ))
	server_addr = socket.gethostbyname(server_name)

	return render_template('main.html', user_agent = request.user_agent, remote_addr = request.remote_addr, server_name = server_name, server_addr = server_addr)

