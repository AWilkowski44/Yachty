from flask import Flask, render_template, url_for, request, redirect, make_response, session
import data_handler as dh

# this fixes the bug with non-loading JS files
import mimetypes
mimetypes.add_type('text/javascript', '.js')


# template_folder = os.path.join(template_folder, 'static')
# template_folder = os.path.join(template_folder, 'templates')
app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    """
    This is a one-pager which shows all the boards and cards
    """

    return render_template('index.html')


# API SECTION

# user register and login section

@app.route("/login", methods=['GET'])
def login():
    return render_template('login.html')


@app.route("/register", methods=['GET'])
def registration():
    return render_template('register.html')


@app.route("/register", methods=['POST'])
def user_register():
    """
    Register a new user and store credentials in a database
    Returns OK if successful or user id
    TODO checking if user already exists
    TODO data validation
    """
    login, password = request.form['email'], request.form['password']

    registered = False

    if login and password:
        registered = dh.user_register(login, password)

    return redirect('index')

@app.route("/login", methods=['POST'])
def user_login():
    """
    Takes user login and password
    Returns session id
    TODO check if session already exists and don't generate new
    TODO garbage collector for expired sessions
    there is verify session for checking tokens
    """

    # login, password = request.json['login'], request.json['password']
    login, password = request.form['login'], request.form['password']

    if dh.check_credentials(login, password):
        res = make_response(redirect('index'))
        # res.set_cookie("token", value=dh.open_session(login))
        return res
    else:
        return redirect('login')





def app_start():
    app.run(debug=True, port=5000)

    # Serving the favicon
    with app.app_context():
        app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon/favicon.ico'))