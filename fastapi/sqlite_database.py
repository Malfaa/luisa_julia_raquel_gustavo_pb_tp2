import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")


def init_db():
  if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()

  cursor.execute("PRAGMA foreign_keys = ON;")

  cursor.execute("""
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    );
    """)

  cursor.execute("""
    CREATE TABLE IF NOT EXISTS prediction (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        intent TEXT NOT NULL,
        owner_id INTEGER NOT NULL,
        FOREIGN KEY (owner_id) REFERENCES user (id)
    );
    """)

  usuarios = [("admin", "admin"), ("jose", "1234"), ("maria", "senha123")]
  cursor.executemany(
      "INSERT INTO user (username, password) VALUES (?, ?);", usuarios
  )

  predicoes = [
      ("Quero solicitar o reembolso do pedido.", "refund", 1),
      ("Como posso rastrear minha entrega?", "general_support", 1),
      ("Minha tela ficou completamente preta.", "technical_issue", 2),
      ("Gostaria de cancelar minha assinatura.", "cancellation", 3),
  ]
  cursor.executemany(
      """
    INSERT INTO prediction (text, intent, owner_id)
    VALUES (?, ?, ?);
    """,
      predicoes,
  )

  conn.commit()
  conn.close()
  print(f"[OK] Banco de dados inicializado com sucesso em: {DB_PATH}")


if __name__ == "__main__":
  init_db()