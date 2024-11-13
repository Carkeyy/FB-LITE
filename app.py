from flask import Flask, render_template, request, redirect, url_for, session
from flask import jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# In-memory storage for users, posts, and messages
users = {}
posts = []
messages = {}

# Home route
@app.route('/')
def index():
    return render_template('index.html', posts=posts)

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Simple validation
        if username in users:
            return 'Username already taken!'
        
        users[username] = password
        return redirect(url_for('login'))
    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if user exists and password matches
        if users.get(username) == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return 'Invalid credentials!'
    
    return render_template('login.html')

# Post status update route
@app.route('/post', methods=['POST'])
def post_status():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    content = request.form['content']
    username = session['username']
    posts.append({'username': username, 'content': content})
    return redirect(url_for('index'))

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Route to view messages
@app.route('/messages')
def view_messages():
    if 'username' not in session:
        return redirect(url_for('login'))

    user = session['username']
    # Fetch messages for the logged-in user
    user_messages = messages.get(user, [])
    return render_template('messages.html', messages=user_messages)

# Route to send a message
@app.route('/send_message', methods=['POST'])
def send_message():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    sender = session['username']
    recipient = request.form['recipient']
    message_content = request.form['message']
    
    if recipient not in users:
        return 'Recipient does not exist!'

    # Store the message for both sender and recipient
    if recipient not in messages:
        messages[recipient] = []
    if sender not in messages:
        messages[sender] = []
    
    messages[recipient].append({'sender': sender, 'message': message_content})
    messages[sender].append({'sender': sender, 'message': message_content})
    
    return redirect(url_for('view_messages'))

if __name__ == '__main__':
    app.run(debug=True)