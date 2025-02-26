Bu proje, hem TCP hem de UDP protokollerini destekleyen bir sohbet uygulamasıdır. Kullanıcılar sunucuya bağlanarak birbirleriyle iletişim kurabilirler.


Özellikler

Çift Protokol Desteği: Hem TCP hem de UDP istemciler ile çalışır.

Çoklu Kullanıcı Desteği: Birden fazla istemci aynı anda bağlanabilir.

Gerçek Zamanlı Mesajlaşma: Kullanıcılar birbirine anlık mesaj gönderebilir.

Kullanıcı Adı Yönetimi: Kullanıcı adı çakışmalarını engeller.


KULLANIMI

1)Sunucuyu Başlat

Önce sunucuyu çalıştırmanız gerekiyor:

python 21100011065_Server.py

Sunucu açıldığında hem TCP hem de UDP bağlantılarını dinlemeye başlayacaktır.


 2)TCP İstemciyi Çalıştır

Başka bir terminalde TCP istemciyi çalıştırın:

python 21100011065_ClientTCP.py

Kullanıcı adı girerek sohbete katılabilirsiniz.


3) UDP İstemciyi Çalıştır

A lternatif olarak UDP istemciyi çalıştırabilirsiniz:

