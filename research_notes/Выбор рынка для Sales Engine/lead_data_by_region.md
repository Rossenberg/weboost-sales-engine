# Доступность, качество и стоимость лид-данных по регионам (B2B outbound, SMB, пример ниши: логистика/3PL/склады)

Дата исследования: 2026-10-03. Большинство цен и «точностей» взяты из блогов вендоров и агрегаторов (помечено «вендор»/«агрегатор»); независимых лабораторных тестов мало. Лимит инструментов (~15 вызовов) исчерпан, поэтому часть вопросов покрыта неполно (см. Gaps).

## 1. Платформы данных (Apollo, Instantly SuperSearch, ZoomInfo, Lusha, Hunter, Snov, Clay, Cognism, Kaspr, Lead411): покрытие по регионам, точность, API, цены, GDPR

### Takeaway
Для США самый дешёвый и достаточный вариант для малой команды: Apollo (от $49-79/seat/мес) или Instantly SuperSearch ($47/мес, ~1 000 верифицированных контактов); для Европы Cognism/Kaspr точнее по телефонам, но Cognism стоит ~$15-25K/год (нереально для малой команды), Apollo в Европе заметно слабее. Для России/СНГ эти платформы практически бесполезны (данных по РФ у них нет или мало; прямых источников не нашёл, см. Gaps).

### Cited Findings
- Apollo, планы (2026, агрегаторы): Free $0 (900 кредитов/год), Basic $49/seat/мес при годовой оплате ($65 помесячно), Professional $79 ($99), Organization $119 (мин. 3 места). Кредиты: email 1, телефон 8. Basic 30 000 кредитов/год, Pro 48 000, Org 72 000. API-доступ реально открывается на Professional и выше. Докупка кредитов ~$0.03-0.05/кредит. — [databar.ai](https://databar.ai/blog/article/apollo-pricing-2026), [saleshandy](https://www.saleshandy.com/blog/apolloio-pricing/), [hackingdemand](https://hackingdemand.com/blog/apollo-io-pricing-2026)
- Apollo: заявлено 275M+ контактов, US-first; email verify ~73% в «независимых тестах» по данным конкурента-агрегатора (Cognism-партнёрский контент, интерес предвзят). Apollo заявляет GDPR-комплаенс как Processor и Controller, ISO 27001, SOC2 Type II; систематический DNC-скрининг публично не описан. — [ZoomInfo Pipeline (конкурент)](https://pipeline.zoominfo.com/sales/apollo-vs-cognism), [cleanlist](https://www.cleanlist.ai/blog/2026-05-23-cognism-vs-apollo)
- Бенчмарк на 1 000 Apollo-email (2026, вендор верификации): после проверки ZeroBounce пропустил 888 адресов (bounce 3.7%), NeverBounce 711 (0.6%), MillionVerifier 709 (1.0%): т.е. ~29% email Apollo «невалидны/рискованны» по строгим верификаторам. — [агрегатор по поиску](https://wizleads.io/blog/email-verification-benchmark-2026/) (первичный источник цифр сам не открывал).
- Instantly SuperSearch: $47 / $97 / $197 в мес за пакеты кредитов (1 500-2 000 / 5 000-7 500 / 10 000-200 000); ~1.5 кредита на верифицированный email, т.е. $47 даёт ~750-1 000 контактов. — [prospeo (агрегатор)](https://prospeo.io/s/lead-search-engine) / [instantly.ai](https://instantly.ai/blog/hunter-email-search-alternatives/) (вендор). Публичного API лидгена у SuperSearch не подтверждено.
- Snov.io: Starter $39/мес = 1 000 кредитов; Pro $99 = 5 000 кредитов. Lusha: Pro $22.45/user/мес (3 000 кредитов/год), Premium $52.45 (7 200/год), телефон = 10 кредитов. Hunter: Free 25 поисков/50 верификаций, платный от $49 (500 поисков / 1 000 верификаций). — [instantly.ai](https://instantly.ai/blog/hunter-email-search-alternatives/), [clearout](https://clearout.io/blog/lusha-alternatives/), [moderninbound](https://moderninbound.com/blog/snov-io-vs-hunter)
- ZoomInfo: от ~$14 995/год (Professional), Elite $40K+, минимум 3 места, годовой контракт; медиана ~$31 875/год (агрегатор по 1 313 покупкам). Сильнее в Северной Америке; в 2025 расширил мобильные данные в 6 странах ЕС. Email-точность ~85% (Cognism-агрегатор) против ~83% у Cognism. — [pin.com](https://www.pin.com/blog/zoominfo-pricing/), [cognism.com](https://www.cognism.com/blog/zoominfo-european-data) (вендор-конкурент), [cleanlist](https://www.cleanlist.ai/blog/2026-03-07-cognism-vs-zoominfo)
- Cognism: EMEA-first, UK-основан, GDPR «legitimate interest», DNC-скрининг по 15 странам (ZoomInfo: 8); контракты $15-25K/год платформа + ~$1.5K/seat; средняя SMB-цена по данным spend-платформы ~$29K/год. — [cleanlist](https://www.cleanlist.ai/blog/2026-03-19-cognism-pricing-guide), [spendhound](https://www.spendhound.com/marketplace/cognism-pricing), [derrick-app](https://derrick-app.com/tools/cognism-pricing)
- Kaspr: заявляет 120M+ европейских контактов (вендор), сильнее Lusha в Европе по телефонам; Lusha: US/глобально. — [kaspr.io](https://www.kaspr.io/kaspr-vs-lusha), [zeliq](https://www.zeliq.com/blog/kaspr-vs-lusha-comparison)
- Clay (оркестратор «waterfall» по десяткам провайдеров), Lead411: цены и покрытие в этом прогоне не проверены.

### Inferences
- Для логистики/3PL малой команде в США: связка FMCSA (бесплатно, см. п.2) + Apollo/Instantly для поиска владельца/менеджера + верификатор. ZoomInfo/Cognism экономически не оправданы при <5 сотрудниках.
- Платформенные базы смещены в сторону компаний с LinkedIn-присутствием; микро-перевозчики и склады-SMB (владелец без LinkedIn) покрываются хуже; для них лучше реестры + карты.
- Так как «точность» у платформ почти всегда мерится вендорами, закладывать 25-30% потерь после верификации (по бенчмарку выше).

### Gaps
- Нет независимых данных о покрытии Apollo/Lusha и др. по России/СНГ и Азии; API-условия Clay/Lead411/Kaspr/Cognism, цена Clay и Lead411 не проверены. Реальные цены Cognism/ZoomInfo приведены по агрегаторам, не по официальным страницам (их нет в открытом доступе).

## 2. Публичные/официальные источники по регионам, наличие бесплатных API

### Takeaway
США (FMCSA) и Великобритания (Companies House) имеют бесплатные открытые данные, пригодные для автоматизации; Австралия (ABN Lookup) и Канада (Corporations Canada) бесплатны, но без контактов. В России бесплатного «полного» API нет: ФНС даёт данные бесплатно в HTML/PDF, а JSON/API платные у посредников; hh.ru закрыл публичный поиск вакансий (апрель 2026). СНГ-реестры: в основном без API.

### Cited Findings
- США, FMCSA: Census File (реестр моторных перевозчиков, ~1.6-2M активных) публикуется как открытые данные на data.gov; в записях есть телефон, адрес, число водителей/машин, у части email. Apify-акторы дают удобную обёртку. — [data.gov](https://catalog.data.gov/dataset/motor-carrier-registrations-census-files), [Apify](https://apify.com/logiover/fmcsa-motor-carrier-census-scraper). Важно: FMCSA покрывает перевозчиков/брокеров, но не складские 3PL (их нет в FMCSA, если нет авторизации брокера/экспедитора).
- США, Google Maps через Apify (Compass crawler-google-places): $1.5 за 1 000 мест на базовом уровне ($2.10 на Business-тарифе); обогащение (email с сайта, сотрудники) тарифицируется отдельно. Free-план $5 кредитов ≈ 3 000 мест. — [Apify](https://apify.com/compass/crawler-google-places), [use-apify](https://use-apify.com/blog/best-google-maps-scrapers-2026)
- Великобритания, Companies House API: бесплатный, лимит 600 запросов / 5 мин на ключ, данные по директорам (officers), PSC, SIC-коды (SIC-фильтрация по складам/логистике 52100 и др. — моё знание, не проверял источник). — [developer guidelines](https://developer.company-information.service.gov.uk/developer-guidelines), [leadistry](https://leadistry.co.uk/blog/companies-house-api-guide)
- Австралия, ABN Lookup: веб-сервисы бесплатны, нужен бесплатный GUID; отдаёт название, статус ABN, тип, штат, GST; контактов нет. — [ABR](https://abr.business.gov.au/Tools/WebServices)
- Канада: Corporations Canada публикует ежедневно обновляемые CSV федеральных корпораций под Open Government Licence (коммерческое использование разрешено); только федеральные, провинциальные реестры разрозненны. — [open.canada.ca](https://open.canada.ca/data/en/dataset/0032ce54-c5dd-4b66-99a0-320a7b5e99f2/resource/582644d6-e3a2-4fc6-a647-a07d81cc8104), [ISED](https://ised-isde.canada.ca/site/corporations-canada/en/data-services)
- Россия, ФНС/ЕГРЮЛ: почти все данные бесплатно в HTML/PDF на egrul.nalog.ru; JSON/XML платно у посредников. API-ФНС: 100 запросов/сутки бесплатно, остальное платно; также DaMIA, ofdata.ru. — [vc.ru](https://vc.ru/money/385736-egryul-egrip-v-vide-arhivov-fns-csv-xml-json-api-i-analiz-dannyh), [api-fns.ru](https://api-fns.ru/api_help), [ofdata](https://ofdata.ru/api)
- Россия, платные API: Контур.Фокус API от ~30 000 ₽/мес (агрегатор; другой источник: «базовые данные до 3 000 компаний 96 000 ₽ на 12 мес»); DaData от 4 900 ₽/мес, 10K запросов/мес бесплатно, минимум ~14 000 ₽/год. — [a2is.ru](https://a2is.ru/catalog/proverka-kontragentov/compare/dadata/focus-kontur), [focus-kontur.ru](https://focus-kontur.ru/api/stoimost/)
- Россия, Rusprofile: собственного API нет; тарифы 940 ₽/мес (6 750 ₽/год) Базовый, 1 990 ₽/мес (19 100 ₽/год) Эксперт. Парсинг сайта — серая зона. — [rusprofile.ru](https://www.rusprofile.ru/subscribe), [pawetta](https://pawetta.com/servisy/rusprofile/)
- Россия, СПАРК: цена/API не проверялись.
- Россия, карты: 2ГИС и Яндекс Карты имеют официальные платные API (Places), плюс множество парсеров (open-source parser-2gis, расширения). Парсеры выдают адрес, телефоны, сайт, иногда email/мессенджеры. — [vc.ru](https://vc.ru/marketing/3034706-parsery-yandeks-kart-i-2gis-besplatnyj-sbor-dannyh), [GitHub parser-2gis](https://github.com/interlark/parser-2gis). Лицензионные условия 2ГИС/Яндекса на массовую выгрузку не проверены.
- Россия, hh.ru: с апреля 2026 публичный `GET /vacancies` отдаёт 403 для неавторизованных запросов; ключ — только работодателям/рекрутинговым сервисам с модерацией. То есть вакансии как intent-сигнал теперь только через платные агрегаторы/ручной просмотр. — [Habr](https://habr.com/ru/news/1069286/), [dev.hh.ru](https://dev.hh.ru/admin/developer_agreement)
- Казахстан: реестр юрлиц (~2.27M записей) есть у коммерческих агрегаторов (companydata.com, REST API платный); открытого официального API не подтверждено; OpenCorporates оценивает открытость невысоко. — [companydata](https://companydata.com/database/company-database-kazakhstan/), [OpenCorporates](http://registries.opencorporates.com/jurisdiction/kz)
- Армения: e-register.am доступен для поиска бесплатно, но на май 2026 публичного API нет; есть сторонние обёртки (Apify). — [businessdataguide](https://www.businessdataguide.com/blog/jurisdictions/armenia-company-search-guide), [Apify](https://apify.com/reestri/am-company-lookup)
- Грузия: реестр NAPR (enreg.reestri.gov.ge) с поиском по названию/ID, данные по директорам/партнёрам; официального открытого API не подтверждено, выгрузка в OpenSanctions. — [enreg.reestri.gov.ge](https://enreg.reestri.gov.ge/main.php?m=new_index&l=en), [OpenSanctions](https://www.opensanctions.org/datasets/ext_ge_company_registry/)
- Страны ЕС (Германия Handelsregister, Франция INSEE/Sirene, Нидерланды KvK и др.): в этом прогоне не исследованы.

### Inferences
- Реестры дают «скелет» (название, адрес, ОКВЭД/SIC, директор), но почти никогда email. Рабочий пайплайн: реестр/карты -> сайт компании -> email-finder/ручной поиск -> верификация.
- Для РФ единственный дешёвый автоматизируемый путь: ФНС-выгрузки + 2ГИС/Яндекс + парсинг сайтов; hh.ru-сигнал потерян.

### Gaps
- Не проверены: ЕС-реестры (Handelsregister, Sirene, KvK), провинциальные реестры Канады, state SoS США, СПАРК, официальные условия 2ГИС/Яндекс API, ограничения FMCSA Terms на коммерческое использование, свежесть email в FMCSA.

## 3. Инструменты верификации email: цена и точность

### Takeaway
Для малой команды достаточно MillionVerifier (~$3.7/1 000) или встроенной верификации Instantly; ни один инструмент не решает catch-all. Цифры точности в основном вендорские.

### Cited Findings
- Цены за 1 000 проверок (вендор Instantly, 2026): ZeroBounce ~$10, NeverBounce ~$8, MillionVerifier ~$3.70; Instantly включает верификацию во flat-fee (~$8-16/1 000). Заявленная точность 97-99%+; независимые сравнения дают 95%+ для топ-инструментов и 87-95% для бюджетных. Бенчмарк Instantly основан на вендорских заявлениях, не на собственном тесте. — [instantly.ai](https://instantly.ai/blog/2026-email-verification-benchmark-accuracy-scores-for-8-top-tools/)
- Catch-all: ZeroBounce даёт AI-скор уверенности; NeverBounce и MillionVerifier помечают как risky; рекомендация — исключать либо принимать повышенный bounce. — [instantly.ai](https://instantly.ai/blog/2026-email-verification-benchmark-accuracy-scores-for-8-top-tools/), [mailsfinder](https://mailsfinder.com/compare/zerobounce-vs-neverbounce-vs-millionverifier)
- Тест на 1 000 Apollo-адресов: bounce после верификации ZeroBounce 3.7%, NeverBounce 0.6%, MillionVerifier 1.0% (но ZeroBounce пропустил больше адресов). — [wizleads (агрегатор)](https://wizleads.io/blog/email-verification-benchmark-2026/)
- Другая оценка: NeverBounce 99.9% (4 995 из 5 000), ZeroBounce 99.0% — вендорский/аффилированный тест. — [zerobounce.net](https://www.zerobounce.net/zerobounce-vs-millionverifier) (вендор)

### Inferences
- Стоимость верификации 1 000 контактов (с запасом на повторы) $4-10, т.е. небольшая доля общей стоимости.
- Российские почты (mail.ru, yandex) и корпоративные домены часто catch-all или блокируют SMTP-пробинг — по общим знаниям, источником не подтверждено; точность зарубежных верификаторов для РФ-доменов вероятно ниже.

### Gaps
- Нет независимого теста верификаторов на русскоязычных доменах (.ru) и на логистических SMB.

## 4. Определение ЛПР (owner/CEO/COO), LinkedIn, легальность, малый бизнес РФ и 152-ФЗ

### Takeaway
В США/Европе ЛПР ищется через LinkedIn-производные базы (Apollo, Cognism) и реестры (UK: директора и PSC). В РФ владелец юрлица/ИП известен из ЕГРЮЛ/ЕГРИП (ФИО, ИНН), но контакты приходится искать отдельно; персональные данные под 152-ФЗ с крупными штрафами с 2025.

### Cited Findings
- Scraping LinkedIn (США): Ninth Circuit в hiQ v. LinkedIn счёл скрейпинг публичных данных не нарушением CFAA, но дело закончилось разбирательством по ToS и мировым соглашением: $500 000 против hiQ, уничтожение данных и запрет. GDPR/CCPA и ToS остаются рисками. — [Apify blog](https://blog.apify.com/hiq-v-linkedin/), [natlawreview](https://natlawreview.com/article/hiq-and-linkedin-reach-proposed-settlement-landmark-scraping-case), [apiserpent](https://apiserpent.com/blog/is-scraping-linkedin-legal-2026)
- Великобритания: Companies House отдаёт officers и PSC (владельцы), т.е. ФИО директора бесплатно (источник: [Companies House API guide](https://leadistry.co.uk/blog/companies-house-api-guide)); email нужно искать отдельно.
- Россия, 152-ФЗ: с 30 мая 2025 штрафы за повторную утечку ПДн — до 3% годовой выручки и не менее 20 млн ₽ (ранее до 300 тыс. ₽); передача ПДн третьим лицам — до 5 млн ₽ для организаций; непредоставление уведомления в РКН — до 300 тыс. ₽. — [Robokassa](https://robokassa.com/blog/news/tsena-oshibki-pochemu-kompanii-mogut-poteryat-milliony-iz-za-novogo-zakona-o-personalnykh-dannykh/), [workspace.ru](https://workspace.ru/blog/izmeneniya-v-zakone-152-fz-pochemu-teper-za-rassylku-mozhno-poluchit-gigantskiy-shtraf/) (блоги, не текст закона)
- Россия, холодный email: регулируется 38-ФЗ «О рекламе» (штраф до 500 000 ₽ для юрлиц) и 152-ФЗ; использование рабочих email из открытых источников для деловой переписки считается допустимым, личные контакты из соцсетей — нет; массовые шаблонные рассылки по купленным/спарсенным базам — прямой путь к нарушению. Практика вендора Coldy: 150M писем, 1 жалоба в ФАС, штраф 3 000 ₽ (вендорская статистика). — [coldy.ai](https://coldy.ai/guides/email-outreach-russian-advertising-law-guide-2025), [companylist.ru](https://companylist.ru/holodnye-b2b-pisma-v-rossii-kotorye-chitayut-polnoe-rukovodstvo-ot-yuridicheskoj-bezopasnosti-do-vysokoj-konversii/)
- Россия: ЕГРЮЛ/ЕГРИП и данные Фокуса/ofdata включают ФИО руководителя/учредителя, ИНН, часть контактов компании (phone/email из публичных источников). — [ofdata](https://ofdata.ru/api), [Контур.Фокус](https://sc-kontur.ru/focus/focus_api)

### Inferences
- В РФ у ИП/микро-бизнеса телефон владельца часто равен телефону компании (ИП = физлицо), т.е. юридически это ПДн; безопаснее таргетить юрлица (ООО) и общие корпоративные адреса, работать как «деловое обращение» с указанием источника контакта.
- Telegram-аккаунт владельцев: источников данных (баз, парсеров) в этом прогоне не нашёл по надёжным ссылкам; сам по себе парсинг Telegram по номеру — серая зона.
- Для малой команды риск 152-ФЗ в основном административный (РКН/ФАС), но не нулевой; нужна юридическая консультация.

### Gaps
- Не проверено: законность парсинга LinkedIn в ЕС (решения DPA по Clearview-подобным кейсам), судьба Proxycurl, доступность контактов владельцев МСБ в РФ (телефоны/email/Telegram) по надёжным источникам, КЗ/АРМ/ГРУЗ законы о ПДн.

## 5. Каналы по регионам (email vs phone vs Telegram vs WhatsApp)

### Takeaway
США/ЕС/UK/AU/CA: email + телефон (LinkedIn как дополнение); Россия/СНГ: Telegram/звонки/WhatsApp (в РФ WhatsApp ограничивался), email работает, но с юридическими ограничениями и низкой доставляемостью российских доменов; точных цифр нет.

### Cited Findings
- Email остаётся основным B2B-каналом в США и Европе последние три года и работает в России; Telegram-лидоген в РФ строится на чатах, каналах и личных сообщениях, боты не должны рассылать автоматом (спам/ФЗ «О рекламе»). — [coldy.ai](https://coldy.ai/blog/b2b-lead-generation-channels-russia-2025), [salesnotes.ru](https://salesnotes.ru/tpost/tkl4mogtn1-holodnie-pisma-telegram-ili-reklama-kana)
- UK/ЕС: телефоны сверяются с DNC-списками (Cognism 15 стран, ZoomInfo 8), для холодных звонков/SMS нужны проверки по регуляциям (PECR/GDPR). — [cognism.com](https://www.cognism.com/blog/zoominfo-european-data)
- Европа GDPR: B2B outreach на «legitimate interest» допустим с возможностью отписки; провайдеры Cognism/Kaspr позиционируются как GDPR-aligned (вендорские заявления).

### Inferences
- WhatsApp в РФ/СНГ: ситуация с блокировками и лимитами менялась; свежих данных не нашёл. Для СНГ (КЗ, Армения, Грузия) WhatsApp и Telegram на практике основные мессенджеры (общее знание, не проверено).

### Gaps
- Нет статистики открытий/ответов по каналам в РФ/СНГ из надёжных источников; нет данных по доставляемости email на российские домены.

## 6. Ориентировочная стоимость в месяц: найти и верифицировать ~1 000 контактов

### Takeaway
США — $50-150/мес; UK/EU/CA/AU — $100-250/мес при ручной сборке из реестров + платформа, на Cognism — на порядок выше; Россия — порядка 5-20 тыс. ₽ деньгами, но существенное время/юридический риск. Все цифры — мои оценки на основе процитированных цен, а не вендорские заявления.

### Cited Findings (исходные цены для расчёта)
- Instantly SuperSearch $47 за ~750-1 000 верифицированных контактов; Apollo Basic $49/seat при 30 000 кредитов/год (при 1 кредит = 1 email это ~2 500/мес); MillionVerifier ~$3.70/1 000; Apify Google Maps $1.5/1 000 мест; Companies House/ABN/FMCSA бесплатно; DaData от 4 900 ₽/мес; Контур.Фокус API от ~30 000 ₽/мес; Rusprofile 940-1 990 ₽/мес. Источники: см. разделы 1-3.

### Inferences (оценки)
- США: FMCSA (бесплатно) + Apollo Basic/Pro ($49-79) + MillionVerifier ($4) + Apify ($2-5) = ~$60-100/мес на 1 000 контактов; при потерях ~30% на верификации нужно закладывать ~1 400 исходных записей (~$80-130).
- UK/EU/CA/AU: Companies House/ABN/CA CSV бесплатно + Apollo ($49-79) или Snov/Kaspr (~$40-100) + верификация ($4-10) = ~$100-200/мес; на Cognism вход $15K+/год (~$1 250+/мес).
- Россия: ФНС-выгрузки (бесплатно) или DaData (4 900 ₽) + 2ГИС/Яндекс парсер (бесплатно-несколько тысяч ₽) + ручной/полуавтоматический поиск контактов + верификация: порядка 5-15 тыс. ₽/мес деньгами; основная стоимость — время и юридический риск. Фокус API (30 000 ₽/мес) для малой команды избыточен.
- СНГ (КЗ/АРМ/ГРУЗ): в основном карты + ручной поиск + мессенджеры; денежные затраты малы, но автоматизация и качество ниже (нет открытых API).

### Gaps
- Нет реальных замеров выхода валидных контактов на 1 000 запросов в нише логистики; не проверены цены Clay, Lead411, СПАРК.
