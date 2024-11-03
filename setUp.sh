python -m venv venv
source venv/bin/activate

cd script
echo "Installing dependencies..."
chmod 770 installDependecies.sh
./installDependecies.sh
cd ..

echo "Everything is ready to go!"
echo "now to run the preject you have to run the ./start[NameOfModel].sh"