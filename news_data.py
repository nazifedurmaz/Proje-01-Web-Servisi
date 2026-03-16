# Gazete Hacettepe'den önceden çekilmiş haber verisi
# (Gerçek ortamda scraper.py bu veriyi canlı olarak üretir)

SAMPLE_NEWS = [
    {
        "id": 910,
        "title": "ACM Hacettepe'ye Kampüsün Enleri oylamasında 3 ödül",
        "summary": "Hacettepe Üniversitesi ACM Öğrenci Topluluğu, Kampüsün Enleri oylamasında 3 farklı kategoride ödül almaya hak kazandı. Topluluk üyeleri ve akademisyenler bu başarıdan büyük gurur duydu.",
        "author": "Öğrenci",
        "date": "16.03.2026",
        "image_url": "",
        "url": "https://gazete.hacettepe.edu.tr/tr/haber/acm_hacettepeye_kampusun_enleri_oylamasinda_3_odul-910",
        "category": "ogrenci"
    },
    {
        "id": 909,
        "title": "Nörobilim alanında üniversitemizden iki önemli başarı",
        "summary": "Hacettepe Üniversitesi Nörobilim araştırmacıları, uluslararası alanda yayımlanan iki ayrı çalışmayla dikkat çekti. Araştırmalar beyin hastalıklarının erken teşhisine yönelik önemli bulgular içeriyor.",
        "author": "Araştırma",
        "date": "13.03.2026",
        "image_url": "https://gazete.hacettepe.edu.tr/fs_/HABERLER/2026/Mart/norobiliml.jpg",
        "url": "https://gazete.hacettepe.edu.tr/tr/haber/norobilim_alaninda_universitemizden_iki_onemli_basari-909",
        "category": "arastirma"
    },
    {
        "id": 908,
        "title": "Hacettepe'den Uluslararası Başarı: BioPATH-SAID projesine AB desteği",
        "summary": "Hacettepe Üniversitesi koordinasyonunda yürütülen BioPATH-SAID projesi, Avrupa Birliği'nin Horizon programı kapsamında önemli bir finansman desteği almaya hak kazandı.",
        "author": "Araştırma",
        "date": "11.03.2026",
        "image_url": "https://gazete.hacettepe.edu.tr/fs_/HABERLER/2026/Mart/biopath.jpg",
        "url": "https://gazete.hacettepe.edu.tr/tr/haber/hacettepeden_uluslararasi_basari:_biopathsaid_projesine_ab_destegi-908",
        "category": "arastirma"
    },
    {
        "id": 907,
        "title": "Bologna-Ankara arasında değişim ve iş birliği projesi başladı",
        "summary": "Hacettepe Üniversitesi ile İtalya'nın Bologna Üniversitesi arasında imzalanan iş birliği protokolü kapsamında öğrenci ve akademisyen değişim programı hayata geçirildi.",
        "author": "Uluslararası İlişkiler",
        "date": "10.03.2026",
        "image_url": "",
        "url": "https://gazete.hacettepe.edu.tr/tr/haber/bolognaankara_arasinda_degisim_ve_is_birligi_projesi_basladi-907",
        "category": "uluslararasi"
    },
    {
        "id": 906,
        "title": "Geleceğin spor kadın liderleri Hacettepe'de",
        "summary": "Hacettepe Üniversitesi Spor Bilimleri Fakültesi, kadın sporculara yönelik liderlik programı düzenledi. Programa farklı branşlardan genç sporcular katıldı.",
        "author": "Spor",
        "date": "09.03.2026",
        "image_url": "https://gazete.hacettepe.edu.tr/fs_/HABERLER/2026/Mart/spor.jpg",
        "url": "https://gazete.hacettepe.edu.tr/tr/haber/gelecegin_spor_kadin_liderleri_hacettepede-906",
        "category": "spor"
    },
    {
        "id": 419,
        "title": "Türkiye'nin en kapsamlı Biyoçeşitlilik Müzesi Hacettepe'de açıldı",
        "summary": "Türlerin ve genlerin biyosferdeki serüvenlerinin keşfedileceği Hacettepe Üniversitesi Biyoçeşitlilik Müzesi'nin (BİYOSFER) açılış töreni, 22 Mayıs 2023 tarihinde Dünya Biyoçeşitlilik Günü'nde Beytepe Yerleşkesinde gerçekleştirildi.",
        "author": "Yönetim",
        "date": "22.05.2023",
        "image_url": "https://www.biyosfermuze.com/wp-content/uploads/2022/10/muze1.jpg",
        "url": "https://gazete.hacettepe.edu.tr/tr/haber/turkiyenin_en_kapsamli_biyocesitlilik_muzesi_hacettepede_acildi-419",
        "category": "yonetim"
    },
    {
        "id": 412,
        "title": "Üniversitemize YÖKAK tarafından 5 yıl süreyle tam akreditasyon",
        "summary": "Yükseköğretim Kalite Kurulu (YÖKAK) tarafından uygulanan Kurumsal Akreditasyon Programı kapsamında Hacettepe Üniversitesi, 5 yıl süreyle tam akreditasyon almaya hak kazandı.",
        "author": "Yönetim",
        "date": "15.04.2023",
        "image_url": "https://gazete.hacettepe.edu.tr/fs_/HABERLER/2023/Nisan/yokak.jpg",
        "url": "https://gazete.hacettepe.edu.tr/tr/haber/universitemize_yokak_tarafindan_5_yil_sureyle_tam_akreditasyon-412",
        "category": "yonetim"
    },
    {
        "id": 407,
        "title": "Projemize TÜBİTAK 1004 desteği",
        "summary": "Sağlıklı Yaşam İçin Yeni Nesil Biyomalzeme Teknolojileri Araştırma Ağı Platformu projesinin imza töreni TEKNOFEST'te yapıldı. Proje, TÜBİTAK 1004 programından önemli bir finansman desteği aldı.",
        "author": "Araştırma",
        "date": "02.10.2022",
        "image_url": "https://gazete.hacettepe.edu.tr/fs_/HABERLER/2022/Ekim/tubitak1004.jpg",
        "url": "https://gazete.hacettepe.edu.tr/tr/haber/universitemiz_tarafindan_sunulan_projeye_tubitak_1004_destegi-407",
        "category": "arastirma"
    },
    {
        "id": 353,
        "title": "İki öğretim üyemize TÜBİTAK Bilim Ödülü",
        "summary": "TÜBİTAK ödülleri kapsamında öğretim üyelerimiz Prof. Dr. Vural Gökmen ve Prof. Dr. Fatih Özaltın'a Bilim Ödülü verildi. Ödüller, Ankara'da düzenlenen törenle sahiplerine teslim edildi.",
        "author": "Ödül",
        "date": "18.12.2021",
        "image_url": "https://gazete.hacettepe.edu.tr/fs_/HABERLER/2021/Aralik/tubitak_bilim.jpg",
        "url": "https://gazete.hacettepe.edu.tr//tr/haber/iki_ogretim_uyemize_tubitak_bilim_odulu-353",
        "category": "odul"
    },
    {
        "id": 337,
        "title": "10 bin yıl öncesine ışık tutan çalışma Current Biology'de yayımlandı",
        "summary": "Hacettepe ve ODTÜ'den araştırmacıların çalışması, Güneybatı Asya ve Doğu Akdeniz'deki insan hareketliliğinin son 10 bin yılını aydınlatan önemli bulgular içeriyor. Makale Current Biology dergisinde yayımlandı.",
        "author": "Araştırma",
        "date": "05.08.2021",
        "image_url": "https://gazete.hacettepe.edu.tr/fs_/HABERLER/2021/Agustos/currentbiology.jpg",
        "url": "http://gazete.hacettepe.edu.tr/tr/haber/10_bin_yil_oncesine_isik_tutan_calisma_current_biologyde_yayimlandi_-337",
        "category": "arastirma"
    }
]
