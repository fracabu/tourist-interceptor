import re
from models import db, Contact

def parse_contacts_from_md(filepath='dati.md'):
    """Parse del file dati.md e importazione nel database"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    contacts_data = []

    # Lista delle organizzazioni principali
    organizations = [
        {
            'name': 'POLICLINICO GEMELLI ROMA - CENTRO CONGRESSI EUROPA',
            'contacts': [
                {'name': 'Francesco Gemelli', 'role': 'Responsabile Formazione Permanente, ECM, Convegni', 'email': 'formazione.permanente-rm@unicatt.it', 'phone': '+39 06 30154886', 'linkedin': 'https://it.linkedin.com/in/francesco-gemelli-0a225792'},
                {'name': 'Simonetta Salomone', 'role': 'Formazione Permanente, ECM, Convegni', 'email': 'simonetta.salomone@unicatt.it', 'phone': '06 30154886'},
                {'name': 'Valeria Polimeni', 'role': 'Formazione Permanente, ECM, Convegni', 'email': 'valeria.polimeni@unicatt.it', 'phone': '06 30154886'},
                {'name': 'Maria Grazia Chierchia', 'role': 'Formazione Permanente, ECM, Convegni', 'email': 'mariagrazia.chierchia@unicatt.it', 'phone': '06 30154886'},
            ],
            'address': 'Largo Francesco Vito, 1 - 00168 Roma',
            'tier': 1,
            'notes': 'Centro Congressi gestito dall\'Università Cattolica. Auditorium 500 posti, sale eventi fino a 850 persone. Specializzato congressi medico-scientifici.'
        },
        {
            'name': 'CONSIGLIO NAZIONALE DEL NOTARIATO - N SERVIZI SRL',
            'contacts': [
                {'name': 'Claudia Franceschini', 'role': 'Direttore Generale N Servizi S.r.l.', 'email': 'segreteriaeventi@nservizi.it', 'phone': '+39 06 36209418'},
                {'name': 'Enrico Parenti', 'role': 'Amministratore Unico N Servizi S.r.l.', 'email': 'segreteriaeventi@nservizi.it'},
                {'name': 'Erika Attili', 'role': 'Segreteria Eventi', 'email': 'segreteriaeventi@nservizi.it'},
            ],
            'address': 'Via Flaminia, 160 - 00196 Roma',
            'tier': 2,
            'notes': 'Società specializzata del notariato per congressi. Certificata ISO 9001. Gestisce 20+ eventi formativi annui. Provider ECM.'
        },
        {
            'name': 'CONVENTION BUREAU ROMA E LAZIO (CBReL)',
            'contacts': [
                {'name': 'Monica Conti', 'role': 'Bureau Manager', 'email': 'monica@cbromaelazio.it', 'phone': '+39 377 5523813', 'linkedin': 'https://it.linkedin.com/in/monica-conti-2964384'},
                {'name': 'Massimo Morale', 'role': 'Sales & Marketing Manager / Business Development', 'email': 'massimo@cbromaelazio.it', 'phone': '+39 377 5523813', 'linkedin': 'https://www.linkedin.com/in/massimo-morale-40234413/'},
                {'name': 'Camilla Collina', 'role': 'Operations Manager', 'email': 'camilla@cbromaelazio.it', 'linkedin': 'https://www.linkedin.com/in/camilla-collina-a4b34118/'},
                {'name': 'Edoardo Siliquini', 'role': 'Communication Manager', 'email': 'edoardo@cbromaelazio.it'},
            ],
            'address': 'Via Flaminia, 388 - 00196 Roma',
            'tier': 1,
            'notes': 'Organismo ufficiale promozione MICE Roma e Lazio. Network 150+ player turismo regionale. PRIORITÀ MASSIMA.'
        },
        {
            'name': 'AUDITORIUM PARCO DELLA MUSICA / FONDAZIONE MUSICA PER ROMA',
            'contacts': [
                {'name': 'Ufficio Commerciale Eventi Corporate', 'role': 'Commerciale Eventi', 'email': 'commerciale@musicaperroma.it', 'phone': '+39 0680241281'},
            ],
            'address': 'Viale Pietro de Coubertin 30, 00196 Roma',
            'tier': 2,
            'notes': 'Oltre 1 milione spettatori/anno. Chiamare infoline per referente diretto nominativo.'
        },
        {
            'name': 'SAPIENZA UNIVERSITÀ ROMA - CENTRO CONGRESSI',
            'contacts': [
                {'name': 'Prof. Tito Marci', 'role': 'Delegato Rettrice per gestione Centro Congressi', 'email': 'tito.marci@uniroma1.it', 'phone': '+39 06 49911', 'linkedin': 'https://www.linkedin.com/in/tito-marci-369b315a/'},
                {'name': 'Valerio Irano', 'role': 'Responsabile Tecnico Centro Congressi', 'email': 'valerio.irano@uniroma1.it', 'phone': '06 49918489'},
            ],
            'address': 'Via Salaria 113, 00198 Roma',
            'tier': 2,
            'notes': 'Istanze utilizzo Centro Congressi almeno 15 giorni lavorativi prima evento.'
        },
        {
            'name': 'BALESTRA SRL CONGRESSI',
            'contacts': [
                {'name': 'Sabina Marra', 'role': 'Manager/Responsabile Segreteria Organizzativa', 'email': 'info@balestrasrl.com', 'phone': '+39 06 214 8065', 'linkedin': 'https://www.linkedin.com/in/sabina-marra-24119132/'},
            ],
            'address': 'Piazza Roberto Malatesta 16, 00176 Roma',
            'tier': 2,
            'notes': 'PCO dal 1983. Provider ECM. Specializzata congressi scientifici, eventi fino a 5.000 partecipanti. Cell assistenza: +39 339 8319858'
        },
        {
            'name': 'ROMA CONVENTION CENTER LA NUVOLA',
            'contacts': [
                {'name': 'Francesca Maralli', 'role': 'Sales and Marketing Manager', 'email': 'f.maralli@romaeur.it', 'phone': '+39 06 5451 3710', 'linkedin': 'https://it.linkedin.com/in/francesca-maralli-8005811'},
                {'name': 'Lucia Ceddia', 'role': 'Sales Marketing Department', 'email': 'info@romaconventiongroup.it'},
            ],
            'address': 'Viale della Pittura, 50 - 00144 Roma',
            'tier': 1,
            'notes': 'Gestisce La Nuvola e Palazzo dei Congressi. Contatto commerciale diretto prioritario.'
        },
        {
            'name': 'FEDERCONGRESSI&EVENTI',
            'contacts': [
                {'name': 'Maria Gabriella Gentile', 'role': 'Presidente (mandato 2025-2028)', 'email': 'federcongressi@federcongressi.it'},
                {'name': 'Alessia Tosti', 'role': 'Responsabile Comunicazione ed Eventi', 'email': 'alessiatosti@federcongressi.it'},
                {'name': 'Ilaria Pedroni', 'role': 'Responsabile Segreteria e Rapporti Organi Associativi', 'email': 'ilariapedroni@federcongressi.it'},
                {'name': 'Silvia Perigli', 'role': 'Segreteria Generale', 'email': 'silviaperigli@federcongressi.it'},
            ],
            'address': 'Via dei Cestari 34, 00186 Roma',
            'tier': 2,
            'notes': 'Presidente dal 2022. Socia fondatrice Meeting Consultants Bologna. Twitter: @gentile_gabri'
        },
        {
            'name': 'LEADER SRL (FareTurismo)',
            'contacts': [
                {'name': 'Ugo Picarelli', 'role': 'Fondatore e Direttore', 'email': 'eventi@leaderonline.it', 'phone': '+39 089 253170', 'linkedin': 'https://www.linkedin.com/in/ugo-picarelli-31956b157/'},
            ],
            'address': 'Via Roma, 226 - 84121 Salerno',
            'tier': 3,
            'notes': 'Organizza FareTurismo (24 edizioni). Anche BMTA e HospitalitySud. Coordinatore Osservatorio Parlamentare Turismo.'
        },
        {
            'name': 'DBINFORMATION (Rivista Parts - Parts Aftermarket Congress)',
            'contacts': [
                {'name': 'Maria Ranieri', 'role': 'Direttore Area Automotive', 'email': 'eventi.automotive@dbinformation.it', 'linkedin': 'https://it.linkedin.com/in/maria-ranieri-74b43a83'},
            ],
            'address': '',
            'tier': 3,
            'notes': 'Content company B2B eventi automotive. Organizza Parts Aftermarket Congress (21 edizioni, 600+ partecipanti annui).'
        },
    ]

    # Creazione contatti nel database
    for org in organizations:
        org_name = org['name']
        org_address = org.get('address', '')
        org_tier = org.get('tier', 2)
        org_notes = org.get('notes', '')

        for contact_info in org['contacts']:
            contact = Contact(
                organization_name=org_name,
                contact_name=contact_info.get('name', ''),
                role=contact_info.get('role', ''),
                email=contact_info.get('email', ''),
                phone=contact_info.get('phone', ''),
                linkedin=contact_info.get('linkedin', ''),
                address=org_address,
                notes=org_notes,
                tier=org_tier,
                status='Freddo',  # Tutti iniziano come "Freddo"
                priority_score=0
            )
            db.session.add(contact)

    try:
        db.session.commit()
        print(f"[OK] Importati con successo i contatti dal file {filepath}")
        return True
    except Exception as e:
        db.session.rollback()
        print(f"[ERRORE] Errore durante l'importazione: {e}")
        return False


def calculate_priority_score(contact):
    """Calcola lo score di priorità basato sui criteri del documento"""
    # Formula semplificata: score base su tier
    tier_score = {1: 30, 2: 20, 3: 10}
    score = tier_score.get(contact.tier, 10)

    # Bonus se ha email diretta
    if contact.email and '@' in contact.email:
        score += 5

    # Bonus se ha telefono
    if contact.phone:
        score += 5

    # Bonus se ha LinkedIn
    if contact.linkedin:
        score += 3

    return score
