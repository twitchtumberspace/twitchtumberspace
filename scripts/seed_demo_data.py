from app.db.session import SessionLocal
from app.services.seed import seed_demo_data


if __name__ == '__main__':
    with SessionLocal() as session:
        seed_demo_data(session)
        print('Demo-Daten importiert.')
