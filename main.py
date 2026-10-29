from kivy.config import Config
Config.set("input", "mouse", "mouse,multitouch_on_demand")
Config.set("kivy", "keyboard_mode", "system")

import json, os, calendar
from datetime import date
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle

BG   = (0.05, 0.07, 0.12, 1)
CARD = (0.11, 0.14, 0.21, 1)
CHI  = (0.16, 0.20, 0.29, 1)
TXT  = (0.96, 0.97, 0.99, 1)
MUT  = (0.55, 0.62, 0.72, 1)
PUR  = (0.55, 0.36, 0.96, 1)
CYN  = (0.02, 0.71, 0.83, 1)
GRN  = (0.06, 0.72, 0.51, 1)
RED  = (0.94, 0.27, 0.42, 1)
YEL  = (0.98, 0.75, 0.14, 1)
DRK  = (0.05, 0.05, 0.10, 1)

FILE = "paketler.json"
LANG_FILE = "dil.json"
ESIK = 400
Window.clearcolor = BG
Window.softinput_mode = 'below_target'

veri = {}
dil_ayar = "tr"

DIL = {
    'tr': {
        'toplam': 'BU AYA KADAR TOPLAM', 'paket_ad': 'P A K E T', 'tab_paket': 'PAKET',
        'tab_takvim': 'TAKVIM', 'tab_maas': 'MAAS', 'gun_ekle': 'GUN EKLE / DUZENLE',
        'tarih': 'Tarih', 'paket': 'Paket', 'kaydet': 'KAYDET', 'dinlendim': 'DINLENDIM',
        'sayi_gir': 'Sayi gir!', 'izin_gunu': 'Izin gunu', 'kayitli': 'paket kayitli (duzenleyebilirsin)',
        'henuz_yok': 'Henuz kayit yok, ekleyebilirsin', 'kaydedildi': 'paket kaydedildi',
        'dinlenme': 'Dinlenme', 'bonus_durumu': 'BONUS DURUMU', 'bonus1': '1. BONUS',
        'bonus2': '2. BONUS', 'bonus3': '3. BONUS', 'kazandin': 'KAZANDIN', 'kalan': 'kaldı',
        'kayit_yok': 'Bu ay kayit yok', 'avans': "AVANS - Ayin 5'i", 'maas_baslik': "MAAS - Ayin 20'si",
        'brut': 'Brut', 'kesinti': 'Kesinti', 'net_avans': 'NET AVANS', 'ilk': 'Ilk',
        'ustu': 'Ustu', 'brut_maas': 'Brut Maas', 'aylik_bonus': 'Aylik Bonus',
        'net_maas': 'NET MAAS', 'eline_gecen': 'ELINE GECEN', 'toplam_paket': 'Toplam %d paket',
        'dil_btn': 'BG', 'istatistik': 'AYLIK ISTATISTIK', 'stat_toplam': 'Toplam paket',
        'stat_calisilan': 'Calisilan gun', 'stat_izin': 'Izin gunu', 'stat_ortalama': 'Gunluk ortalama',
        'stat_en_iyi': 'En iyi gun', 'stat_en_kotu': 'En dusuk gun', 'gun_kazanc': 'BUGUNUN KAZANCI',
        'gun_kazanc_bekle': 'Kaydet butonuna bas',
        'aylar': ['', 'Ocak', 'Subat', 'Mart', 'Nisan', 'Mayis', 'Haziran', 'Temmuz', 'Agustos', 'Eylul', 'Ekim', 'Kasim', 'Aralik'],
        'gunler': ['Pt', 'Sa', 'Ca', 'Pe', 'Cu', 'Ct', 'Pa'],
    },
    'bg': {
        'toplam': 'ОБЩО ЗА МЕСЕЦА', 'paket_ad': 'П А К Е Т', 'tab_paket': 'ПАКЕТ',
        'tab_takvim': 'КАЛЕНДАР', 'tab_maas': 'ЗАПЛАТА', 'gun_ekle': 'ДОБАВИ / РЕДАКТИРАЙ',
        'tarih': 'Дата', 'paket': 'Пакет', 'kaydet': 'ЗАПАЗИ', 'dinlendim': 'ПОЧИВАХ',
        'sayi_gir': 'Въведи число!', 'izin_gunu': 'Почивен ден', 'kayitli': 'пакета записани (можеш да редактираш)',
        'henuz_yok': 'Още няма запис, добави сега', 'kaydedildi': 'пакета записани',
        'dinlenme': 'Почивка', 'bonus_durumu': 'СЪСТОЯНИЕ НА БОНУС', 'bonus1': '1-ВИ БОНУС',
        'bonus2': '2-РИ БОНУС', 'bonus3': '3-ТИ БОНУС', 'kazandin': 'СПЕЧЕЛИ', 'kalan': 'остават',
        'kayit_yok': 'Няма записи този месец', 'avans': 'АВАНС - 5-то число', 'maas_baslik': 'ЗАПЛАТА - 20-то число',
        'brut': 'Бруто', 'kesinti': 'Удръжка', 'net_avans': 'НЕТО АВАНС', 'ilk': 'Първи',
        'ustu': 'Останали', 'brut_maas': 'Бруто заплата', 'aylik_bonus': 'Месечен бонус',
        'net_maas': 'НЕТО ЗАПЛАТА', 'eline_gecen': 'ПОЛУЧАВАШ', 'toplam_paket': 'Общо %d пакета',
        'dil_btn': 'TR', 'istatistik': 'МЕСЕЧНА СТАТИСТИКА', 'stat_toplam': 'Общо пакети',
        'stat_calisilan': 'Работни дни', 'stat_izin': 'Почивни дни', 'stat_ortalama': 'Средно на ден',
        'stat_en_iyi': 'Най-добър ден', 'stat_en_kotu': 'Най-слаб ден', 'gun_kazanc': 'ПЕЧАЛБА ЗА ДЕНЯ',
        'gun_kazanc_bekle': 'Натисни ЗАПАЗИ',
        'aylar': ['', 'Януари', 'Февруари', 'Март', 'Април', 'Май', 'Юни', 'Юли', 'Август', 'Септември', 'Октомври', 'Ноември', 'Декември'],
        'gunler': ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Нд'],
    }
}

def dil(k):
    return DIL.get(dil_ayar, DIL['tr']).get(k, k)

def dil_yukle():
    global dil_ayar
    if os.path.exists(LANG_FILE):
        try:
            with open(LANG_FILE, 'r') as f:
                d = json.load(f)
                dil_ayar = d.get('lang', 'tr')
        except:
            dil_ayar = 'tr'

def dil_kaydet():
    with open(LANG_FILE, 'w') as f:
        json.dump({'lang': dil_ayar}, f)

def yukle():
    if os.path.exists(FILE):
        with open(FILE, encoding='utf-8') as f:
            return json.load(f)
    return {}

def kaydet(v):
    with open(FILE, 'w', encoding='utf-8') as f:
        json.dump(v, f, ensure_ascii=False)

def ay_toplam(y, a):
    b = "%04d-%02d" % (y, a)
    return sum(p for t, p in veri.items() if t.startswith(b))

def gun_toplam(hedef):
    try:
        y, m, d = hedef.split('-')
        ay_basi = "%s-%s-01" % (y, m)
        return sum(p for t, p in veri.items() if ay_basi <= t <= hedef)
    except:
        return 0

def gunluk_kazanc(paket_sayisi):
    avans_brut = paket_sayisi * 0.5112997239
    avans_net = avans_brut * 0.91
    maas_brut = paket_sayisi * 1.3293792821
    maas_net = maas_brut * 0.77
    toplam = avans_net + maas_net
    return toplam

def aylik_istatistik(y, a):
    b = "%04d-%02d" % (y, a)
    ay_veri = {t: p for t, p in veri.items() if t.startswith(b)}
    calisilan_gun = sum(1 for p in ay_veri.values() if p > 0)
    izin_gun = sum(1 for p in ay_veri.values() if p == 0)
    toplam = sum(ay_veri.values())
    ort = toplam / calisilan_gun if calisilan_gun > 0 else 0
    en_iyi_tarih = None
    en_iyi_deger = 0
    en_kotu_tarih = None
    en_kotu_deger = 99999
    for t, p in ay_veri.items():
        if p > en_iyi_deger:
            en_iyi_deger = p
            en_iyi_tarih = t
        if p > 0 and p < en_kotu_deger:
            en_kotu_deger = p
            en_kotu_tarih = t
    if en_kotu_deger == 99999:
        en_kotu_deger = 0
    return toplam, calisilan_gun, izin_gun, ort, en_iyi_tarih, en_iyi_deger, en_kotu_tarih, en_kotu_deger

def hesapla(t):
    ab = t * 0.5112997239
    an = ab * 0.91
    i = min(t, ESIK)
    f = max(t - ESIK, 0)
    mb = i * 1.3293792821 + f * 1.9940689232
    mn = mb * 0.77
    bonus = 0
    if t >= 700:
        bonus = 80
    elif t >= 600:
        bonus = 60
    elif t >= 400:
        bonus = 40
    mn_bonuslu = mn + bonus
    return mb, mn, ab, an, bonus, mn_bonuslu

class Kart(BoxLayout):
    def __init__(self, r=20, bg=CARD, **kw):
        super().__init__(**kw)
        with self.canvas.before:
            self._c = Color(*bg)
            self._rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[r])
        self.bind(pos=self._u, size=self._u)
    def _u(self, *a):
        self._rect.pos = self.pos
        self._rect.size = self.size

class GunKart(Kart):
    def __init__(self, tarih, callback, **kw):
        super().__init__(**kw)
        self.tarih = tarih
        self.callback = callback
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.callback(self.tarih)
            return True
        return False

class Buton(Button):
    def __init__(self, r=16, bg=PUR, tc=TXT, **kw):
        super().__init__(**kw)
        self.background_normal = ''
        self.background_active = ''
        self.background_color = (0, 0, 0, 0)
        self.color = tc
        self.bold = True
        self.font_size = '18sp'
        with self.canvas.before:
            self._c = Color(*bg)
            self._rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[r])
        self.bind(pos=self._u, size=self._u)
    def _u(self, *a):
        self._rect.pos = self.pos
        self._rect.size = self.size
    def renk(self, bg, tc=None):
        self._c.rgba = bg
        if tc:
            self.color = tc

class In(TextInput):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.background_normal = ''
        self.background_active = ''
        self.background_color = CHI
        self.foreground_color = TXT
        self.cursor_color = PUR
        self.hint_text_color = MUT
        self.font_size = '22sp'
        self.padding = [15, 14, 15, 14]
        self.multiline = False
        self.use_bubble = False
        self.write_tab = False
        self.cursor_width = 2

class PaketApp(App):
    def build(self):
        global FILE, veri
        self.title = 'Paket Takip'
        self.data_dir = self.user_data_dir
        FILE = os.path.join(self.data_dir, "paketler.json")
        veri = yukle()
        dil_yukle()
        self.aktif_tab = 'p'
        self.root_box = BoxLayout(orientation='vertical', padding=[14, 14, 14, 10], spacing=10)
        self.olustur()
        return self.root_box

    def olustur(self):
        self.root_box.clear_widgets()
        u = Kart(r=26, orientation='vertical', size_hint_y=0.20, padding=[12, 10, 12, 10], spacing=2)
        ust = BoxLayout(orientation='horizontal', size_hint_y=0.25)
        ust.add_widget(Label(text=dil('toplam'), font_size='13sp', color=MUT, bold=True))
        self.dil_btn = Buton(text=dil('dil_btn'), bg=CHI, tc=CYN, r=10, font_size='12sp', size_hint_x=0.18)
        self.dil_btn.bind(on_press=self.dil_degistir)
        ust.add_widget(self.dil_btn)
        u.add_widget(ust)
        self.tl = Label(text='0', font_size='55sp', bold=True, color=YEL, size_hint_y=0.55)
        u.add_widget(self.tl)
        u.add_widget(Label(text=dil('paket_ad'), font_size='12sp', color=MUT, bold=True, size_hint_y=0.20))
        self.root_box.add_widget(u)
        self.ic = BoxLayout(orientation='vertical', spacing=10)
        self.root_box.add_widget(self.ic)
        a = BoxLayout(size_hint_y=0.10, spacing=8)
        self.bp = Buton(text=dil('tab_paket'), bg=PUR, r=22)
        self.bt = Buton(text=dil('tab_takvim'), bg=CARD, tc=MUT, r=22)
        self.bm = Buton(text=dil('tab_maas'), bg=CARD, tc=MUT, r=22)
        self.bp.bind(on_press=lambda x: self.sp())
        self.bt.bind(on_press=lambda x: self.st())
        self.bm.bind(on_press=lambda x: self.sm())
        a.add_widget(self.bp)
        a.add_widget(self.bt)
        a.add_widget(self.bm)
        self.root_box.add_widget(a)
        self.gt()
        if self.aktif_tab == 'p':
            self.sp()
        elif self.aktif_tab == 't':
            self.st()
        elif self.aktif_tab == 'm':
            self.sm()

    def dil_degistir(self, inst):
        global dil_ayar
        dil_ayar = 'bg' if dil_ayar == 'tr' else 'tr'
        dil_kaydet()
        self.olustur()

    def gt(self):
        if hasattr(self, 'ti') and self.ti and self.ti.text.strip():
            tarih = self.ti.text.strip()
        else:
            tarih = date.today().isoformat()
        self.tl.text = str(gun_toplam(tarih))

    def rs(self, ak):
        self.bp.renk(CARD, MUT)
        self.bt.renk(CARD, MUT)
        self.bm.renk(CARD, MUT)
        if ak == 'p':
            self.bp.renk(PUR, TXT)
        elif ak == 't':
            self.bt.renk(CYN, DRK)
        elif ak == 'm':
            self.bm.renk(GRN, DRK)

    def tz(self):
        self.ic.clear_widgets()

    def sp(self):
        self.aktif_tab = 'p'
        self.rs('p')
        self.tz()
        self.ic.add_widget(Label(text=dil('gun_ekle'), font_size='20sp', bold=True, color=TXT, size_hint_y=0.06))
        k1 = Kart(r=20, orientation='horizontal', size_hint_y=0.11, padding=[15, 8, 15, 8], spacing=10)
        k1.add_widget(Label(text=dil('tarih'), font_size='15sp', color=MUT, size_hint_x=0.3, bold=True))
        self.ti = In(text=date.today().isoformat(), size_hint_x=0.7)
        self.ti.font_size = '18sp'
        self.ti.halign = 'center'
        k1.add_widget(self.ti)
        self.ic.add_widget(k1)

        k2 = Kart(r=20, orientation='horizontal', size_hint_y=0.15, padding=[15, 8, 15, 8], spacing=10)
        k2.add_widget(Label(text=dil('paket'), font_size='15sp', color=MUT, size_hint_x=0.3, bold=True))
        
        self.pi = In(input_type='number', size_hint_x=0.7)
        self.pi.font_size = '38sp'
        self.pi.halign = 'center'
        k2.add_widget(self.pi)
        self.ic.add_widget(k2)

        kz_kart = Kart(r=16, bg=CHI, orientation='vertical', size_hint_y=0.13, padding=[15, 8, 15, 8], spacing=2)
        kz_kart.add_widget(Label(text=dil('gun_kazanc'), font_size='12sp', bold=True, color=MUT, size_hint_y=0.35))
        self.kz = Label(text=dil('gun_kazanc_bekle'), font_size='22sp', bold=True, color=YEL, size_hint_y=0.65)
        kz_kart.add_widget(self.kz)
        self.ic.add_widget(kz_kart)

        kb = Buton(text=dil('kaydet'), bg=GRN, tc=DRK, r=20, size_hint_y=0.13, font_size='19sp')
        kb.bind(on_press=self.kt)
        self.ic.add_widget(kb)

        db = Buton(text=dil('dinlendim'), bg=RED, r=20, size_hint_y=0.11)
        db.bind(on_press=self.dt)
        self.ic.add_widget(db)

        self.dl = Label(text='', font_size='13sp', size_hint_y=0.10, color=GRN, bold=True)
        self.ic.add_widget(self.dl)

    def kt(self, inst):
        t = self.ti.text.strip()
        try:
            p = int(self.pi.text)
        except:
            self.dl.text = dil('sayi_gir')
            self.dl.color = RED
            return
        if not t:
            t = date.today().isoformat()
            self.ti.text = t
        kazanc = gunluk_kazanc(p)
        veri[t] = p
        kaydet(veri)
        self.gt()
        self.kz.text = '%.2f EUR' % kazanc
        self.kz.color = YEL
        self.dl.text = '%s -> %d %s' % (t, p, dil('kaydedildi'))
        self.dl.color = GRN
        self.pi.text = ''

    def dt(self, inst):
        t = self.ti.text.strip() or date.today().isoformat()
        veri[t] = 0
        kaydet(veri)
        self.gt()
        self.kz.text = dil('gun_kazanc_bekle')
        self.kz.color = YEL
        self.dl.text = '%s -> %s' % (t, dil('dinlenme'))
        self.dl.color = RED
        self.pi.text = ''

    def gun_sec(self, tarih):
        self.sp()
        self.ti.text = tarih
        self.gt()
        if tarih in veri:
            k = veri[tarih]
            if k == 0:
                self.dl.text = '%s -> %s' % (tarih, dil('izin_gunu'))
                self.dl.color = RED
            else:
                self.pi.text = str(k)
                kazanc = gunluk_kazanc(k)
                self.kz.text = '%.2f EUR' % kazanc
                self.kz.color = YEL
                self.dl.text = '%s -> %d %s' % (tarih, k, dil('kayitli'))
                self.dl.color = YEL
        else:
            self.dl.text = '%s -> %s' % (tarih, dil('henuz_yok'))
            self.dl.color = MUT

    def st(self):
        self.aktif_tab = 't'
        self.rs('t')
        self.tz()
        b = date.today()
        y = b.year
        mo = b.month
        AY = dil('aylar')
        self.ic.add_widget(Label(text='%s %d' % (AY[mo], y), font_size='22sp', bold=True, color=TXT, size_hint_y=0.06))
        kart = Kart(r=20, padding=[8, 8, 8, 8], size_hint_y=0.42)
        g = GridLayout(cols=7, spacing=3)
        for x in dil('gunler'):
            g.add_widget(Label(text=x, bold=True, font_size='11sp', color=MUT))
        c = calendar.Calendar(firstweekday=0)
        for hf in c.monthdayscalendar(y, mo):
            for gn in hf:
                if gn == 0:
                    g.add_widget(Widget())
                else:
                    gs = '%04d-%02d-%02d' % (y, mo, gn)
                    k = veri.get(gs)
                    if k is None:
                        rn = CHI
                        yt = MUT
                        al = '-'
                    elif k == 0:
                        rn = RED
                        yt = TXT
                        al = 'IZIN'
                    else:
                        rn = GRN
                        yt = DRK
                        al = str(k)
                    h = GunKart(r=10, bg=rn, orientation='vertical', padding=[1, 2, 1, 2], spacing=0, tarih=gs, callback=self.gun_sec)
                    h.add_widget(Label(text=str(gn), font_size='12sp', bold=True, color=yt))
                    h.add_widget(Label(text=al, font_size='8sp', color=yt))
                    g.add_widget(h)
        kart.add_widget(g)
        self.ic.add_widget(kart)

        tt = ay_toplam(y, mo)
        self.ic.add_widget(Label(text=dil('bonus_durumu'), font_size='18sp', bold=True, color=YEL, size_hint_y=0.06))
        bonus_kart = Kart(r=18, orientation='vertical', size_hint_y=0.42, padding=[12, 12, 12, 12], spacing=10)

        def bonus_satiri(hedef, para, anahtar, renk_aktif):
            kalan = max(hedef - tt, 0)
            satir = Kart(r=14, bg=CHI, orientation='vertical', size_hint_y=None, height=85, padding=[15, 8, 15, 8], spacing=2)
            if kalan == 0:
                ust_yazi = '%s  %d paket' % (dil(anahtar), hedef)
                ust_renk = renk_aktif
                alt_yazi = '%s  +%d EUR' % (dil('kazandin'), para)
                alt_renk = GRN
            else:
                ust_yazi = '%s  (%d paket)' % (dil(anahtar), hedef)
                ust_renk = TXT
                alt_yazi = '%d %s -> +%d EUR' % (kalan, dil('kalan'), para)
                alt_renk = renk_aktif
            l1 = Label(text=ust_yazi, font_size='17sp', bold=True, color=ust_renk, halign='left', valign='middle')
            l1.bind(size=l1.setter('text_size'))
            l2 = Label(text=alt_yazi, font_size='15sp', bold=True, color=alt_renk, halign='left', valign='middle')
            l2.bind(size=l2.setter('text_size'))
            satir.add_widget(l1)
            satir.add_widget(l2)
            bonus_kart.add_widget(satir)

        bonus_satiri(400, 40, 'bonus1', YEL)
        bonus_satiri(600, 60, 'bonus2', CYN)
        bonus_satiri(700, 80, 'bonus3', PUR)
        self.ic.add_widget(bonus_kart)

    def sm(self):
        self.aktif_tab = 'm'
        self.rs('m')
        self.tz()
        b = date.today()
        y = b.year
        mo = b.month
        tt = ay_toplam(y, mo)
        if tt == 0:
            bo = Kart(r=20, padding=20)
            bo.add_widget(Label(text=dil('kayit_yok'), font_size='20sp', color=MUT))
            self.ic.add_widget(bo)
            return
        mb, mn, ab, an, bonus, mn_bonuslu = hesapla(tt)
        i = min(tt, ESIK)
        f = max(tt - ESIK, 0)
        sc = ScrollView()
        bx = BoxLayout(orientation='vertical', size_hint_y=None, spacing=8, padding=[4, 4, 4, 4])
        bx.bind(minimum_height=bx.setter('height'))

        def ln(m, d, r=TXT, bg2=CARD):
            k = Kart(r=12, bg=bg2, orientation='horizontal', size_hint_y=None, height=48, padding=[15, 6, 15, 6])
            k.add_widget(Label(text=m, font_size='15sp', color=MUT))
            k.add_widget(Label(text=d, font_size='16sp', bold=True, color=r))
            bx.add_widget(k)

        def bs(m, r):
            bx.add_widget(Label(text=m, font_size='18sp', bold=True, color=r, size_hint_y=None, height=40))

        bs(dil('avans'), YEL)
        ln(dil('brut'), '%.2f EUR' % ab)
        ln(dil('kesinti') + ' %9', '-%.2f EUR' % (ab - an), RED)
        ln(dil('net_avans'), '%.2f EUR' % an, GRN, CHI)
        bx.add_widget(Label(text='', size_hint_y=None, height=8))
        bs(dil('maas_baslik'), CYN)
        ln('%s %d x 1.3293' % (dil('ilk'), i), '%.2f EUR' % (i * 1.3293792821))
        if f:
            ln('%s %d x 1.9941' % (dil('ustu'), f), '%.2f EUR' % (f * 1.9940689232))
        ln(dil('brut_maas'), '%.2f EUR' % mb)
        ln(dil('kesinti') + ' %23', '-%.2f EUR' % (mb - mn), RED)
        if bonus > 0:
            ln(dil('aylik_bonus'), '+%.0f EUR' % bonus, YEL)
        ln(dil('net_maas'), '%.2f EUR' % mn_bonuslu, GRN, CHI)
        bx.add_widget(Label(text='', size_hint_y=None, height=15))
        tk = Kart(r=22, bg=CHI, orientation='vertical', size_hint_y=None, height=110, padding=[15, 12, 15, 12], spacing=2)
        tk.add_widget(Label(text=dil('eline_gecen'), font_size='13sp', bold=True, color=MUT, size_hint_y=0.3))
        tk.add_widget(Label(text='%.2f EUR' % (an + mn_bonuslu), font_size='40sp', bold=True, color=YEL, size_hint_y=0.7))
        bx.add_widget(tk)

        bx.add_widget(Label(text='', size_hint_y=None, height=20))
        bs(dil('istatistik'), PUR)

        toplam, cal_gun, izin_gun, ort, en_iyi_t, en_iyi_d, en_kotu_t, en_kotu_d = aylik_istatistik(y, mo)
        AY = dil('aylar')
        def tarih_yazi(t):
            if not t:
                return '-'
            try:
                _, mm, dd = t.split('-')
                return '%d %s' % (int(dd), AY[int(mm)])
            except:
                return t

        stat_kart = Kart(r=14, bg=CHI, orientation='vertical', size_hint_y=None, height=290, padding=[18, 14, 18, 14], spacing=6)

        def stat_satir(etiket, deger, renk=TXT):
            s = BoxLayout(orientation='horizontal', size_hint_y=None, height=38)
            l1 = Label(text=etiket, font_size='15sp', color=MUT, halign='left', valign='middle')
            l1.bind(size=l1.setter('text_size'))
            l2 = Label(text=deger, font_size='16sp', bold=True, color=renk, halign='right', valign='middle')
            l2.bind(size=l2.setter('text_size'))
            s.add_widget(l1)
            s.add_widget(l2)
            stat_kart.add_widget(s)

        stat_satir(dil('stat_toplam'), str(toplam), YEL)
        stat_satir(dil('stat_calisilan'), str(cal_gun), GRN)
        stat_satir(dil('stat_izin'), str(izin_gun), RED)
        stat_satir(dil('stat_ortalama'), '%.1f' % ort, CYN)
        stat_satir(dil('stat_en_iyi'), '%s (%d)' % (tarih_yazi(en_iyi_t), en_iyi_d), GRN)
        stat_satir(dil('stat_en_kotu'), '%s (%d)' % (tarih_yazi(en_kotu_t), en_kotu_d), YEL)
        bx.add_widget(stat_kart)

        bx.add_widget(Label(text='', size_hint_y=None, height=10))
        bx.add_widget(Label(text=dil('toplam_paket') % tt, font_size='14sp', color=MUT, size_hint_y=None, height=30))
        sc.add_widget(bx)
        self.ic.add_widget(sc)

if __name__ == '__main__':
    PaketApp().run()
