"""
Run once to populate the database with sample data.
Usage: python seed.py
"""
from datetime import datetime, timedelta, timezone

from database import SessionLocal, Base, engine
from core.security import hash_password
from models.user import User
from models.feedback import Feedback
from models.video_call import VideoCall
from models.job import Job
from models.training import Training, TrainingEnrollment
from models.assessment import Assessment
from models.career import CareerGoal, CareerMilestone

Base.metadata.create_all(bind=engine)


def seed():
    db = SessionLocal()

    if db.query(User).first():
        print("Database already has data — skipping seed.")
        db.close()
        return

    now = datetime.now(timezone.utc)

    # ── Users ─────────────────────────────────────────────────────────────────

    employee = User(
        email="ana.silva@empresa.com",
        hashed_password=hash_password("senha123"),
        name="Ana Silva",
        user_type="employee",
        department="Engenharia",
        role="Desenvolvedora Frontend",
        accessibility_libras=True,
        accessibility_captions=True,
        preferred_language="pt",
    )

    manager = User(
        email="carlos.souza@empresa.com",
        hashed_password=hash_password("senha123"),
        name="Carlos Souza",
        user_type="employee",
        department="Engenharia",
        role="Tech Lead",
        preferred_language="pt",
    )

    company = User(
        email="rh@empresa.com",
        hashed_password=hash_password("senha123"),
        name="Empresa Inclusiva RH",
        user_type="company",
        company_name="Empresa Inclusiva",
        preferred_language="pt",
    )

    colleague = User(
        email="maria.costa@empresa.com",
        hashed_password=hash_password("senha123"),
        name="Maria Costa",
        user_type="employee",
        department="Design",
        role="UX Designer",
        preferred_language="pt",
    )

    db.add_all([employee, manager, company, colleague])
    db.flush()

    # ── Feedback ──────────────────────────────────────────────────────────────

    db.add_all([
        Feedback(
            author_id=manager.id,
            recipient_id=employee.id,
            feedback_type="positive",
            input_mode="text",
            content="Excelente trabalho na entrega do sprint! Sua atenção aos detalhes de acessibilidade fez toda a diferença.",
            status="read",
            created_at=now - timedelta(days=2),
        ),
        Feedback(
            author_id=colleague.id,
            recipient_id=employee.id,
            feedback_type="recognition",
            input_mode="text",
            content="Obrigada por me ajudar com a integração da API. Você explicou tudo muito bem.",
            status="pending",
            created_at=now - timedelta(days=5),
        ),
        Feedback(
            author_id=employee.id,
            recipient_id=manager.id,
            feedback_type="constructive",
            input_mode="text",
            content="As reuniões de alinhamento poderiam ter uma pauta enviada com antecedência para facilitar a preparação.",
            status="read",
            created_at=now - timedelta(days=7),
        ),
    ])

    # ── Video Calls ───────────────────────────────────────────────────────────

    db.add_all([
        VideoCall(
            created_by_id=manager.id,
            participant_id=employee.id,
            title="1:1 Desenvolvimento de Carreira",
            description="Conversa sobre metas e próximos passos na carreira.",
            scheduled_at=now + timedelta(days=3),
            duration_minutes=45,
            requires_libras=True,
            sign_language="libras",
            status="scheduled",
            created_by_role="manager",
        ),
        VideoCall(
            created_by_id=employee.id,
            participant_id=colleague.id,
            title="Feedback sobre o projeto de design",
            scheduled_at=now + timedelta(days=7),
            duration_minutes=30,
            requires_libras=False,
            status="scheduled",
            created_by_role="employee",
        ),
    ])

    # ── Jobs ──────────────────────────────────────────────────────────────────

    db.add_all([
        Job(
            posted_by_id=company.id,
            title="Desenvolvedora Frontend Sênior",
            department="Engenharia",
            location="São Paulo, SP",
            job_type="full-time",
            work_model="hybrid",
            salary_range="R$ 12.000 – R$ 16.000",
            description="Buscamos uma desenvolvedora frontend sênior para liderar projetos de acessibilidade digital.",
            requirements="React, TypeScript, 5+ anos de experiência, conhecimento em WCAG.",
            is_accessible=True,
            is_internal=True,
        ),
        Job(
            posted_by_id=company.id,
            title="UX Designer Pleno",
            department="Design",
            location="Remoto",
            job_type="full-time",
            work_model="remote",
            salary_range="R$ 8.000 – R$ 11.000",
            description="Designer para criar experiências inclusivas e acessíveis para todos os usuários.",
            requirements="Figma, pesquisa com usuários, portfólio com foco em acessibilidade.",
            is_accessible=True,
            is_internal=False,
        ),
        Job(
            posted_by_id=company.id,
            title="Tech Lead — Plataforma de Dados",
            department="Engenharia",
            location="São Paulo, SP",
            job_type="full-time",
            work_model="hybrid",
            salary_range="R$ 18.000 – R$ 24.000",
            description="Liderar o time de dados responsável pela plataforma analítica da empresa.",
            requirements="Python, Spark, liderança técnica, 7+ anos de experiência.",
            is_accessible=False,
            is_internal=True,
        ),
    ])

    # ── Trainings ─────────────────────────────────────────────────────────────

    t1 = Training(
        created_by_id=company.id,
        title="Comunicação Inclusiva no Trabalho",
        description="Aprenda como se comunicar de forma respeitosa e inclusiva com colegas de diferentes origens e necessidades.",
        category="Diversidade & Inclusão",
        duration_hours=4,
    )
    t2 = Training(
        created_by_id=company.id,
        title="Liderança Empática",
        description="Técnicas para liderar equipes com empatia, escuta ativa e foco no bem-estar.",
        category="Liderança",
        duration_hours=8,
    )
    t3 = Training(
        created_by_id=company.id,
        title="Acessibilidade Digital — WCAG na Prática",
        description="Como aplicar as diretrizes de acessibilidade WCAG 2.1 em produtos digitais.",
        category="Técnico",
        duration_hours=6,
    )
    db.add_all([t1, t2, t3])
    db.flush()

    db.add_all([
        TrainingEnrollment(training_id=t1.id, user_id=employee.id, progress_pct=75),
        TrainingEnrollment(training_id=t3.id, user_id=employee.id, progress_pct=30),
    ])

    # ── Assessments ───────────────────────────────────────────────────────────

    db.add_all([
        Assessment(
            created_by_id=company.id,
            title="Avaliação de Desempenho — Q1 2026",
            description="Autoavaliação de competências técnicas e comportamentais do primeiro trimestre.",
            category="performance",
            due_date=now + timedelta(days=10),
        ),
        Assessment(
            created_by_id=company.id,
            title="Pesquisa de Clima Organizacional",
            description="Avalie o ambiente de trabalho, cultura e práticas de inclusão da empresa.",
            category="culture",
            due_date=now + timedelta(days=20),
        ),
    ])

    # ── Career Goals ──────────────────────────────────────────────────────────

    goal = CareerGoal(
        user_id=employee.id,
        title="Tornar-me Tech Lead até o final de 2026",
        description="Desenvolver habilidades de liderança técnica e gestão de pessoas para assumir um cargo de liderança.",
        target_date=datetime(2026, 12, 31, tzinfo=timezone.utc),
    )
    goal.milestones = [
        CareerMilestone(title="Concluir o treinamento de Liderança Empática", is_completed=False),
        CareerMilestone(title="Liderar um projeto end-to-end", is_completed=False),
        CareerMilestone(title="Fazer mentoria com um Tech Lead atual", is_completed=True,
                        completed_at=now - timedelta(days=15)),
    ]
    db.add(goal)

    db.commit()
    db.close()
    print("✓ Banco populado com sucesso!")
    print("\nContas criadas:")
    print("  Funcionária : ana.silva@empresa.com   / senha123")
    print("  Tech Lead   : carlos.souza@empresa.com / senha123")
    print("  RH (empresa): rh@empresa.com           / senha123")
    print("  Colega      : maria.costa@empresa.com  / senha123")


if __name__ == "__main__":
    seed()
