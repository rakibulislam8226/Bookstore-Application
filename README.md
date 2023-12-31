## Bookstore Application

---
* python 3.10
* Sqlite3
---
<h3 style="color:red;">Warning</h3>
<small>To add a book to the list/database there needs authenticated user. So you can authenticated through Add cart API and login into the sire or you can log in to the admin site using 
http://rakibulislam8226.pythonanywhere.com/admin/ 
username = admin, 
password = admin. 
After the browser knows your authorizations then you can perform the API and also can add a book. N:B: If those configurations need to do then let me know I will do those. </small>

#### Clone the repo
```
git clone git@github.com:rakibulislam8226/Bookstore-Application.git
```
**Go to the directory file**
```
cd Bookstore-Application/
```
---
###### Open the project into a code editor and expand terminal OR continue with default terminal. ######
---
**Create virtual environment based on your operating system**
 * **For ubuntu**
 ```shell
python3.10 -m venv venv
  ```

  ###### Activate the virtual environment
 ```shell
source venv/bin/activate
  ```
 * **For windows**
 ```shell
python -m venv venv
  ```

---
**Copy .example.env file to .env:**
###### N:B: If you skip the .env section then no problems at this moment

  * For linux
    ```shell
    cp .example.env .env
    ```
  * For windows
    ```shell
    copy .example.env .env
    ```

##### Fill the .env with proper data
---
### Install the requirements file.
```
pip install -r requirements.txt
```
#### Go the the src directory
```
cd src/
```

  ###### Migrate the project
 ```shell
python manage.py migrate
  ```
  ###### If needed create superuser with proper data
  ```shell
  python manage.py createsuperuser
  ```
  ###### Run the server
 ```shell
python manage.py runserver
  ```
---

## Project Structure
```
.
├── README.md
├── requirements.txt
└── src
    ├── book_store
    │   ├── admin.py
    │   ├── apps.py
    │   ├── forms.py
    │   ├── __init__.py
    │   ├── middlewares
    │   │   ├── auth.py
    │   │   └── __init__.py
    │   ├── models.py
    │   ├── serializers.py
    │   ├── templates
    │   │   ├── add_book.html
    │   │   ├── base.html
    │   │   ├── cart.html
    │   │   ├── index.html
    │   │   ├── login.html
    │   │   ├── orders.html
    │   │   └── signup.html
    │   ├── templatetags
    │   │   ├── cart.py
    │   │   └── custom_filter.py
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    ├── config
    │   ├── asgi.py
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    └── manage.py

```