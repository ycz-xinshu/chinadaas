#kill python processes
ps -ef|grep python|grep -v grep|cut -c 9-15|xargs kill -9

nohup python manage.py runserver h2:8000 &
