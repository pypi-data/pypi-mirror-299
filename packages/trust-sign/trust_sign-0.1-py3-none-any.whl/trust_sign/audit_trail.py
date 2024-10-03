import sqlite3

def init_db():
    conn = sqlite3.connect('audit_trail.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_trail (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            details TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_audit_trail(action, details):
    conn = sqlite3.connect('audit_trail.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO audit_trail (action, details) VALUES (?, ?)', (action, details))
    conn.commit()
    conn.close()



def log_audit_trail(action, details):
    """
    Fonction pour enregistrer les actions dans un audit trail.
    
    :param action: Type d'action effectuée.
    :param details: Détails associés à l'action.
    """
    # Ici, vous pouvez écrire les logs dans un fichier, une base de données, etc.
    print(f"ACTION: {action}, DETAILS: {details}")