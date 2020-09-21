#/bin/sh
pip install --user -r book_rental_manager/requirements.txt

#tail -F /etc/hosts
python -m book_rental_manager server -a 0.0.0.0 -p 5000