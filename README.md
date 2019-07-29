# FlaskRestAPI




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
