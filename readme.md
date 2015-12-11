# Sonos player

Trigger alarms or events on Sonos systems.

More info: https://www.codedog.co.uk/sonosalarm

# Quick usage:

  1) Discover your player names

```
Sams-MacBook-Pro-4:sonosalarm sam$ sonosalarm discovery
+----------------+--------------------------+----------------+----------------+
| Zone Name      | UID                      | Group          | Current Volume |
+----------------+--------------------------+----------------+----------------+
| Player 1       | RINCON_000XXXXXXXXXX1400 | Player 1       | 5              |
+----------------+--------------------------+----------------+----------------+
| Player 2       | RINCON_000XXXXXXXXXX1400 | Player 1       | 13             |
+----------------+--------------------------+----------------+----------------+
| Player 3       | RINCON_000XXXXXXXXXX1400 | Player 1       | 17             |
+----------------+--------------------------+----------------+----------------+
```

  2) Create a config file with a URL in

```yaml
zone: "Player 1"
file: "http://example.com/Friday.aif"
volume: 65
fadeout: 3
```

  3) Configure a cronjob to run the alarm

```
58 16 * * Fri smudge sonosalarm alarm --config=/path/to/config.yml
```
