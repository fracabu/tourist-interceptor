from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, Contact, Interaction, Event
from parser import parse_contacts_from_md, calculate_priority_score
from email_generator import generate_email
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tourist-interceptor-secret-key-2025'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/')
def index():
    """Dashboard principale"""
    total_contacts = Contact.query.count()

    # Statistiche per status
    status_stats = {}
    for status in ['Freddo', 'Tiepido', 'Caldo', 'Cliente', 'Partner']:
        status_stats[status] = Contact.query.filter_by(status=status).count()

    # Contatti da seguire oggi
    today = datetime.now().date()
    contacts_to_follow = Contact.query.filter(
        Contact.next_action_date <= datetime.now()
    ).order_by(Contact.next_action_date).limit(5).all()

    # Ultimi 5 contatti aggiunti
    recent_contacts = Contact.query.order_by(Contact.created_at.desc()).limit(5).all()

    # Statistiche per tier
    tier_stats = {}
    for tier in [1, 2, 3]:
        tier_stats[tier] = Contact.query.filter_by(tier=tier).count()

    return render_template('index.html',
                         total_contacts=total_contacts,
                         status_stats=status_stats,
                         tier_stats=tier_stats,
                         contacts_to_follow=contacts_to_follow,
                         recent_contacts=recent_contacts)


@app.route('/contacts')
def contacts():
    """Lista tutti i contatti con filtri"""
    # Filtri
    tier_filter = request.args.get('tier', type=int)
    status_filter = request.args.get('status')
    search = request.args.get('search', '')

    query = Contact.query

    if tier_filter:
        query = query.filter_by(tier=tier_filter)

    if status_filter:
        query = query.filter_by(status=status_filter)

    if search:
        query = query.filter(
            (Contact.organization_name.ilike(f'%{search}%')) |
            (Contact.contact_name.ilike(f'%{search}%')) |
            (Contact.email.ilike(f'%{search}%'))
        )

    contacts_list = query.order_by(Contact.tier, Contact.organization_name).all()

    return render_template('contacts.html', contacts=contacts_list)


@app.route('/contact/<int:contact_id>')
def contact_detail(contact_id):
    """Dettaglio singolo contatto"""
    contact = Contact.query.get_or_404(contact_id)
    interactions = Interaction.query.filter_by(contact_id=contact_id).order_by(Interaction.interaction_date.desc()).all()

    return render_template('contact_detail.html', contact=contact, interactions=interactions)


@app.route('/contact/<int:contact_id>/edit', methods=['GET', 'POST'])
def edit_contact(contact_id):
    """Modifica contatto"""
    contact = Contact.query.get_or_404(contact_id)

    if request.method == 'POST':
        contact.organization_name = request.form.get('organization_name')
        contact.contact_name = request.form.get('contact_name')
        contact.role = request.form.get('role')
        contact.email = request.form.get('email')
        contact.phone = request.form.get('phone')
        contact.linkedin = request.form.get('linkedin')
        contact.address = request.form.get('address')
        contact.notes = request.form.get('notes')
        contact.tier = int(request.form.get('tier', 2))
        contact.status = request.form.get('status', 'Freddo')

        # Next action
        next_action_date_str = request.form.get('next_action_date')
        if next_action_date_str:
            contact.next_action_date = datetime.strptime(next_action_date_str, '%Y-%m-%d')
        contact.next_action_description = request.form.get('next_action_description')

        # Ricalcola score
        contact.priority_score = calculate_priority_score(contact)

        db.session.commit()
        flash(f'✅ Contatto {contact.organization_name} aggiornato!', 'success')
        return redirect(url_for('contact_detail', contact_id=contact.id))

    return render_template('edit_contact.html', contact=contact)


@app.route('/contact/<int:contact_id>/add_interaction', methods=['POST'])
def add_interaction(contact_id):
    """Aggiungi interazione a un contatto"""
    contact = Contact.query.get_or_404(contact_id)

    interaction = Interaction(
        contact_id=contact_id,
        interaction_type=request.form.get('interaction_type'),
        notes=request.form.get('notes'),
        outcome=request.form.get('outcome')
    )

    # Aggiorna last_contact_date del contatto
    contact.last_contact_date = datetime.now()

    db.session.add(interaction)
    db.session.commit()

    flash('✅ Interazione aggiunta!', 'success')
    return redirect(url_for('contact_detail', contact_id=contact_id))


@app.route('/contact/new', methods=['GET', 'POST'])
def new_contact():
    """Aggiungi nuovo contatto"""
    if request.method == 'POST':
        contact = Contact(
            organization_name=request.form.get('organization_name'),
            contact_name=request.form.get('contact_name'),
            role=request.form.get('role'),
            email=request.form.get('email'),
            phone=request.form.get('phone'),
            linkedin=request.form.get('linkedin'),
            address=request.form.get('address'),
            notes=request.form.get('notes'),
            tier=int(request.form.get('tier', 2)),
            status=request.form.get('status', 'Freddo')
        )

        contact.priority_score = calculate_priority_score(contact)

        db.session.add(contact)
        db.session.commit()

        flash(f'✅ Nuovo contatto {contact.organization_name} creato!', 'success')
        return redirect(url_for('contact_detail', contact_id=contact.id))

    return render_template('new_contact.html')


@app.route('/contact/<int:contact_id>/generate_email', methods=['GET', 'POST'])
def generate_email_for_contact(contact_id):
    """Genera email personalizzata per un contatto"""
    contact = Contact.query.get_or_404(contact_id)

    if request.method == 'POST':
        template_type = request.form.get('template_type', 'first_contact')
        user_name = request.form.get('user_name', '')
        user_email = request.form.get('user_email', '')
        user_phone = request.form.get('user_phone', '')
        custom_notes = request.form.get('custom_notes', '')

        email_data = generate_email(
            contact=contact,
            template_type=template_type,
            user_name=user_name,
            user_email=user_email,
            user_phone=user_phone,
            custom_notes=custom_notes
        )

        return render_template('email_generated.html',
                             contact=contact,
                             email_data=email_data)

    return render_template('generate_email.html', contact=contact)


@app.route('/events')
def events():
    """Lista eventi"""
    events_list = Event.query.order_by(Event.event_start_date.desc()).all()
    return render_template('events.html', events=events_list)


@app.route('/event/new', methods=['GET', 'POST'])
def new_event():
    """Aggiungi nuovo evento"""
    if request.method == 'POST':
        event = Event(
            event_name=request.form.get('event_name'),
            venue=request.form.get('venue'),
            organizer=request.form.get('organizer'),
            estimated_participants=request.form.get('estimated_participants', type=int),
            event_status=request.form.get('event_status', 'Da contattare'),
            notes=request.form.get('notes'),
            opportunity_value=request.form.get('opportunity_value', type=float, default=0.0),
            probability=request.form.get('probability', type=int, default=10)
        )

        # Date
        start_date_str = request.form.get('event_start_date')
        end_date_str = request.form.get('event_end_date')

        if start_date_str:
            event.event_start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        if end_date_str:
            event.event_end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

        db.session.add(event)
        db.session.commit()

        flash(f'✅ Evento {event.event_name} aggiunto!', 'success')
        return redirect(url_for('events'))

    return render_template('new_event.html')


@app.route('/stats')
def stats():
    """Statistiche avanzate"""
    total_contacts = Contact.query.count()
    total_interactions = Interaction.query.count()
    total_events = Event.query.count()

    # Conversioni
    clienti = Contact.query.filter_by(status='Cliente').count()
    partner = Contact.query.filter_by(status='Partner').count()

    # Pipeline value
    events_list = Event.query.all()
    pipeline_value = sum((e.opportunity_value * e.probability / 100) for e in events_list)

    return render_template('stats.html',
                         total_contacts=total_contacts,
                         total_interactions=total_interactions,
                         total_events=total_events,
                         clienti=clienti,
                         partner=partner,
                         pipeline_value=pipeline_value)


@app.route('/import_contacts')
def import_contacts():
    """Importa contatti da dati.md"""
    if Contact.query.count() > 0:
        flash('⚠️ Database già popolato. Elimina i contatti esistenti prima di re-importare.', 'warning')
        return redirect(url_for('index'))

    success = parse_contacts_from_md('dati.md')

    if success:
        # Ricalcola score per tutti i contatti
        contacts = Contact.query.all()
        for contact in contacts:
            contact.priority_score = calculate_priority_score(contact)
        db.session.commit()

        flash(f'✅ Importati {Contact.query.count()} contatti da dati.md!', 'success')
    else:
        flash('❌ Errore durante l\'importazione', 'error')

    return redirect(url_for('index'))


@app.cli.command()
def init_db():
    """Inizializza il database"""
    db.create_all()
    print("[OK] Database creato!")


@app.cli.command()
def import_data():
    """Importa dati da dati.md"""
    parse_contacts_from_md('dati.md')

    # Ricalcola score
    contacts = Contact.query.all()
    for contact in contacts:
        contact.priority_score = calculate_priority_score(contact)
    db.session.commit()

    print(f"[OK] Importati {Contact.query.count()} contatti!")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='127.0.0.1', port=5000)
