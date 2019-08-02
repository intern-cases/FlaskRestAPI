# Blog example with Flask Rest API

Install
----

    $ git clone git@github.com:intern-cases/FlaskRestAPI.git
    $ cd /Projenin konumu
    $ docker-compose build
    $ doker-compose up -d
    
Start
---
    $ docker exec -it flaskrestapi_app_1 bash
    root:/app# python manage.py db migrate
    root:/app# python manage.py db upgrade
    root:/app# python manage.py runserver
    root:/app# python initial.py
    
    
    http://127.0.0.1:1996/
 
 Test dosyasının içindeki [postman_collection.json](https://github.com/intern-cases/FlaskRestAPI/blob/master/test/test.postman_collection.json "postman_collection.json") 
 dosyasını postmande çalıştırarak test sorgularını deneyebilirsiniz.
    


## Projenin amacı:
  API kullanıcı adı, email ve passwordla kaydolarak gönderi
    paylaşma, paylaşılan gönderilere yorum yapma amacıyla oluşturulmuştur.
  Gönderi paylaşmak ve yorum yapmak vb. durumlar için giriş 
    yapmak zorunludur. Giriş yapmış kullanıcılar aynı zamanda 
    kullanıcıya, gönderiye veya yoruma puan verebilirler. 
  Bir kullanıcı sadece kendine ait yorumu, gönderiyi veya kendi kullanıcı
    bilgilerini silebilir veya güncelleyebilmektedir ancak admin yetkisine
    sahip kullanıcı tüm yetkilere sahiptir.
    
##Projenin Özeti ve Kullanılan Teknolojiler : 
Proje Python Flask framework ile yapılmış olup Postgresql veritabanı bağlantıları için Flask-SQLAlchemy kullanılmıştır.
Diğer kütüphaneler için requirements.txt
    
 # Endpointler:
 Alt kısımdaki endpointler,[Endpoints](https://github.com/intern-cases/FlaskRestAPI/tree/master/api "Endpoints")
 dosyasındaki url uzantılarının ne iş yaptıklarını göstermektedir. Test dosyasının içindeki .json uzaktılı dosyayı [Postman](https://www.getpostman.com "Postman") ile açtığınızda tüm endpointlerin deneme requestlerine ulaşabilirsiniz.      
 Sonrasında ilk kullanıcının rolü admin olan rol 2 olarak tanımlanmalıdır. Ardından admin olan kullanıcı authentication kısmından giriş yaptığında diğer kullanıcılara admin yetkisi atayabilir(/setroles endpointini kullanarak).
 
 ### Örnek Request:
    
    GET  127.0.0.1:1996/users/list
    
 ### Örnek Response:

    [
        {
            "comments": [],
            "created_time": "2019-08-02T07:34:25.683699+00:00",
            "email": "test@testmail.com",
            "modified_at": "2019-08-02T07:34:25.683699+00:00",
            "points": [],
            "posts": [],
            "user_id": 1,
            "username": "test"
        }
    ]
    
    
### Örnek Request:
    
    POST 127.0.0.1:1996/users/sign_up
    Body: 
    {
	"username":"test",
	"password":"test123",
	"email":"test@testmail.com"
    }
    
### Örnek Response:
    
    It signs a user to database and returns json test:
    Request done.
  
| HTTP Method| Url                                   | Explanation                                                                 |
| :---       |     :---:                             |          ---:                                                               |
| POST       |/users/sign_up                         | Yeni bir kullanıcı eklemek için kullanılır                                  |
| POST       |/users/set_points/<string:username>    | Girilen username'e puan verilir                                             |
| GET        |/users/user_panel                      | Login yapan kullanıcı kullanıcı bilgilerini görebilir                       |
| GET        |/users/list                            | Tüm kullanıcılar birlikte görülebilir                                       |
| GET        |/users/<int:user_id>                   | User_id bilgisi girilen kullanıcının bilgileri gösterilir                   |
| GET        |/users/<string:username>               | Username bilgisi verilen kullanıcının bilgileri gösterilir                  |
| PUT        |/users/<string:username>               | Login yapan kullanıcı kullanıcı bilgilerini günceller                       |
| DELETE     |/users/delete/<int:user_id>            | Login yapan kullanıcı user_id'sini girerek kullanıcıyı siler                |
| DELETE     |/user/delete/<string:username>         | Login yapan kullanıcı username'ini girerek kullanıcıyı siler                |
| POST       |/posts/post                                  | Login yapan kullanıcı hesabına post ekleyebilir                             |
| POST       |/posts/set_points_post/<int:post_id>         | Login yapan kullanıcı post_id girerek başkasının postuna puan verebilir     |
| GET        |/posts/my_posts                              | Login yapan kullanıcı kendi postlarını görebilir                            |
| GET        |/posts/main_page                             | Tüm postlar görülebilir                                                     |
| GET        |/posts/<int:user_id>                    | User_id'si girilen kisinin tüm postları görülebilir                         |
| GET        |/posts/<string:username>                | Username'i girilen kisinin tüm postları görülebilir                         |
| PUT        |/posts/<int:user_id>/<int:post_id>      | Login yapan kullanıcı user_id ve post_id girerek postta güncelleme yapabilir|
| DELETE     |/posts/<int:post_id>                    | Login yapan kullanıcı post_id'sini girdiği postu silebilir.                 |
| POST       |/comments/post<int:post_id>             | Login yapan kullanıcı post_id'sini girdiği posta comment ekleyebilir        |
| POST       |/comments/set_points_comment/<int:comment_id    | Login yapan kullanıcı comment_id'sini girdiği commente puan verebilir       |
| PUT        |/comments/<int:post_id>/<int:comment_id>| Login yapan kullanıcı post_id ve comment_id'sini girdiği commenti günceller |
| DELETE     |/comments/delete<int:comment_id>        | Login yapan kullanıcı comment_id'sini verdiği commenti silebilir            |
| POST       |/comments/<int:comment_id>              | Login yapan kullanıcı comment_id'sini verdiği commente comment atabilir     |
| GET        |/comments/post<int:post_id>                      | Post_id'si verilen posta ait commentler görülebilir                         |
| PUT        |/users/set_roles                          | Admin yetkisi olan kişi diğer kullanıcılara roller atayabilir               |

# Veritabanı Diyagramı:
Aşağıda görüldüğü şekildedir. Endpointlerde çağırılan veritabanı tablolarını diyagrama bakarak görebilirsiniz.

![](https://github.com/intern-cases/FlaskRestAPI/blob/develop/docs/dbmodel.png)


# UML Diyagramı:
Sağ taraftaki admin giriş yaptığında tüm kullanıcılara bağlı gönderi ve yorumları silme yetkisine sahiptir.
![](https://github.com/intern-cases/FlaskRestAPI/blob/develop/docs/flaskuml.png)
