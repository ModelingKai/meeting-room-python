# meeting-room-python

![](https://github.com/ModelingKai/meeting-room-python/workflows/Python%20application/badge.svg)
![Generate PlantUML Diagrams](https://github.com/ModelingKai/meeting-room-python/workflows/Generate%20PlantUML%20Diagrams/badge.svg)


# DjangoとVue.jsの環境確認

## 前提
- `pipenv update` で、djangorestframeworkを用意
- vue-cliが使えるようになること

---
## 手順

- Vue.js側のテンプレートファイルのビルド(npm run build)
- Djangoで使うデータベースを用意する(migrate)
- Djangoのサーバ内で使う管理者ユーザの作成(createsuperuser)
- Djangoサーバの起動

### Vue.js側のテンプレートファイルのビルド

```shell
cd frontend
npm run build
```

リポジトリ直下で`static`と`templates`フォルダが作成される


###  Djangoで使うデータベースを用意する

```shell
python manage.py makemigrations
python manage.py migrate
```

リポジトリの直下に、各モデルに対応したテーブルを内包する `db.sqlite3` が作成される

作成されるsqliteのファイル名は、 `config/settings.py`のDATABASESで管理している

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

### Djangoのサーバ内で使う管理者ユーザの作成

```shell
python manage.py createsuperuser
ユーザー名 (leave blank to use 'nakajimaatsushi'): 
メールアドレス: 
Password: 
Password (again): 
```

### Djangoサーバの起動

```shell
python manage.py runserver
```

http://127.0.0.1:8000/ へアクセス。createsuperuserで作成したユーザとパスワードでログインできる
