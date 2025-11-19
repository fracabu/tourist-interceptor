"""
Generatore di email personalizzate per outreach B2B
Basato sulla strategia del documento info.md
"""

def generate_email(contact, template_type, user_name="", user_email="", user_phone="", custom_notes=""):
    """
    Genera email personalizzata in base al contatto e tipo di template

    Args:
        contact: oggetto Contact dal database
        template_type: tipo di email (first_contact, follow_up, quote, partnership)
        user_name: nome del mittente
        user_email: email del mittente
        user_phone: telefono del mittente
        custom_notes: note aggiuntive personalizzate

    Returns:
        dict con 'subject' e 'body'
    """

    # Dati contatto
    contact_name = contact.contact_name or "Gentile responsabile"
    org_name = contact.organization_name
    role = contact.role or ""

    # Determina il tipo di organizzazione per personalizzare
    org_type = _detect_org_type(org_name, role)

    templates = {
        'first_contact': _template_first_contact,
        'follow_up': _template_follow_up,
        'quote_request': _template_quote_request,
        'partnership': _template_partnership,
        'event_specific': _template_event_specific
    }

    generator = templates.get(template_type, _template_first_contact)

    return generator(
        contact_name=contact_name,
        org_name=org_name,
        role=role,
        org_type=org_type,
        user_name=user_name,
        user_email=user_email,
        user_phone=user_phone,
        custom_notes=custom_notes,
        contact=contact
    )


def _detect_org_type(org_name, role):
    """Rileva il tipo di organizzazione per personalizzare il messaggio"""
    org_lower = org_name.lower()
    role_lower = role.lower() if role else ""

    if 'pco' in org_lower or 'congress' in org_lower or 'balestra' in org_lower:
        return 'pco'
    elif 'convention bureau' in org_lower or 'mice' in org_lower:
        return 'convention_bureau'
    elif 'hotel' in org_lower or 'hilton' in org_lower or 'ergife' in org_lower:
        return 'hotel'
    elif 'policlinico' in org_lower or 'gemelli' in org_lower or 'ospedale' in org_lower:
        return 'medical'
    elif 'universit' in org_lower or 'sapienza' in org_lower:
        return 'university'
    elif 'notariato' in org_lower or 'ordine' in org_lower or 'consiglio' in org_lower:
        return 'professional_order'
    elif 'auditorium' in org_lower or 'musica' in org_lower:
        return 'cultural_venue'
    elif 'nuvola' in org_lower or 'fiera' in org_lower:
        return 'convention_center'
    elif 'federcongressi' in org_lower:
        return 'federation'
    else:
        return 'generic'


def _template_first_contact(contact_name, org_name, role, org_type, user_name, user_email, user_phone, custom_notes, contact):
    """Template per primo contatto - cold email professionale"""

    # Personalizzazione oggetto in base al tipo
    subject_variants = {
        'pco': f"Soluzione alloggio premium per relatori - Partnership {org_name}",
        'convention_bureau': f"Opportunità collaborazione MICE - Alloggi premium Roma",
        'hotel': f"Soluzione overflow congressi - Appartamento premium zona {_get_zone(org_name)}",
        'medical': f"Alloggio relatori congressi medici - Soluzione premium",
        'university': f"Hosting visiting professors e relatori - Appartamento premium",
        'professional_order': f"Soluzione alloggio eventi formativi {org_name}",
        'cultural_venue': f"Alloggio artisti e ospiti VIP - Appartamento premium",
        'convention_center': f"Partnership alloggi premium per espositori e relatori",
        'federation': f"Proposta collaborazione settore MICE - Alloggi B2B",
        'generic': f"Soluzione alloggio premium per eventi e congressi"
    }

    subject = subject_variants.get(org_type, subject_variants['generic'])

    # Introduzione personalizzata
    intro_variants = {
        'pco': f"""Mi rivolgo a lei in qualità di {role} di {org_name}, realtà che conosco per l'eccellente lavoro nell'organizzazione di congressi ed eventi.""",

        'convention_bureau': f"""Mi rivolgo a lei come {role} del {org_name}, network di riferimento per il settore MICE nel Lazio.""",

        'hotel': f"""Mi rivolgo a lei per proporre una soluzione complementare ai servizi di {org_name}, particolarmente utile nei periodi di overflow o per ospiti che cercano privacy e spazi abitativi superiori.""",

        'medical': f"""Mi rivolgo a lei in riferimento ai numerosi congressi medico-scientifici che si svolgono presso {org_name}.""",

        'university': f"""Mi rivolgo a lei in riferimento agli eventi scientifici e convegni organizzati da {org_name}.""",

        'professional_order': f"""Mi rivolgo a lei in riferimento agli eventi formativi e convegni organizzati da {org_name}.""",

        'cultural_venue': f"""Mi rivolgo a lei in riferimento agli eventi culturali e corporate ospitati presso {org_name}.""",

        'convention_center': f"""Mi rivolgo a lei come {role} di {org_name}, venue di riferimento per grandi eventi congressuali a Roma.""",

        'federation': f"""Mi rivolgo a lei come {role} di {org_name}, federazione di riferimento per il settore congressuale italiano.""",

        'generic': f"""Mi rivolgo a lei in qualità di {role} di {org_name}."""
    }

    intro = intro_variants.get(org_type, intro_variants['generic'])

    # Value proposition personalizzata
    value_prop_variants = {
        'pco': """Offriamo una soluzione di alloggio premium specificamente pensata per relatori, ospiti VIP e professionisti durante congressi ed eventi:

• Appartamento intero di 50 m² (vs 20-25 m² camera hotel standard)
• Privacy assoluta e spazi separati: living per lavorare, zona notte per riposare
• Posizione strategica Balduina: 100 metri da stazione Appiano FS (Fiumicino Airport Train), 2 fermate metro da San Pietro
• Vicinanza a principali sedi congressuali: Hilton Rome Cavalieri Via Cadlolo (10 min), Policlinico Gemelli (raggiungibile in bici), Auditorium Parco della Musica (15 min)
• Servizi premium inclusi: WiFi veloce per videocall, Netflix, Sky, cucina attrezzata, lavatrice
• Prezzo competitivo: €90-120/notte vs €150-250 hotel 4 stelle zona""",

        'convention_bureau': """Come operatori specializzati nel segmento MICE, proponiamo una soluzione complementare alla vostra offerta di alloggi:

• Appartamento premium 50 m² per professionisti in trasferta congressuale
• Alternativa qualitativa all'hotel tradizionale per chi cerca privacy e spazio
• Posizionamento strategico: Balduina, 100m da Appiano FS, ottimi collegamenti verso tutte le sedi
• Servizi business-ready: WiFi veloce, spazi per lavorare, massima tranquillità zona residenziale
• Disponibilità per partnership su base ricorrente
• Possibilità di inserimento nel vostro network di strutture convenzionate""",

        'hotel': """Proponiamo una collaborazione per situazioni di overflow o per ospiti che cercano soluzioni alternative:

• Appartamento intero premium 50 m² - ideale quando le vostre camere sono sold-out
• Soluzione per ospiti che richiedono privacy superiore (relatori, VIP, piccoli gruppi)
• Posizione: zona Balduina, quartiere residenziale, 100m da stazione Appiano FS, ottimi collegamenti
• Sistema di referral reciproco: vi segnaliamo ospiti quando siamo pieni, voi fate altrettanto
• Possibilità di accordo con piccola commissione per reciproci referral
• Manteniamo elevato standard qualitativo per tutelare la vostra reputazione""",

        'medical': """Offriamo una soluzione di alloggio particolarmente apprezzata da relatori e visiting professors durante congressi medici:

• Appartamento intero 50 m² con privacy totale per preparare presentazioni
• Spazi adeguati per studio e concentrazione pre-congresso
• Vicinanza strategica: raggiungibile in bici da {org_name}
• Tranquillità zona residenziale Balduina - ideale per riposo dopo giornate intense
• Cucina attrezzata per chi ha esigenze alimentari specifiche
• Connessione veloce per videocall e telemedicina
• Prezzo allineato ai budget istituzionali per ospitalità relatori""",

        'university': """Offriamo una soluzione di alloggio dedicata a visiting professors, relatori e ospiti istituzionali:

• Appartamento premium 50 m² con ambiente professionale e confortevole
• Spazi separati: area living per ricevere colleghi, zona notte privata
• Ideale per soggiorni medio-lunghi durante semestri, conferenze, progetti di ricerca
• Connessione internet veloce e affidabile per didattica online
• Zona tranquilla e sicura, quartiere residenziale
• Flessibilità check-in/out per chi arriva da conferenze serali
• Possibilità di convenzione per esigenze ricorrenti""",

        'professional_order': """Offriamo una soluzione di alloggio premium per relatori e partecipanti ai vostri eventi formativi:

• Appartamento intero 50 m² - comfort superiore per professionisti
• Privacy e tranquillità per chi partecipa a corsi intensivi o convegni multi-giornata
• Posizione strategica con ottimi collegamenti verso le principali sedi eventi
• Spazi per studio individuale e revisione materiali formativi
• Ideale per relatori che necessitano concentrazione prima degli interventi
• Prezzo competitivo rispetto agli hotel convenzionati standard
• Disponibilità a tariffe agevolate per eventi ricorrenti""",

        'cultural_venue': """Offriamo una soluzione di alloggio premium per artisti, talent e ospiti VIP:

• Appartamento intero 50 m² con massima privacy e riservatezza
• Ambiente confortevole e silenzioso per riposo pre/post performance
• Vicinanza strategica: da {org_name} facilmente raggiungibile
• Spazi living per piccoli meeting informali o prove
• Servizi entertainment (Netflix, Sky) per relax
• Flessibilità orari check-in/out compatibile con eventi serali
• Quartiere residenziale discreto, lontano da affollamento turistico""",

        'convention_center': """Proponiamo una partnership per offrire ai vostri clienti una soluzione alloggio alternativa:

• Appartamento premium 50 m² per espositori, relatori, organizzatori
• Soluzione complementare agli hotel partner nei periodi di alta occupazione
• Posizione: zona Balduina Roma Nord, collegamento Appiano FS per raggiungere tutte le sedi
• Ideale per soggiorni di 3-5 giorni durante allestimento e svolgimento eventi
• Privacy e spazi superiori rispetto a camere hotel standard
• Possibilità di inserimento nei vostri pacchetti espositori
• Tariffe competitive per accordi su base ricorrente""",

        'federation': """Come operatori del settore alloggi B2B congressuale, proponiamo una collaborazione:

• Soluzione di alloggio premium specializzata sul segmento MICE
• Appartamento 50 m² dedicato a professionisti in trasferta per eventi
• Posizionamento strategico zona Balduina con eccellenti collegamenti (Appiano FS, metro, bus)
• Interesse a entrare nel network di strutture qualificate del settore
• Disponibilità a rispettare standard qualitativi e best practice del settore
• Possibilità di case study per dimostrare efficacia soluzioni alternative all'hotel
• Apertura a partecipazione eventi settore e networking""",

        'generic': """Offriamo una soluzione di alloggio premium per professionisti durante eventi e congressi:

• Appartamento intero di 50 m² con privacy e comfort superiori
• Posizione strategica zona Balduina: 100m da Appiano FS, 2 fermate da San Pietro
• Servizi premium inclusi: WiFi veloce, spazi living/notte separati, cucina attrezzata
• Ideale per relatori, ospiti VIP, partecipanti a congressi multi-giornata
• Prezzo competitivo rispetto a hotel standard
• Flessibilità e personalizzazione servizi"""
    }

    value_prop = value_prop_variants.get(org_type, value_prop_variants['generic'])

    # Call to action personalizzata
    cta_variants = {
        'pco': "Sarei lieto di inviarle maggiori dettagli sulla struttura, tariffe e condizioni per partnership su base ricorrente. Potremmo organizzare un breve call conoscitivo o, se preferisce, un sopralluogo della struttura.",

        'convention_bureau': "Sarei interessato a valutare le modalità per entrare nel vostro network di strutture qualificate. Posso inviarle la scheda tecnica completa e valutare un incontro per discutere forme di collaborazione.",

        'hotel': "Resto a disposizione per illustrarle la proposta in dettaglio e discutere un eventuale accordo di reciproco referral. Posso inviarle foto, dettagli e condizioni economiche.",

        'generic': "Resto a disposizione per inviarle maggiori informazioni sulla struttura, foto, tariffe e per organizzare eventualmente un sopralluogo."
    }

    cta = cta_variants.get(org_type, cta_variants['generic'])

    # Note personalizzate se fornite
    custom_section = f"\n\n{custom_notes}\n" if custom_notes else ""

    # Firma
    signature = f"""Cordiali saluti,

{user_name}
Roma Caput Mundi Apartments
{user_email}
{user_phone}

P.S. La struttura si trova in zona Balduina, quartiere residenziale sicuro e ben collegato. Posso inviarle una brochure dettagliata e testimonianze di ospiti business precedenti.""" if user_name else """Cordiali saluti,

Roma Caput Mundi Apartments"""

    body = f"""Gentile {contact_name},

{intro}

{value_prop}
{custom_section}
{cta}

{signature}"""

    return {
        'subject': subject,
        'body': body
    }


def _template_follow_up(contact_name, org_name, role, org_type, user_name, user_email, user_phone, custom_notes, contact):
    """Template per follow-up dopo primo contatto senza risposta"""

    subject = f"Re: Soluzione alloggio premium - {org_name}"

    body = f"""Gentile {contact_name},

Le scrivo in seguito alla mia email della scorsa settimana riguardante la nostra soluzione di alloggio premium per professionisti durante congressi ed eventi.

Comprendo che i periodi siano intensi e le comunicazioni numerose.

Riepilogando in sintesi la proposta:
• Appartamento intero 50 m² zona Balduina (100m Appiano FS, 2 fermate San Pietro)
• Soluzione ideale per relatori, ospiti VIP, professionisti
• Privacy, spazi superiori e servizi premium a prezzo competitivo
• Vicinanza strategica a Hilton Cavalieri Via Cadlolo, Gemelli, Auditorium, principali sedi congressuali

{custom_notes if custom_notes else ''}

Sarebbe disponibile per una breve chiamata di 10 minuti questa settimana? Posso adattarmi ai suoi orari.

In alternativa, posso semplicemente inviarle materiale informativo senza impegno.

Cordiali saluti,

{user_name}
{user_email}
{user_phone}"""

    return {
        'subject': subject,
        'body': body
    }


def _template_quote_request(contact_name, org_name, role, org_type, user_name, user_email, user_phone, custom_notes, contact):
    """Template per invio preventivo dopo richiesta"""

    subject = f"Preventivo alloggio premium - {org_name}"

    body = f"""Gentile {contact_name},

grazie per l'interesse manifestato nella nostra soluzione di alloggio.

Come da sua richiesta, le invio il preventivo per:

**DETTAGLI STRUTTURA:**
• Tipologia: Appartamento intero premium
• Superficie: 50 m²
• Composizione: Living con divano letto, camera matrimoniale separata, cucina attrezzata, bagno
• Capacità: fino a 4 persone
• Ubicazione: Via Balduina (quartiere Balduina), 00136 Roma
• Distanze strategiche:
  - Stazione Appiano FS: 100 metri (treno diretto Fiumicino Airport + Termini)
  - San Pietro: 2 fermate metro
  - Hilton Rome Cavalieri (Via Cadlolo): 10 minuti
  - Auditorium Parco della Musica: 15 minuti
  - Policlinico Gemelli: raggiungibile in bici

**SERVIZI INCLUSI:**
• WiFi veloce (fibra)
• Netflix, Sky
• Aria condizionata
• Riscaldamento
• Lavatrice
• Cucina completa (frigo, forno, piano cottura, moka, stoviglie)
• Biancheria letto e bagno
• Set cortesia

**TARIFFE:**
• 1-2 notti: €120/notte
• 3-5 notti: €100/notte
• 6+ notti: €90/notte
• Tariffe speciali per partnership ricorrenti o gruppi: da concordare

**CONDIZIONI:**
• Check-in flessibile (concordabile)
• Check-out flessibile (concordabile)
• Pulizia finale inclusa
• Acconto: 30% alla conferma
• Saldo: all'arrivo

{custom_notes if custom_notes else ''}

Resto a disposizione per qualsiasi chiarimento o per organizzare un sopralluogo della struttura.

Cordiali saluti,

{user_name}
{user_email}
{user_phone}"""

    return {
        'subject': subject,
        'body': body
    }


def _template_partnership(contact_name, org_name, role, org_type, user_name, user_email, user_phone, custom_notes, contact):
    """Template per proposta partnership strutturata"""

    subject = f"Proposta partnership alloggi B2B - {org_name}"

    body = f"""Gentile {contact_name},

in seguito ai precedenti contatti e all'interesse reciproco, le propongo una collaborazione strutturata tra {org_name} e Roma Caput Mundi Apartments.

**OBIETTIVO PARTNERSHIP:**
Offrire ai vostri clienti/relatori/partecipanti una soluzione di alloggio premium alternativa all'hotel standard, con vantaggi economici e qualitativi per entrambe le parti.

**PROPOSTA OPERATIVA:**

1. **Convenzione preferenziale:**
   - Tariffe dedicate per vostri referral: €85-95/notte (vs €100-120 pubbliche)
   - Priorità disponibilità per vostri eventi
   - Flessibilità totale su orari check-in/out

2. **Sistema di referral reciproco:**
   - Inseriamo {org_name} come partner consigliato per servizi complementari
   - Voi inserite la nostra struttura tra le soluzioni alloggio consigliate
   - Commissione su prenotazioni generate: da concordare (proposta 10%)

3. **Materiali e comunicazione:**
   - Vi forniamo materiale fotografico e descrittivo professionale
   - Possibilità di citazione reciproca su siti web e materiali promozionali
   - Testimonianze e referenze condivise

4. **Supporto operativo:**
   - Referente dedicato per gestione prenotazioni partnership
   - Report periodici su utilizzo e feedback ospiti
   - Disponibilità a sopralluoghi per vostri clienti

{custom_notes if custom_notes else ''}

Sarebbe disponibile per un incontro per discutere i dettagli e formalizzare l'accordo?

Resto in attesa di un suo riscontro.

Cordiali saluti,

{user_name}
{user_email}
{user_phone}"""

    return {
        'subject': subject,
        'body': body
    }


def _template_event_specific(contact_name, org_name, role, org_type, user_name, user_email, user_phone, custom_notes, contact):
    """Template per proposta legata a evento specifico"""

    subject = f"Soluzione alloggio relatori per [NOME EVENTO]"

    body = f"""Gentile {contact_name},

ho notato che {org_name} sta organizzando [NOME EVENTO] in data [DATE EVENTO].

Le scrivo per proporle una soluzione di alloggio dedicata ai vostri relatori e ospiti VIP.

**PROPOSTA PER [NOME EVENTO]:**

• Appartamento intero premium 50 m² disponibile per le date dell'evento
• Ideale per 1-2 relatori che necessitano privacy e spazi per preparare interventi
• Posizione strategica con collegamento diretto alla sede evento
• Ambiente tranquillo per concentrazione pre-congresso
• Servizi business-ready: WiFi veloce, spazi lavoro, massima riservatezza

**CONDIZIONI DEDICATE PER L'EVENTO:**
• Tariffa evento: €[TARIFFA]/notte
• Check-in/out flessibili compatibili con orari sessioni
• Possibilità di estensione notti se relatori anticipano arrivo

{custom_notes if custom_notes else ''}

Vista la prossimità dell'evento, resto a disposizione per un riscontro rapido.

Posso inviarle foto della struttura e maggiori dettagli?

Cordiali saluti,

{user_name}
{user_email}
{user_phone}

P.S. Se per questo evento siete già organizzati, tenete presente la nostra soluzione per eventi futuri."""

    return {
        'subject': subject,
        'body': body
    }


def _get_zone(org_name):
    """Estrae la zona dell'organizzazione destinataria per personalizzare"""
    if 'eur' in org_name.lower():
        return 'EUR'
    elif 'gemelli' in org_name.lower():
        return 'Monte Mario/Gemelli'
    elif 'centro' in org_name.lower() or 'auditorium' in org_name.lower():
        return 'Centro/Flaminio'
    elif 'hilton' in org_name.lower() and 'cavalieri' in org_name.lower():
        return 'Balduina (stessa zona)'
    else:
        return 'Balduina'
