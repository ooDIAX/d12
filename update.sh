pip install -r requirements.txt
echo "Sleeping for 10 seconds to allow the database to start up..."
sleep 10
nohup python3 main.py &