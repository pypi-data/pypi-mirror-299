from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import paramiko

app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key'  # 用于Flash消息和表单CSRF保护

# 初始化Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# 用户模型
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# 模拟用户数据库
users = {'admin': {'password': 'admin'}}

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
@login_required
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 验证Linux系统的用户名和密码
        try:
            # 使用paramiko进行SSH连接
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect('your_linux_server_ip', username=username, password=password)
            ssh.close()

            # 如果连接成功，登录用户
            if username in users and users[username]['password'] == password:
                user = User(username)
                login_user(user)
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password', 'error')
        except paramiko.AuthenticationException:
            flash('Invalid username or password', 'error')
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()