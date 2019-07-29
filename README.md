# FlaskRestAPI

## Projenin amacı:
  API kullanıcı adı, email ve passwordla kaydolarak gönderi
    paylaşma, paylaşılan gönderilere yorum yapma amacıyla oluşturulmuştur.
  Gönderi paylaşmak ve yorum yapmak vb. durumlar için giriş 
    yapmak zorunludur. Giriş yapmış kullanıcılar aynı zamanda 
    kullanıcıya, gönderiye veya yoruma puan verebilirler. 
  Bir kullanıcı sadece kendine ait yorumu, gönderiyi veya kendi kullanıcı
    bilgilerini silebilir veya güncelleyebilmektedir ancak admin yetkisine
    sahip kullanıcı tüm yetkilere sahiptir.
    
 ## Projenin çalıştırılması:
Projeyi kendi bilgisayarınıza çektikten sonra [requirements.txt](https://github.com/intern-cases/FlaskRestAPI/blob/master/requirements.txt "requirements.txt")
 dosyasını
 
 `$ cd 'Projeyi çektiğiniz konum'`  
 `$ pip install requirements.txt`
 Şeklinde kurarak projeye ait tüm kütüphaneleri yükleyebilirsiniz.
 
 (Virtual enviroment üzerinde kurulması tavsiye edilir.)
 
 Veritabanı olarak postgresql kullanmak isterseniz 
 `$ pip install postgres` komutuyla indirebilirsiniz.
 `$ pg_ctl -D /usr/local/var/postgres start` komutu ile de postgresqli başlatmanız gerekmektedir.
 

 ## Endpointlerin çalışma şekli:
 Alt kısımdaki endpointler,[Endpoints](https://github.com/intern-cases/FlaskRestAPI/blob/master/testviews.py "Endpoints")
 dosyasındaki url uzantılarının ne iş yaptıklarını göstermektedir. Test dosyasının içindeki .json uzaktılı dosyayı [Postman](https://www.getpostman.com "Postman") ile açtığınızda tüm endpointlerin deneme requestlerine ulaşabilirsiniz.
 [Endpoints](https://github.com/intern-cases/FlaskRestAPI/blob/master/testviews.py "Endpoints") dosyasının içinde /addroles endpointini açarak veritabanında RolesModele ilk olarak user eklenmeli sonrasında admin eklenmeli. Auto increment sayesinde user'ın role_id'si 1, adminin role_id'si 2 olarak tanımlanmalıdır.('POST' requestinde "role_name":"user", "role_name":"admin" olarak 2 kez request yapılmalıdır.) Sonrasında ilk kullanıcının rolü admin olan rol 2 olarak tanımlanmalıdır. Ardından admin olan kullanıcı authentication kısmından giriş yaptığında diğer kullanıcılara admin yetkisi atayabilir(/setroles endpointini kullanarak).
 

| HTTP Method| Url                                   | Explanation                                                                 |
| :---       |     :---:                             |          ---:                                                               |
| POST       |/user                                  | Yeni bir kullanıcı eklemek için kullanılır                                  |
| POST       |/set_points/<string:username>          | Girilen username'e puan verilir                                             |
| GET        |/user_panel                            | Login yapan kullanıcı kullanıcı bilgilerini görebilir                       |
| GET        |/users                                 | Tüm kullanıcılar birlikte görülebilir                                       |
| GET        |/user/<int:user_id>                    | User_id bilgisi girilen kullanıcının bilgileri gösterilir                   |
| GET        |/user/<string:username>                | Username bilgisi verilen kullanıcının bilgileri gösterilir                  |
| PUT        |/user/<string:username>                | Login yapan kullanıcı kullanıcı bilgilerini günceller                       |
| DELETE     |/user/<int:user_id>                    | Login yapan kullanıcı user_id'sini girerek kullanıcıyı siler                |
| DELETE     |/user/<string:username>                | Login yapan kullanıcı username'ini girerek kullanıcıyı siler                |
| POST       |/post                                  | Login yapan kullanıcı hesabına post ekleyebilir                             |
| POST       |/set_points_post/<int:post_id>         | Login yapan kullanıcı post_id girerek başkasının postuna puan verebilir     |
| GET        |/my_posts                              | Login yapan kullanıcı kendi postlarını görebilir                            |
| GET        |/main_page                             | Tüm postlar görülebilir                                                     |
| GET        |/post/<int:user_id>                    | User_id'si girilen kisinin tüm postları görülebilir                         |
| GET        |/post/<string:username>                | Username'i girilen kisinin tüm postları görülebilir                         |
| PUT        |/post/<int:user_id>/<int:post_id>      | Login yapan kullanıcı user_id ve post_id girerek postta güncelleme yapabilir|
| DELETE     |/post/<int:post_id>                    | Login yapan kullanıcı post_id'sini girdiği postu silebilir.                 |
| POST       |/comment/post<int:post_id>             | Login yapan kullanıcı post_id'sini girdiği posta comment ekleyebilir        |
| POST       |/set_points_comment/<int:comment_id    | Login yapan kullanıcı comment_id'sini girdiği commente puan verebilir       |
| PUT        |/comment/<int:post_id>/<int:comment_id>| Login yapan kullanıcı post_id ve comment_id'sini girdiği commenti günceller |
| DELETE     |/comment/delete<int:comment_id>        | Login yapan kullanıcı comment_id'sini verdiği commenti silebilir            |
| POST       |/comment/<int:comment_id>              | Login yapan kullanıcı comment_id'sini verdiği commente comment atabilir     |
| GET        |/post<int:post_id>/comments            | Post_id'si verilen posta ait commentler görülebilir                         |
| POST       |/addroles                              | Başlangıçta admin yetkisi için bir kere kullanılmalıdır                     |
| PUT        |/setroles                              | Admin yetkisi olan kişi diğer kullanıcılara roller atayabilir               |

### Veritabanı diyagramı:
Aşağıda görüldüğü şekildedir. Endpointlerde çağırılan veritabanı tablolarını diyagrama bakarak görebilirsiniz.

![](https://github.com/intern-cases/FlaskRestAPI/blob/develop/pictures/dbmodel.png)


