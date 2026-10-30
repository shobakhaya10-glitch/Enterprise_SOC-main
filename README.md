Security alerts are stored in the SQLite database.

---

### 3. Security Event Logging

Security events are recorded in the SOC database.

Events include:

- Successful logins
- Failed logins
- Network reachability events
- Port status events

---

### 4. SOC Dashboard

The monitoring dashboard provides a security summary containing:

- Total security events
- Successful logins
- Failed logins
- Network events
- Port events
- HIGH severity alerts
- Recent security events
- Recent security alerts

---

### 5. Network Monitoring

The network monitoring module displays:

- Hostname
- Network interface
- IP address
- Host reachability

---

### 6. Port Monitoring

The system can test selected ports on a target host.

Currently monitored ports:

- Port 22
- Port 80
- Port 443

---

## System Architecture

```text
                    ENTERPRISE SOC
                          |
        +-----------------+-----------------+
        |                 |                 |
 Authentication      Monitoring        Network
        |                 |                 |
        v                 v                 v
     auth.py          monitor.py       network.py
        |                 |                 |
        +-----------------+-----------------+
                          |
                          v
                    alerts.py
                          |
                          v
                    database.py
                          |
                          v
                    SQLite Database
                       soc.db
