# 🏥 Sistema de Gestão de Clínica Médica

Sistema web para gerenciamento de clínicas médicas desenvolvido com Django, incluindo controle de médicos, pacientes, consultas e dashboard analítico com gráficos em tempo real.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Django](https://img.shields.io/badge/Django-6.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 Funcionalidades

- ✅ **Gestão de Médicos**: Cadastro com CRM, especialidade e controle de consultas
- ✅ **Gestão de Pacientes**: Registro completo com CPF, telefone, e-mail e histórico
- ✅ **Agendamento de Consultas**: Controle de data, horário, valor e informações clínicas
- ✅ **Dashboard Analítico**: 
  - 7 KPIs (faturamento, ticket médio, consultas, etc.)
  - 5 gráficos interativos (Chart.js)
  - Análise por período, médico e especialidade
- ✅ **Interface Administrativa**: Painel customizado com Django Jazzmin

## 🚀 Tecnologias Utilizadas

- **Backend**: Python 3.13 + Django 6.0
- **Banco de Dados**: SQLite (dev) / PostgreSQL (produção)
- **Frontend Admin**: Django Jazzmin + Chart.js
- **Deploy**: Docker Compose

## 📦 Instalação e Execução

### Opção 1: Ambiente Local
```bash
# Clone o repositório
git clone https://github.com/seu-usuario/clinica_medica.git
cd clinica_medica

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Execute as migrações
python manage.py migrate

# Crie um superusuário
python manage.py createsuperuser

# (Opcional) Popule o banco com dados fictícios
python popular_banco.py

# Inicie o servidor
python manage.py runserver
```

Acesse: `http://localhost:8000/admin`

### Opção 2: Docker Compose
```bash
# Suba o container
docker-compose up

# Em outro terminal, execute as migrações
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python popular_banco.py
```

Acesse: `http://localhost:8080/admin`

## 📊 Estrutura do Projeto
```
clinica_medica/
├── core/                   # Configurações do projeto Django
│   ├── settings.py        # Configurações principais
│   └── urls.py            # Rotas principais
├── core_clinica/          # App principal
│   ├── models.py          # Modelos (Medico, Paciente, Consulta)
│   ├── admin.py           # Customização do Django Admin
│   ├── views.py           # API para dashboard
│   ├── reports.py         # Funções de relatórios
│   └── templates/         # Templates HTML customizados
├── popular_banco.py       # Script para dados fictícios
├── docker-compose.yml     # Configuração Docker
└── requirements.txt       # Dependências Python
```

## 🎯 Modelos de Dados

### Médico
- Nome, CRM (único), Especialidade
- Relacionamento: Um médico tem várias consultas

### Paciente
- Nome, CPF (único), Telefone, E-mail, Data de Nascimento
- Relacionamento: Um paciente tem várias consultas

### Consulta
- Paciente, Médico, Data, Horário, Valor
- Campos clínicos: Observações, Diagnóstico, Prescrição
- Ordenação: Data e horário decrescentes

## 📈 Dashboard - Indicadores Disponíveis

**KPIs:**
- Faturamento Total
- Faturamento do Mês
- Ticket Médio
- Total de Consultas (mês e geral)
- Total de Pacientes e Médicos

**Gráficos:**
1. Faturamento diário (últimos 30 dias) - Linha
2. Consultas por especialidade - Rosca
3. Faturamento por médico - Barras horizontais
4. Top 5 pacientes por gasto - Barras
5. Faturamento mensal - Barras + Linha

## 🔐 Segurança (Próximos Passos)

- [ ] Migrar `SECRET_KEY` para variável de ambiente
- [ ] Configurar `DEBUG=False` em produção
- [ ] Implementar autenticação JWT para API
- [ ] Adicionar validação de CPF/CRM únicos
- [ ] Configurar HTTPS no deploy

## 🧪 Testes (Em Desenvolvimento)
```bash
python manage.py test core_clinica
```

## 📝 Melhorias Futuras

- [ ] Exportação de relatórios em PDF
- [ ] Sistema de notificações por e-mail
- [ ] API REST com Django Rest Framework
- [ ] Filtros avançados no dashboard
- [ ] Agendamento online para pacientes
- [ ] Integração com sistema de pagamentos

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

---

⭐ Se este projeto foi útil, deixe uma estrela!
