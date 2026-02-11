import os
import django
import random
from datetime import datetime, timedelta

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from core_clinica.models import Medico, Paciente, Consulta

def popular():
    print("🚀 Gerando dados fictícios atualizados...")
    
    # Criar Médicos
    especialidades = ['Cardiologia', 'Dermatologia', 'Pediatria', 'Clínico Geral']
    medicos = []
    for i in range(4):
        m, created = Medico.objects.get_or_create(
            crm=f"CRM-{random.randint(1000, 9999)}",
            defaults={
                'nome': f"Médico {i+1}",
                'especialidade': especialidades[i]
            }
        )
        medicos.append(m)

    # Criar Pacientes
    for i in range(10):
        # Gerando uma data de nascimento aleatória
        data_nasc = datetime.now() - timedelta(days=random.randint(7000, 30000))
        
        Paciente.objects.get_or_create(
            cpf=f"{random.randint(100,999)}.{random.randint(100,999)}.{random.randint(100,999)}-{random.randint(10,99)}",
            defaults={
                'nome': f"Paciente {i+1}",
                'data_nascimento': data_nasc.date(),
                'email': f"paciente{i+1}@email.com",
                'telefone': "99999-9999"
            }
        )
    
    pacientes = list(Paciente.objects.all())

    # Criar 50 Consultas
    for _ in range(50):
        p = random.choice(pacientes)
        m = random.choice(medicos)
        data_cons = datetime.now() - timedelta(days=random.randint(0, 30))
        
        Consulta.objects.create(
            paciente=p,
            medico=m,
            data=data_cons.date(),
            horario="14:00",
            valor_consulta=random.uniform(150.0, 500.0)
        )
    print("✅ 50 consultas geradas com sucesso!")

if __name__ == '__main__':
    popular()