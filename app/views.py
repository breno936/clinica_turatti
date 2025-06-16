from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from app import db
from app.models import Consulta, User
from datetime import datetime
from flask_login import logout_user, login_required, login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
import random
import string
from functools import wraps

views_bp = Blueprint('views', __name__)

# ================= DECORADORES =================

def role_required(*roles):
    def check_role(f):
        @wraps(f)
        def wrapper_check_user_role(*args, **kwargs):
            if current_user.role not in roles:
                abort(403)
            return f(*args, **kwargs)
        return wrapper_check_user_role
    return check_role

# ================= LOGIN / LOGOUT =================

@views_bp.route('/cadastro_medico', methods=['GET', 'POST'])
@login_required
@role_required('admin')  # Somente administradores podem cadastrar médicos
def cadastro_medico():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('As senhas não coincidem.', 'danger')
            return redirect(url_for('views.cadastro_medico'))

        if User.query.filter_by(email=email).first():
            flash('E-mail já cadastrado.', 'danger')
            return redirect(url_for('views.cadastro_medico'))

        hashed_password = generate_password_hash(password)
        novo_medico = User(email=email, password=hashed_password, role='medico')
        db.session.add(novo_medico)
        db.session.commit()

        flash('Médico cadastrado com sucesso!', 'success')
        return redirect(url_for('views.home'))

    return render_template('cadastro_medico.html')

@views_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            # Redirecionamento por perfil
            if user.role == 'medico':
                return redirect(url_for('views.home'))
            elif user.role == 'paciente':
                return redirect(url_for('views.home'))
            else:
                return redirect(url_for('views.home'))
        else:
            flash('Login inválido. Tente novamente.', 'danger')
            return redirect(url_for('views.login'))

    return render_template('login.html')


@views_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.login'))

# ================= PÁGINA INICIAL =================

@views_bp.route('/')
@login_required
def home():
    return render_template('index.html')

# ================= CONSULTAS =================

@views_bp.route('/agendar', methods=['GET', 'POST'])
@login_required
@role_required('paciente', 'admin')
def agendar():
    medicos = User.query.filter_by(role='medico').all()

    if request.method == 'POST':
        data_hora = request.form['data_hora']
        medico_id = request.form['medico_id']
        paciente_id = current_user.id

        try:
            data_hora = datetime.strptime(data_hora, '%Y-%m-%dT%H:%M')
        except ValueError:
            return "Data e hora inválidas. Use o formato: YYYY-MM-DD HH:MM", 400

        consulta = Consulta(data_hora=data_hora, paciente_id=paciente_id, medico_id=medico_id)
        db.session.add(consulta)
        db.session.commit()

        flash('Consulta agendada com sucesso!', 'success')
        return redirect(url_for('views.lista'))

    return render_template('agendar.html', medicos=medicos)

@views_bp.route('/consultas')
@login_required
def lista():
    if current_user.role == 'admin':
        consultas = Consulta.query.all()
    elif current_user.role == 'medico':
        consultas = Consulta.query.filter_by(medico_id=current_user.id).all()
    else:
        consultas = Consulta.query.filter_by(paciente_id=current_user.id).all()

    return render_template('consultas.html', consultas=consultas)

@views_bp.route('/aceitar_consulta/<int:consulta_id>', methods=['POST'])
@login_required
@role_required('medico')
def aceitar_consulta(consulta_id):
    consulta = Consulta.query.get_or_404(consulta_id)
    consulta.status = 'aceita'
    db.session.commit()
    flash('Consulta aceita com sucesso!', 'success')
    return redirect(url_for('views.lista'))

@views_bp.route('/recusar_consulta/<int:consulta_id>', methods=['POST'])
@login_required
@role_required('medico')
def recusar_consulta(consulta_id):
    consulta = Consulta.query.get_or_404(consulta_id)
    consulta.status = 'recusada'
    db.session.commit()
    flash('Consulta recusada.', 'danger')
    return redirect(url_for('views.lista'))

# ================= RECUPERAÇÃO DE SENHA =================

@views_bp.route('/recuperar_senha', methods=['GET', 'POST'])
def recuperar_senha():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()

        if user:
            token = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
            reset_link = url_for('views.resetar_senha', token=token, _external=True)

            msg = Message('Redefinição de Senha', recipients=[email])
            msg.body = f'Clique no link para redefinir sua senha: {reset_link}'
            mail.send(msg)

            flash('E-mail enviado! Verifique sua caixa de entrada.', 'success')
            return redirect(url_for('views.login'))
        else:
            flash('E-mail não encontrado!', 'danger')

    return render_template('recuperar_senha.html')

@views_bp.route('/resetar_senha/<token>', methods=['GET', 'POST'])
def resetar_senha(token):
    if request.method == 'POST':
        nova_senha = request.form['nova_senha']
        confirmacao_senha = request.form['confirmacao_senha']

        if nova_senha != confirmacao_senha:
            flash('As senhas não coincidem', 'danger')
            return redirect(url_for('views.resetar_senha', token=token))

        user = User.query.first()  # Aqui deve validar o token real

        if user:
            user.password = generate_password_hash(nova_senha)
            db.session.commit()
            flash('Senha redefinida com sucesso', 'success')
            return redirect(url_for('views.login'))

    return render_template('resetar_senha.html')

# ================= CADASTRO =================

@views_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form.get('role', 'paciente')

        if password != confirm_password:
            flash('As senhas não coincidem.', 'danger')
            return redirect(url_for('views.cadastro'))

        if User.query.filter_by(email=email).first():
            flash('E-mail já cadastrado', 'danger')
            return redirect(url_for('views.cadastro'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(email=email, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('views.login'))

    return render_template('cadastro.html')
