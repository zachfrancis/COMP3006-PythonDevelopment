
#!/bin/bash
cut -c63-69 Data.txt | sort -b -n | python3 compute_stats.py

