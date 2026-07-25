# Pop-It Runner 3D 🌶️

Gerçek 3D (Three.js / WebGL) "satisfying pop-it runner" — TikTok/Shorts için dikey (9:16) hyper-casual oyun.

## Çalıştırma

`popit3d/index.html` dosyasını tarayıcıda açman yeterli (çift tıkla — internet gerekmez, Three.js `three.min.js` olarak yanında geliyor). Mobilde en iyi deneyim için telefonda dikey tam ekran aç.

## Nasıl oynanır

- **Basılı tut, bırakma:** Parmağın ekranda olduğu sürece 3D el, sıradaki objeye otomatik uzanıp patlatır (tek tek nişan almak yok).
- **Bırakınca** el durur; patlatılmayan baloncuklar şeritten kaçar → sağ üstteki hırsız yaklaşır. 3 kaçırmada bar bir miktar geri gider.
- **🌶️ Kırmızı biber:** El yanlışlıkla ona da basarsa ekran kızarır, alevler fışkırır, ekran sertçe sarsılır ve oyun 2 saniye donar — sonra **kaldığı yerden** devam eder (baştan başlamaz).
- **Tek bar:** Üstteki bar dolarken renk aşamaları otomatik değişir: 🟡 Sarı → 🟢 Yeşil → 🔵 Mavi → 🟣 Mor → 🔴 Kırmızı (MAX). Her aşamada hız ve biber sıklığı artar; geçişler ~1 sn yumuşak renk geçişiyle olur. Bar dolunca zafer ekranı.
- İlk kırmızı biber **4. objede** gelir; 0-4 sn arası ısınma (yavaş) bölümüdür.

## Teknik

- Gerçek 3D sahne: perspektif kamera (~55° kuş bakışı), yönlü ışık + yumuşak gölgeler (PCF), gerçek z-derinliği — 2D illüzyon değil.
- Three.js r147 (vendored, `three.min.js`), tek HTML dosyası, harici bağımlılık yok.
- Kontrol: `pointerdown` → basılı tutma, `pointerup`/`pointercancel` → durdurma, `touch-action: none`.
- Sesler WebAudio ile üretiliyor (pop perdesi combo ile yükselir); sağ üstteki 🔊 ile susturulabilir (Shorts'ta dış müzik için).
- Havuzlanmış objeler + paylaşılan geometri/malzeme; pixel ratio ≤ 2 — düşük/orta seviye telefonlarda 60 FPS hedefi.

## Tasarım kararları (dokümandaki açık uçlu maddeler)

- Hırsız mekaniği **korundu**, ama 3 kaçırma round'u bitirmek yerine **bar cezası** veriyor (video akışı kesilmesin diye).
- Opsiyonel bomba/yumruk engeli **eklenmedi** — tek engel kırmızı biber (doküman onaya bırakmıştı).
