ssh -t anhd@45.55.44.160 "cd /var/www/anhd-council-backend && sudo sh pull.sh"

docker exec -it app python pre_cache.py
