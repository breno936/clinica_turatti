# 🏥 Clínica Online

Sistema completo de agendamento de consultas médicas, desenvolvido com **Python (Flask)** e **Bootstrap 5**. A aplicação permite que pacientes agendem consultas com médicos, que médicos visualizem suas consultas e que administradores cadastrem médicos e acompanhem os agendamentos.

---

## 💡 Sobre o Projeto

O sistema foi desenvolvido com foco em **simplicidade, usabilidade e organização**, permitindo:

- 👨‍⚕️ Cadastro de médicos e pacientes  
- 📅 Agendamento de consultas por pacientes  
- 🩺 Visualização de consultas pelos médicos  
- 🧑‍💻 Área de login com autenticação  
- 🔐 Redefinição de senha via e-mail e dentro do sistema  
- 🎨 Interface moderna e responsiva com Bootstrap  

---

## 🚀 Como Rodar o Projeto (Passo a Passo)

> 📝 **Pré-requisitos:**
> - Python 3 instalado (recomenda-se 3.9 ou superior)
> - Git (opcional, mas recomendado)
> - Ambiente virtual configurado (veja abaixo)

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/clinica-online.git
cd clinica-online
```
###2. Crie e ative o ambiente virtual
bash
Copiar
Editar
python -m venv venv
Ativar no Windows:

bash
Copiar
Editar
venv\Scripts\activate
Ativar no Linux/macOS:

bash
Copiar
Editar
source venv/bin/activate

###3. Instale as dependências
bash
Copiar
Editar
pip install -r requirements.txt
Se não tiver o requirements.txt, instale manualmente:

bash
Copiar
Editar
pip install flask flask_sqlalchemy flask_login flask_mail

###4. Configure o ambiente
Crie um arquivo .env (ou edite diretamente o app/__init__.py) com suas configurações de e-mail, por exemplo:

python
Copiar
Editar
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'seuemail@gmail.com'
app.config['MAIL_PASSWORD'] = 'sua_senha_de_app'
💡 Para usar e-mail com Gmail, ative a autenticação em dois fatores e gere uma senha de app.

###5. Rode o projeto
bash
Copiar
Editar
flask run
Acesse no navegador: http://localhost:5000

👥 Perfis de Usuário
Paciente

Pode se cadastrar

Pode agendar consultas com médicos

Pode visualizar suas próprias consultas

Médico

Deve ser cadastrado por um administrador

Visualiza somente consultas agendadas para ele

Não pode agendar consultas

Administrador

Visualiza todas as consultas

Pode cadastrar médicos manualmente (via banco de dados ou interface futura)
