from loguru import logger
import datetime

def create_ticket(issue_type: str, description: str):
    ticket_id = f"TCK-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

    ticket = {
        "id": ticket_id,
        "type": issue_type,
        "description": description,
        "status": "OPEN",
        "created_at": datetime.datetime.now().isoformat()
    }

    logger.success(f"Ticket creado: {ticket_id}")
    return ticket

if __name__ == "__main__":
    logger.add("logs/rpa.log", rotation="1 MB")

    issue = input("Tipo de problema (bug/incidente): ")
    desc = input("Descripción del problema: ")

    ticket = create_ticket(issue, desc)

    print("\nTicket generado:")
    for k, v in ticket.items():
        print(f"{k}: {v}")
