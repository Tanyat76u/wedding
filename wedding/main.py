from flask import Flask, render_template, url_for, request, redirect # импортируем фласк класс из библиотки фласк   #импортируем функцию html
from flask_sqlalchemy import SQLAlchemy #класс импортируем из библиотеки flask_sqlalchemy
from datetime import datetime

app = Flask(__name__)  # директива передает название файла в котором мы это запускаем
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#обьяект db на основе класса SQLAlchemy, в констркутере прописываем обьект на основе класса фласк
#db.init_app(app)

class Article(db.Model): #класс куда мы будем записывать различные статьи на сайте, наследуем все из db model - который явл обьектом SQLAlchemy
#для каждой статьи устанавливаем название, вступит текст, текст основной, дата создания, идентификатор
    id = db.Column(db.Integer, primary_key=True) #только целые числа
    title = db.Column(db.String(100), nullable=False) #только строка 300 символов
    intro = db.Column(db.String(300), nullable=False) #только строка 300 символов
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow) #дата когда добавляется статья

    def __repr__(self): #магический метод repr
        return '<Article %r>' % self.id #когда будем выбирать какой либо обьект на основе класса, у нас будет выдаваться сам обьект и id

# функция кот будет отслеживать опред адрес, мы будем писать хелло опльзовталею если он перейдет на страничку
# декоратор app ,  отслеживание главной страницы и прописываем текст
@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html") #"hello world"


@app.route('/about')
def about():
    return render_template("about.html")#"About page"


@app.route('/posts')
def posts():# в артиклс первая запись из бд будет выводиться, если все надо - то all ставим
    articles = Article.query.order_by(Article.date).all()
    return render_template("posts.html", articles=articles) #ПЕРЕДАем шаблон - такой список Артиклс, при этом в шаблоне можем иметь доступ к этому списку по названию артиклс

@app.route('/create-article', methods=['POST', 'GET']) #отслеживаем адрес,  методы отправить и получить
def create_article():
    if request.method == "POST":
        title = request.form['title']#pass
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article) #добавляем обЪект
            db.session.commit() #сохраняем
            return redirect('/')
        except:
            return "При добавлении статьи прозошла ошибка"
    else:
        return render_template("create-article.html")#"About page"


if __name__ == "__main__":
    app.run(debug=True)  # ошибки все показываются, потом фолс поставим
