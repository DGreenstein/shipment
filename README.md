# Shipment

A game where you accept and run shipments to earn cash.  What you ship matters.  More risk, more reward.

## Game Features

- Travel from port to port.  
- Accept shipments from the list and complete the delivery.
    - Buy into black market lists?
    - Locate underground ports?
- Shipments can be both legit and illegal.
- Random port authority checks will occur.
    - Cargo manifest reconcilliation.
    - Passenger manifest reconcilliation.
    - Port authority corruption?  Can you bribe your way out of trouble?
    - Higher suspicion = tougher to get past.
- Upgrade your ship as you earn money.
    - Run more / larger cargo.
    - Improve technology.
    - Hidden compartments / false walls?
- Coast Guard in transit?

Server will maintain a leader board.
Implement seasons?  (Reset leader board / bank / etc on interval?)
All PvE... no player-to-player interactions for now

## Design

Client / Server based game.

Server:
- Maintains player state and assets
- Available shipments and thier rates
- Generates random events
- Tracks and publishes Leader Board (via API)

Client:
- Manages user input and data exchange with server
