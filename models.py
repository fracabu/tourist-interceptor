from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Contact(db.Model):
    """Modello per i contatti B2B"""
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    organization_name = db.Column(db.String(200), nullable=False)
    contact_name = db.Column(db.String(200))
    role = db.Column(db.String(200))
    email = db.Column(db.String(200))
    phone = db.Column(db.String(100))
    linkedin = db.Column(db.String(300))
    address = db.Column(db.String(300))
    notes = db.Column(db.Text)

    # Classificazione
    tier = db.Column(db.Integer, default=2)  # 1=Alta priorità, 2=Media, 3=Bassa
    status = db.Column(db.String(50), default='Freddo')  # Freddo, Tiepido, Caldo, Cliente, Partner
    priority_score = db.Column(db.Integer, default=0)

    # Date tracking
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_contact_date = db.Column(db.DateTime)
    next_action_date = db.Column(db.DateTime)
    next_action_description = db.Column(db.String(500))

    # Relazioni
    interactions = db.relationship('Interaction', backref='contact', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Contact {self.organization_name}>'


class Interaction(db.Model):
    """Storico interazioni con i contatti"""
    __tablename__ = 'interactions'

    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=False)
    interaction_date = db.Column(db.DateTime, default=datetime.utcnow)
    interaction_type = db.Column(db.String(100))  # Email, Telefono, LinkedIn, Persona
    notes = db.Column(db.Text)
    outcome = db.Column(db.String(200))  # Esito dell'interazione

    def __repr__(self):
        return f'<Interaction {self.interaction_type} - {self.interaction_date}>'


class Event(db.Model):
    """Eventi da monitorare"""
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(300), nullable=False)
    event_start_date = db.Column(db.DateTime)
    event_end_date = db.Column(db.DateTime)
    venue = db.Column(db.String(300))
    organizer = db.Column(db.String(300))
    estimated_participants = db.Column(db.Integer)
    event_status = db.Column(db.String(100), default='Da contattare')  # Da contattare, Contattato, Preventivo inviato, etc.
    notes = db.Column(db.Text)
    opportunity_value = db.Column(db.Float, default=0.0)
    probability = db.Column(db.Integer, default=10)  # 10-100%

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Event {self.event_name}>'
