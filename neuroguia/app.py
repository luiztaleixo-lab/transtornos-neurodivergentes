import os
import json
import re
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_socketio import SocketIO, emit, join_room, leave_room
from models import db, User, ForumRoom, ForumMessage, PrivateMessage
from chatbot import get_response, CHATBOT_TOPICS

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'neuroguia-chave-secreta-segura-2026')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, realize login para acessar esta funcionalidade.'
login_manager.login_message_category = 'info'

socketio = SocketIO(app, cors_allowed_origins='*', async_mode='threading')

IMAGE_PATTERNS = [
    re.compile(r'(?i)\bhttps?://[^\s]+\.(?:png|jpe?g|gif|webp|svg|bmp|tiff|ico|heic|avif)(?:\?[^\s]*)?\b'),
    re.compile(r'(?i)!\[[^\]]*\]\([^)]+\)'),
    re.compile(r'(?i)<img\b'),
    re.compile(r'(?i)data:image/[a-zA-Z0-9.+-]+;base64'),
    re.compile(r'(?i)\b(?:imgur\.com|gyazo\.com|prntscr\.com|postimg\.cc|imgbb\.com|ibb\.co|tinypic\.com)/[^\s]+\b')
]

def contains_image_content(text: str) -> bool:
    if not text:
        return False
    for pattern in IMAGE_PATTERNS:
        if pattern.search(text):
            return True
    return False

def sanitize_message(text: str) -> str:
    cleaned = re.sub(r'<[^>]*?>', '', text)
    return cleaned.strip()

def load_conditions():
    json_path = os.path.join(app.root_path, 'static', 'data', 'conditions.json')
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# ----------------- ROTAS PRINCIPAIS -----------------

@app.route('/')
def index():
    conditions = load_conditions()
    selected_id = request.args.get('condicao', 'ah-sd')
    selected_condition = next((c for c in conditions if c['id'] == selected_id), conditions[0] if conditions else None)
    return render_template('index.html', conditions=conditions, selected=selected_condition)

@app.route('/condicoes/<condition_id>')
def condition_detail(condition_id):
    conditions = load_conditions()
    selected_condition = next((c for c in conditions if c['id'] == condition_id), None)
    if not selected_condition:
        abort(404)
    return render_template('index.html', conditions=conditions, selected=selected_condition)

# ----------------- AUTENTICACAO -----------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('Preencha todos os campos.', 'danger')
            return render_template('auth.html', mode='login')
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash(f'Bem-vindo(a), {user.username}.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Nome de usuário ou senha incorretos.', 'danger')
            
    return render_template('auth.html', mode='login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        bio = request.form.get('bio', '').strip()
        avatar_color = request.form.get('avatar_color', '#4a6b5d').strip()
        
        if not username or not password:
            flash('Nome de usuário e senha são obrigatórios.', 'danger')
            return render_template('auth.html', mode='register')
        
        if len(username) < 3 or len(username) > 30:
            flash('O nome de usuário deve ter entre 3 e 30 caracteres.', 'danger')
            return render_template('auth.html', mode='register')
            
        if len(password) < 6:
            flash('A senha deve conter no mínimo 6 caracteres.', 'danger')
            return render_template('auth.html', mode='register')
            
        if User.query.filter_by(username=username).first():
            flash('Este nome de usuário já está em uso. Escolha outro.', 'warning')
            return render_template('auth.html', mode='register')
            
        new_user = User(
            username=username,
            bio=bio[:500],
            avatar_color=avatar_color if avatar_color in ['#4a6b5d', '#c2593f', '#2f4858', '#8c6d46', '#5b5377', '#3a6073'] else '#4a6b5d'
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        flash('Conta criada com sucesso.', 'success')
        return redirect(url_for('index'))
        
    return render_template('auth.html', mode='register')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sessão encerrada com sucesso.', 'info')
    return redirect(url_for('index'))

# ----------------- PERFIL E BUSCA DE USUARIOS -----------------

@app.route('/perfil', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        bio = request.form.get('bio', '').strip()
        avatar_color = request.form.get('avatar_color', '#4a6b5d').strip()
        
        current_user.bio = bio[:500]
        if avatar_color in ['#4a6b5d', '#c2593f', '#2f4858', '#8c6d46', '#5b5377', '#3a6073']:
            current_user.avatar_color = avatar_color
            
        db.session.commit()
        flash('Perfil atualizado com sucesso.', 'success')
        return redirect(url_for('profile'))
        
    return render_template('profile.html', user=current_user)

@app.route('/perfil/<int:user_id>')
def view_user_profile(user_id):
    user = db.session.get(User, user_id)
    if not user:
        abort(404)
    return render_template('user_profile.html', user=user)

@app.route('/busca')
def search_users():
    query = request.args.get('q', '').strip()
    users = []
    if query:
        users = User.query.filter(User.username.ilike(f'%{query}%')).limit(30).all()
    return render_template('search.html', query=query, users=users)

# ----------------- FORUM -----------------

@app.route('/forum')
def forum_list():
    rooms = ForumRoom.query.order_by(ForumRoom.created_at.desc()).all()
    return render_template('forum.html', rooms=rooms, active_room=None, messages=[])

@app.route('/forum/<int:room_id>')
def forum_room(room_id):
    room = db.session.get(ForumRoom, room_id)
    if not room:
        abort(404)
    rooms = ForumRoom.query.order_by(ForumRoom.created_at.desc()).all()
    messages = room.messages.order_by(ForumMessage.created_at.asc()).limit(150).all()
    return render_template('forum.html', rooms=rooms, active_room=room, messages=messages)

@app.route('/forum/nova-sala', methods=['POST'])
@login_required
def create_room():
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    
    if not name:
        flash('O nome da sala é obrigatório.', 'danger')
        return redirect(url_for('forum_list'))
        
    if ForumRoom.query.filter_by(name=name).first():
        flash('Já existe uma sala com esse nome.', 'warning')
        return redirect(url_for('forum_list'))
        
    new_room = ForumRoom(
        name=name[:100],
        description=description[:255],
        created_by_id=current_user.id
    )
    db.session.add(new_room)
    db.session.commit()
    flash('Sala de discussão criada com sucesso.', 'success')
    return redirect(url_for('forum_room', room_id=new_room.id))

# ----------------- CHAT PRIVADO 1:1 -----------------

@app.route('/chat/privado/<int:recipient_id>')
@login_required
def private_chat(recipient_id):
    if recipient_id == current_user.id:
        flash('Não é possível abrir um chat privado consigo mesmo.', 'info')
        return redirect(url_for('search_users'))
        
    recipient = db.session.get(User, recipient_id)
    if not recipient:
        abort(404)
        
    messages = PrivateMessage.query.filter(
        ((PrivateMessage.sender_id == current_user.id) & (PrivateMessage.recipient_id == recipient_id)) |
        ((PrivateMessage.sender_id == recipient_id) & (PrivateMessage.recipient_id == current_user.id))
    ).order_by(PrivateMessage.created_at.asc()).limit(200).all()
    
    room_name = f'private_{min(current_user.id, recipient_id)}_{max(current_user.id, recipient_id)}'
    
    return render_template('private_chat.html', recipient=recipient, messages=messages, room_name=room_name)

# ----------------- CHATBOT -----------------

@app.route('/chatbot')
def chatbot_page():
    return render_template('chatbot.html', topics=CHATBOT_TOPICS)

@app.route('/api/chatbot', methods=['POST'])
def chatbot_api():
    data = request.get_json(silent=True) or {}
    topic_or_query = data.get('topic') or data.get('query') or ''
    result = get_response(topic_or_query)
    return jsonify(result)

# ----------------- SOCKETIO EVENT HANDLERS -----------------

@socketio.on('join_forum')
def handle_join_forum(data):
    room_id = data.get('room_id')
    if room_id:
        room_name = f'forum_{room_id}'
        join_room(room_name)

@socketio.on('leave_forum')
def handle_leave_forum(data):
    room_id = data.get('room_id')
    if room_id:
        room_name = f'forum_{room_id}'
        leave_room(room_name)

@socketio.on('send_forum_message')
def handle_forum_message(data):
    if not current_user.is_authenticated:
        emit('error_message', {'error': 'Usuário não autenticado.'})
        return
        
    room_id = data.get('room_id')
    raw_content = data.get('content', '').strip()
    
    if not room_id or not raw_content:
        return
        
    if contains_image_content(raw_content):
        emit('error_message', {'error': 'Envio de imagens ou links de imagens é proibido nas mensagens.'})
        return
        
    clean_content = sanitize_message(raw_content)
    if not clean_content or len(clean_content) > 2000:
        return
        
    room = db.session.get(ForumRoom, room_id)
    if not room:
        return
        
    message = ForumMessage(
        room_id=room_id,
        user_id=current_user.id,
        content=clean_content
    )
    db.session.add(message)
    db.session.commit()
    
    payload = message.to_dict()
    emit('new_forum_message', payload, room=f'forum_{room_id}')

@socketio.on('join_private')
def handle_join_private(data):
    if not current_user.is_authenticated:
        return
    room_name = data.get('room_name')
    if room_name and room_name.startswith('private_'):
        parts = room_name.split('_')
        if len(parts) == 3:
            try:
                u1, u2 = int(parts[1]), int(parts[2])
                if current_user.id in (u1, u2):
                    join_room(room_name)
            except ValueError:
                pass

@socketio.on('leave_private')
def handle_leave_private(data):
    room_name = data.get('room_name')
    if room_name:
        leave_room(room_name)

@socketio.on('send_private_message')
def handle_private_message(data):
    if not current_user.is_authenticated:
        emit('error_message', {'error': 'Usuário não autenticado.'})
        return
        
    recipient_id = data.get('recipient_id')
    raw_content = data.get('content', '').strip()
    
    if not recipient_id or not raw_content:
        return
        
    if contains_image_content(raw_content):
        emit('error_message', {'error': 'Envio de imagens ou links de imagens é proibido no chat privado.'})
        return
        
    clean_content = sanitize_message(raw_content)
    if not clean_content or len(clean_content) > 2000:
        return
        
    recipient = db.session.get(User, recipient_id)
    if not recipient:
        return
        
    message = PrivateMessage(
        sender_id=current_user.id,
        recipient_id=recipient_id,
        content=clean_content
    )
    db.session.add(message)
    db.session.commit()
    
    room_name = f'private_{min(current_user.id, recipient_id)}_{max(current_user.id, recipient_id)}'
    payload = message.to_dict()
    emit('new_private_message', payload, room=room_name)

# ----------------- INICIALIZACAO DO BANCO E SALAS PADRAO -----------------

def init_db():
    with app.app_context():
        db.create_all()
        
        if ForumRoom.query.count() == 0:
            default_rooms = [
                ('Geral e Acolhimento', 'Espaço aberto para apresentações, dúvidas e relatos sobre neurodivergência.'),
                ('Vida Adulta e Carreira', 'Conversas sobre adaptações no trabalho, autonomia e desafios cotidianos.'),
                ('Educação e Aprendizagem', 'Debates sobre adaptações curriculares, apoio escolar e técnicas de estudo.'),
                ('Rede de Apoio e Famílias', 'Troca de experiências entre pais, cuidadores, parceiros e educadores.')
            ]
            for name, desc in default_rooms:
                room = ForumRoom(name=name, description=desc)
                db.session.add(room)
            db.session.commit()
            print('Banco de dados inicializado com salas padrão.')

init_db()

if __name__ == '__main__':
    socketio.run(app, debug=True, host='127.0.0.1', port=5000)
