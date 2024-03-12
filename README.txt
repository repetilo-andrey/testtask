# Опционально, для библиотеки виртуального окружения
sudo apt install python3-venv
###

# скачиваем код
git clone git@github.com:repetilo-andrey/testtask.git

# Создаем виртуальное окружение для проекта, устанавливаем либы
cd testtask
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
cd testtask

# в качестве тестовой базы планировал просто SQLite. Но, оказалось, что она некорректно ищет в кириллице (юникоде).
# поэтому создаем базу в postgres. или пропускаем этот шаг и для использования SQLite в файле testtask/testtask/settings.py комментим/раскомментим то, что касается DATABASES
sudo -u postgres psql
create database testtask ENCODING UTF8;
create user testtask_user with encrypted password '1';
grant all privileges on database testtask to testtask_user;
\q

# из-за использования django-mptt процесс создания тестовых записей занимает до получаса. перед стартом миграций можно уменьшить количество иерархических деревьев в файле testtask/coworkers/migrations/0003_test_data.py, 69 строка
python manage.py migrate

# регистрацию не требовалось реализовать, поэтому для теста действвий залогиненного юзера создаем его командой
python manage.py createsuperuser

# запуск
python manage.py runserver