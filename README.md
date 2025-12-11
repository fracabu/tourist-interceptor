# 🧭 Tourist Interceptor CRM

**CRM locale per lead generation B2B nel settore eventi e congressi a Roma**

Tool semplice e potente per gestire contatti, tracciare eventi e ottimizzare l'outreach per case vacanze nel segmento congressuale.

---

## ✨ Funzionalità

- ✅ **Dashboard interattiva** con statistiche in tempo reale
- 📇 **Gestione contatti B2B** con sistema di priorità (Tier 1/2/3)
- 📊 **Pipeline management** con stati (Freddo → Tiepido → Caldo → Cliente → Partner)
- 🗓️ **Tracking eventi** congressuali con valore opportunità
- 💬 **Storico interazioni** per ogni contatto
- 📈 **Sistema di scoring automatico** per prioritizzazione
- 🔔 **Reminder follow-up** con date prossime azioni
- 📤 **Import automatico** da file Markdown

---

## 🚀 Installazione e Avvio Rapido

### 1. Requisiti

- **Python 3.8+** installato sul sistema
- Nessun altro requisito! Tutto il resto verrà installato automaticamente.

### 2. Installazione dipendenze

Apri il terminale nella cartella del progetto e installa le dipendenze:

```bash
pip install -r requirements.txt
```

### 3. Primo avvio e importazione dati

Avvia l'applicazione:

```bash
python app.py
```

Vedrai questo messaggio:
```
* Running on http://127.0.0.1:5000
```

### 4. Apri il browser

Vai su: **http://127.0.0.1:5000**

### 5. Importa i contatti

Nella dashboard, clicca sul pulsante **"Importa Contatti da dati.md"**

Verranno importati automaticamente tutti i 20+ contatti dal file `dati.md`!

---

## 📖 Come Usare il Tool

### Dashboard (`/`)
- Panoramica statistiche: totale contatti, clienti, partner, lead caldi
- Distribuzione per status e tier
- Contatti da seguire oggi (reminder)
- Ultimi contatti aggiunti

### Contatti (`/contacts`)
- Lista completa con **filtri**:
  - Cerca per nome, email, organizzazione
  - Filtra per Tier (1/2/3)
  - Filtra per Status (Freddo/Tiepido/Caldo/Cliente/Partner)
- Visualizza tutti i dettagli: email, telefono, LinkedIn, score

### Dettaglio Contatto (`/contact/<id>`)
- Tutte le informazioni del contatto
- **Storico interazioni** (email, telefono, LinkedIn, persona)
- **Aggiungi nuova interazione** con esito
- Modifica contatto e aggiorna status
- Imposta prossima azione con data e descrizione

### Eventi (`/events`)
- Traccia eventi congressuali
- Valore opportunità e probabilità chiusura
- Status evento (Da contattare → Chiuso/Vinto)

### Statistiche (`/stats`)
- KPI completi: contatti, clienti, partner, eventi
- **Pipeline value** ponderata
- Progressi verso obiettivi 90 giorni (dalla strategia documento)

---

## 🎯 Workflow Consigliato

### Settimana 1: Setup e familiarizzazione
1. ✅ Importa contatti da `dati.md`
2. ✅ Esplora la dashboard e le sezioni
3. ✅ Identifica i **Tier 1** (alta priorità) da contattare per primi

### Settimana 2-4: Primo outreach
1. Filtra contatti per **Tier 1** e **Status = Freddo**
2. Per ogni contatto:
   - Apri il dettaglio
   - Prepara email/telefonata
   - Dopo il contatto: **Aggiungi interazione**
   - Aggiorna status se necessario (es. da Freddo → Tiepido)
   - Imposta **prossima azione** con data

### Routine giornaliera (15 minuti)
1. Controlla dashboard → **"Da Seguire Oggi"**
2. Esegui le azioni programmate
3. Aggiungi interazione dopo ogni contatto
4. Pianifica prossima azione

### Routine settimanale (30 minuti)
1. Vai su **Statistiche** → verifica progressi
2. Filtra contatti "Tiepidi" → identifica chi far diventare "Caldo"
3. Aggiungi nuovi eventi scoperti nella settimana
4. Pulisci reminder vecchi

---

## 📊 Sistema di Prioritizzazione

### Tier (Priorità)
- **Tier 1** 🔴 Alta priorità (es. Convention Bureau, Policlinico Gemelli, La Nuvola)
- **Tier 2** 🟡 Media priorità (es. Federcongressi, Sapienza, Balestra SRL)
- **Tier 3** ⚪ Bassa priorità (es. Organizzatori secondari)

### Status (Stato Lead)
- **Freddo**: Mai contattato o nessuna risposta
- **Tiepido**: Ha risposto, interesse generico
- **Caldo**: Interesse concreto, preventivo richiesto
- **Cliente**: Prenotazione confermata
- **Partner**: Accordo collaborazione attivo

### Priority Score
Calcolato automaticamente basato su:
- Tier del contatto
- Presenza email diretta (+5 punti)
- Presenza telefono (+5 punti)
- Presenza LinkedIn (+3 punti)

---

## 🗂️ Struttura File

```
tourist-interceptor/
│
├── app.py                  # Applicazione Flask principale
├── models.py               # Database models (Contact, Interaction, Event)
├── parser.py               # Import da dati.md
├── requirements.txt        # Dipendenze Python
├── README.md              # Questa guida
│
├── dati.md                # I tuoi contatti (20+ organizzazioni)
├── info.md                # Strategia B2B lead generation
│
├── crm.db                 # Database SQLite (creato automaticamente)
│
└── templates/             # Template HTML
    ├── base.html
    ├── index.html
    ├── contacts.html
    ├── contact_detail.html
    ├── edit_contact.html
    ├── new_contact.html
    ├── events.html
    ├── new_event.html
    └── stats.html
```

---

## 💡 Suggerimenti e Best Practices

### ✅ DO:
- Aggiorna **sempre** lo storico interazioni dopo ogni contatto
- Imposta **prossima azione** con data per ogni contatto attivo
- Usa i **filtri** per identificare chi seguire
- Cambia status quando il lead si scalda
- Controlla la dashboard ogni mattina (5 minuti)

### ❌ DON'T:
- Non accumulare contatti senza mai aggiornarli
- Non lasciare interazioni senza esito registrato
- Non dimenticare di impostare reminder follow-up
- Non trascurare i Tier 1 (massima priorità!)

---

## 🔧 Comandi Utili

### Avviare il server
```bash
python app.py
```

### Re-importare dati (se modifichi dati.md)
Devi prima eliminare il database e riavviare:
```bash
# Windows
del crm.db
python app.py

# Mac/Linux
rm crm.db
python app.py
```
Poi clicca su "Importa Contatti" nella dashboard.

### Backup database
Il file `crm.db` contiene tutti i tuoi dati. Copialo regolarmente:
```bash
# Windows
copy crm.db crm_backup_2025.db

# Mac/Linux
cp crm.db crm_backup_2025.db
```

---

## 📈 Obiettivi 90 Giorni (dalla strategia)

Il tool ti aiuta a raggiungere:
- ✅ **60-80 contatti B2B qualificati** nel database
- ✅ **15-20 preventivi inviati** a organizzatori/PCO
- ✅ **5-8 prenotazioni dirette B2B** confermate
- ✅ **3-5 partnership strategiche** attivate

Controlla i progressi nella sezione **Statistiche**!

---

## 🎨 Personalizzazione

### Aggiungere nuove organizzazioni
Vai su **Contatti → Nuovo Contatto** e compila il form.

### Modificare tier/status
Apri il contatto → **Modifica** → Cambia tier o status.

### Tracciare eventi
**Eventi → Nuovo Evento** → Inserisci:
- Nome evento
- Date
- Sede (es. Hilton Rome Eur)
- Valore opportunità (€)
- Probabilità chiusura (%)

---

## 🆘 Risoluzione Problemi

### Il server non parte
```bash
pip install --upgrade flask flask-sqlalchemy
python app.py
```

### Dati non importati
Verifica che `dati.md` sia nella stessa cartella di `app.py`.

### "Database locked"
Chiudi altre istanze di `app.py` e riprova.

---

## 📞 Supporto

Per problemi o domande, controlla:
1. Questa guida (README.md)
2. Il file strategia completa (info.md)

---

## 🎯 Prossimi Sviluppi (Opzionali)

Funzionalità che possiamo aggiungere:
- 📧 Generatore email personalizzate
- 🔔 Notifiche desktop per reminder
- 📊 Export Excel/CSV aggiornato
- 🌐 Web scraping automatico eventi
- 📱 Invio SMS reminder
- 🔗 Integrazione Google Calendar

---

**Buon lead generation! 🚀**

*Creato per ottimizzare la strategia B2B di Roma Caput Mundi Apartments*

