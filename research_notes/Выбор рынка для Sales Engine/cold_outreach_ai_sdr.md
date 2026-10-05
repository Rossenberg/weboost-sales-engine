# Эффективность B2B cold outreach и ландшафт AI-SDR (2025-2026)

Примечание: ~25 вызовов поиска/загрузки. Большая часть цифр — вендорский маркетинг (вендоры продают инструменты/услуги) и страдает от survivorship bias. Определения "reply rate" у источников РАЗНЫЕ (см. первый раздел) — прямое сравнение цифр некорректно.

## 1. Бенчмарки cold email 2025-2026

### Takeaway
Цифры расходятся в ~8 раз из-за методологии: Instantly (платформа, активные пользователи) — средний reply rate 3.43%, Belkins (агентские кампании, replies/sent без автоответов) — 0.45%. Реалистичная ожидаемая воронка для агентства: 0.5-2.5 встреч на 100 писем у Belkins; у "хороших" кампаний 5-10% reply. Малые компании (0-10 чел.) и founders отвечают лучше крупных.

### Cited Findings
- Instantly 2026 report (период 1 янв – 18 дек 2025, "миллиарды" писем, 700k+ бизнесов): средний reply rate 3.43%; top quartile 5.5%+; top 10% 10.7%+; 58% ответов приходят с шага 1, 42% с фолоу-апов; оптимальная последовательность 4-7 касаний; письмо <80 слов; bounce <2% считается нормой; лучший день — среда. В отчёте НЕТ разбивки по индустриям/размерам и отдельного positive reply — [Instantly](https://instantly.ai/cold-email-benchmark-report-2026). Bias: выборка только активных пользователей платформы, вендор продаёт инструмент.
- Belkins 2026 study (7 530 489 писем, 34 393 ответа, кампании 2025): средний reply rate 0.45% (replies / sent, без автоответов и bounce; в прошлые годы считали от открывших — поэтому цифры не сопоставимы со старыми отчётами); >1 200 назначенных встреч из 7.5M писем (~0.016% от отправленных); пик в феврале 0.54%, декабрь 0.35% — [Belkins](https://belkins.io/blog/cold-email-response-rates). Bias: кампании клиентов агентства Belkins (в основном B2B-услуги/tech), тренд вниз.
- Belkins по размеру компании: 0-10 сотрудников 0.72%; 11-50 — 0.49%; 10 000+ — 0.22%. По должности: founders/owners 0.57%, C-level 0.42%, VP 0.32% — [Belkins](https://belkins.io/blog/cold-email-response-rates).
- Belkins по индустриям: Food&Beverage 3.47%, Construction 0.60%, Financial Services 0.59%, Healthcare 0.57%, Legal 0.56% (Education/Government ~1.8%, Banking/Insurance ~0.25% — приблизительные значения из пересказа страницы, не точные) — [Belkins](https://belkins.io/blog/cold-email-response-rates).
- Belkins по странам: Польша 1.43%, Ирландия 0.74%, Дания 0.73%, Канада 0.63%, США 0.51%, Великобритания 0.48% — [Belkins](https://belkins.io/blog/cold-email-response-rates). Лучшее время 8:00-12:00 (0.54%), Ср/Чт 0.48%.
- Woodpecker (20M+ писем, 1000+ клиентов, 52 страны; в статье также цитируются Belkins 16.5M и Instantly): reply rate по размеру списка: <50 контактов 5.8%; 50-200 — 4-5%; 200-500 ~3%; 500-1000+ 2.1%. Средний bounce 5.1%; "хорошо" <2%, "отлично" <1.5%. 3-5 фолоу-апов: 8.3% против 4.1% без фолоу-апов. Продвинутая персонализация 17-18% против 7-9% базовой. Часть цифр — агрегат чужих данных — [Woodpecker](https://woodpecker.co/blog/cold-email-statistics/).
- Метрики воронки по умолчанию у MailDeck (инфраструктурный вендор, 833K+ ящиков): reply 2-5% (дефолт 3.5%), positive reply 10-20% от ответов (дефолт 15%), booking 25-40%, show 65-80% — это допущения калькулятора, не измерения — [MailDeck](https://maildeck.co/blog/cold-email-cost-per-lead/).
- Агрегаторы утверждают падение reply rate с 7% до 5.1% в 2024→2025 (первоисточник не проверен) — [GigRadar](https://gigradar.io/blog/digital-marketing-agency-lead-generation).
- Данные Smartlead, Lemlist, Apollo, Backlinko, прямого positive reply rate по индустриям — в этом прогоне НЕ получены (см. Gaps).

### Inferences
- Для расчёта юнит-экономики консервативнее брать Belkins-подобные (0.4-0.7% reply, 0.5-2 встречи/100 контактов при ХОРОШЕМ таргетинге? — нет, 0.5-2.5% оценка идёт из вторичного пересказа; сам Belkins даёт ~0.016% на все письма), а оптимистичный сценарий — Instantly top-quartile. Разброс на 1-2 порядка по встречам.
- Малые лист-сегменты (<50 контактов, 5.8%) = в пользу узкого ICP и ручной/AI-персонализации вместо масс-рассылки, при этом малые компании (0-10 чел.) отвечают лучше (0.72%) — это целевой сегмент SMB-услуг.

### Gaps
- Нет точных positive reply rate и meeting rate по индустриям/размерам от Instantly/Smartlead/Lemlist/Apollo.
- Не проверены первоисточники для "Belkins 0.5-2.5% meeting rate" (вторичный пересказ поиска).

## 2. Изменения доставляемости (Google/Yahoo/Microsoft)

### Takeaway
Правила формально бьют по отправителям 5 000+ писем/день на один домен получателя, но спам-порог 0.3% (цель <0.10%) и требования аутентификации де-факто применимы ко всем. Малый отправитель с 2-10 ящиками формально ниже порога, но на практике должен иметь SPF+DKIM+DMARC и держать жалобы <0.1%.

### Cited Findings
- Google (официальная справка): все отправители — SPF или DKIM, PTR (forward/reverse DNS), TLS, формат RFC 5322; 5 000+ сообщений/день — обязательно DMARC, выравнивание From с SPF/DKIM, one-click unsubscribe для маркетинговых писем; спам-рейт в Postmaster Tools держать <0.3%, рекомендуется <0.10% — [Google](https://support.google.com/a/answer/81126).
- С ноября 2025 Gmail усиливает применение: неподходящие письма могут временно ограничиваться по скорости или отклоняться навсегда (по вторичным источникам) — [Proofpoint](https://www.proofpoint.com/us/blog/email-and-cloud-threats/clock-ticking-stricter-email-authentication-enforcements-google-start); [PowerDMARC](https://powerdmarc.com/google-and-yahoo-email-authentication-requirements/).
- Yahoo: рекомендует спам-рейт <0.3% (с февраля 2024 вместе с Google) — [PowerDMARC](https://powerdmarc.com/google-and-yahoo-email-authentication-requirements/).
- Microsoft (Outlook.com/Hotmail/Live): с 5 мая 2025 домены 5 000+ писем/день должны проходить SPF, DKIM и иметь DMARC минимум p=none с выравниванием; несоответствующие письма отклоняются, а не уходят в junk; нужны рабочие From/Reply-To, one-click unsubscribe, гигиена списков — [dmarcian](https://dmarcian.com/microsoft-enforces-spf-dkim-dmarc/); [DMARCwise](https://dmarcwise.io/blog/outlook-new-requirements-2025). Применимо к consumer-доменам Microsoft, не к корпоративному Microsoft 365 (из пересказа — уточнить).
- Warm-up (вендорские данные, bias): новые домены без прогрева 25-30% (или 40-70%) inbox placement против 80-95% с прогревом; безопасно 20-50 писем/ящик/день, на новых доменах 5-15 первые 4 недели, 2-3 ящика на домен, 14+ дней прогрева — [Instantly](https://instantly.ai/blog/how-to-achieve-90-cold-email-deliverability-in-2025/); [MailReach](https://www.mailreach.co/blog/gmail-warmup); [Growth Engineer](https://growthengineer.ai/blog/cold-email-deliverability-2026). Цифры разных вендоров противоречат друг другу (25-30% vs 40-70%), независимой проверки нет.
- Инфраструктура: Google Workspace ящик ~$2.99-3.90, ~20 писем/день (~$5.91 за 1K писем); Outlook-ящики $0.30-0.40 при 4-10/день — [MailDeck](https://maildeck.co/blog/cold-email-cost-per-lead/).

### Inferences
- Для 2-10 ящиков (~40-300 писем/день) порог 5 000/день не достигается, но Gmail применяет репутационные фильтры ко всем; ключевое — отдельные домены для рассылки, DMARC, bounce <2%, жалобы <0.1%, верификация списков.
- Пропускная способность малого отправителя жёстко ограничена: 5 ящиков × 20-30/день ≈ 100-150 новых контактов/день ≈ 2 000-3 000/мес.

### Gaps
- Нет независимых (не от вендоров прогрева) данных об эффективности warm-up.
- Не проверены официальные страницы Yahoo/Microsoft напрямую.

## 3. AI-персонализация vs шаблоны; AI-disclosure; отношение получателей

### Takeaway
Данные сильно противоречивы и почти все вендорские: от +57% до 5x. Контролируемых A/B-тестов на раскрытие AI в cold email найти не удалось. Опросы показывают, что большинство получателей не против AI, но почти половина говорит, что ответила бы реже.

### Cited Findings
- Заявленные результаты AI-персонализации: 18% vs 3.4% (5.2x) у вендоров; 4.6% AI vs <1% шаблонные у другого; +57% lift "при корректных данных"; 50-250% прирост персонализации — все вендорские блоги без раскрытых выборок — [HighTicketAISystems](https://highticketaisystems.com/blog/ai-personalization-cold-email-reply-rates); [Unify](https://www.unifygtm.com/explore/cold-email-ab-testing). Для статистически значимого 20% лифта нужно ~1 500 писем на вариант.
- Woodpecker: расширенная персонализация 17-18% vs 7-9% базовой (≈2x) — [Woodpecker](https://woodpecker.co/blog/cold-email-statistics/).
- Hunter.io (размер выборки и дата не указаны, обновлено 24.11.2025): 67% decision-makers не против AI-писем; 47% менее вероятно ответили бы, если подумали бы что письмо от AI — [Hunter](https://hunter.io/blog/the-cold-email-confidence-gap-why-senders-fear-ai-more-than-decision-makers).
- Обнаружение: Bynder (2 000 потребителей) — 50% отличили AI-текст; Validity (1 000 потребителей) — 43% уверены, что отличат; другое исследование — 83% — [SalesHandy](https://www.saleshandy.com/blog/ai-vs-human-cold-emails/); [MagicTeams](https://blog.magicteams.ai/blog/does-disclosing-ai-emails-hurt-response-rates/).
- Раскрытие AI: прямых A/B по cold email нет; косвенно: Meltwater/YouGov (9 869 взрослых, 7 стран) — 86% считают, что бренды должны раскрывать AI-контент; Gartner (1 539 US потребителей) — половина предпочитает контент без GenAI; PNAS Nexus — маркировка AI не снижала убедительность; опрос 1 455 пациентов — падение удовлетворённости 0.13/5 при раскрытии — [MagicTeams](https://blog.magicteams.ai/blog/does-disclosing-ai-emails-hurt-response-rates/). Автор там сам признаёт отсутствие email-A/B.
- Агентское наблюдение: "AI-звучащие" письма (формульная структура, обилие прилагательных) режут отклик — [Hunter](https://hunter.io/blog/the-cold-email-confidence-gap-why-senders-fear-ai-more-than-decision-makers).

### Inferences
- Хук "я AI-ассистент" как открытая гипотеза: нет данных ни за, ни против; потребуется собственный A/B (≥1 500 писем на вариант — для малого отправителя это ~1 месяц объёма).
- Реальный эффект персонализации скорее ~1.5-2x (Woodpecker), а 5x — маркетинг.

### Gaps
- Нет публичных A/B-тестов AI vs шаблон с раскрытыми выборками от нейтральных источников.
- Нет данных о раскрытии AI именно в cold email.

## 4. Рынок AI-SDR: продукты, цены, провалы

### Takeaway
Рынок перегрет: дорогие годовые контракты (11x ~$36k/год; Artisan $2-5k/мес), высокая текучесть (оценки 50-80% отмены за 3 месяца), реальные кейсы требуют 15-20 ч/нед человеческого надзора. Доказательная база — вендорская; независимых контролируемых тестов нет.

### Cited Findings
- Цены: 11x (Alice) ~$36 000/год, обычно $50-60k в первый год, годовой контракт; Artisan ~$280-5 000+/мес (самообслуживаемые планы $280-660/мес; нормальные объёмы $1.5-5k/мес; годовой контракт $18-24k и выше); AiSDR $900-2 500/мес; Clay $185-495/мес (кредиты); Regie.ai Free/Pro $49/мес/Enterprise — [Altitude pricing index](https://altitudebiz.dev/notes/ai-sdr-pricing-index); [SalesRobot](https://www.salesrobot.co/blogs/artisan-ai-review); [MarketBetter](https://marketbetter.ai/blog/artisan-ai-pricing-2026/). Цены Apollo, Instantly, Amplemarket не найдены. Цены вторичные, актуальность не гарантирована.
- Типично $500-1 500/мес на место mid-market; человек-SDR $90-130k/год fully loaded; ориентир стоимости встречи: AI $20-200 (лучшие случаи) против человек $250-900; автор отмечает "нет публичных контролируемых A/B-исследований AI vs человек по closed revenue" — [SushiData](https://sushidata.com/blog/2026/03/24/the-state-of-the-ai-sdr-in-2026/).
- SaaStr/Artisan (кейс опубликован самим вендором): ~6 недель, 6 892 письма (3 574 новым лидам), positive response rate 3.55-3.6%, LinkedIn-принятие 49.4% — [Artisan case](https://www.artisan.co/casestudies/saastr). Lemkin: "cost per lead $52", "$1M+ pipeline за 90 дней" с несколькими AI-агентами, но 15-20 ч/нед ручного надзора — [Artisan blog](https://www.artisan.co/blog/the-best-ai-sdrs); [post-mortem](https://deathtocoldemails.com/ai-sdr-post-mortem/).
- 11x (по post-mortem блога deathtocoldemails — независимый автор, не расследование): заявленный ARR $14M против ~$3M после оттока; 70-80% клиентов уходили в течение 3 месяцев (12-мес контракты с 3-мес break clause); ZoomInfo (пилот янв-фев 2025) и Airtable числились клиентами после отказа; ZoomInfo направил cease-and-desist — [post-mortem](https://deathtocoldemails.com/ai-sdr-post-mortem/). Требует перепроверки по первоисточникам (TechCrunch и т.д. не загружены).
- Artisan: CEO признал "довольно низкий response rate" и "относительно высокий churn" первого поколения и "очень плохие галлюцинации" на старте; LinkedIn заблокировал компанию ~19 дек 2025 – начало янв 2026 (~2 недели) из-за использования бренда и скрапинга данных вендорами; G2 ~3.5; оценка "50-70% managed-AI-SDR контрактов отменяются за 90 дней" (вторичная оценка, источник неясен) — [Salesmotion](https://salesmotion.io/blog/ai-sdr-tools-compared); [post-mortem](https://deathtocoldemails.com/ai-sdr-post-mortem/). Анекдот: 20 000+ сообщений и 3 000 LinkedIn-заявок — 0 встреч.
- Категории: автономные (AiSDR), AI-first SEP (Regie, Reply), SEP с AI (Outreach, Salesloft, Apollo, HubSpot), копилоты (SellScale, Warmly) — [SushiData](https://sushidata.com/blog/2026/03/24/the-state-of-the-ai-sdr-in-2026/).
- Много источников про 11x/Artisan — конкуренты (11x.ai публикует "Artisan review", Artisan — "vs 11x"): нужна осторожность.

### Inferences
- Для сервис-бизнеса с 2-10 ящиками AI-SDR платформы за $20-60k/год экономически неоправданны; конкурентная альтернатива — Clay/сборка (n8n + верифицированные данные) на $200-700/мес.
- Эффект насыщения: рост объёма писем при стабильном среднем reply (Instantly) и тренд Belkins вниз (0.54%→0.35% за 2025) указывают на растущую усталость inbox.

### Gaps
- Нет подтверждённых цен Apollo AI, Instantly AI, Amplemarket; нет G2/Trustpilot отзывов напрямую (только пересказы).
- Не проверены первоисточники скандала 11x.

## 5. Реальные кейсы агентств/соло-основателей

### Takeaway
Публичных кейсов с полной воронкой (письма → ответы → встречи → сделки → выручка → затраты) почти нет; большинство — маркетинг агентств, продающих cold email. Реальные малые кейсы — единичные и без подтверждения.

### Cited Findings
- DesignScript (маркетинговое агентство, кейс на сайте SalesBlink — вендорский): 30 000+ писем за 3 мес, ~1 073 положительных ответа, 50+ закрытых сделок, "$10M+ pipeline" — [SalesBlink](https://salesblink.io/case-studies/designscript-marketing-agency). Не верифицируемо; 83% open rate нереалистичен при текущем трекинге.
- Агентство (кейс outboundsystem.com): 35 встреч за 3 мес при средней сделке $20K; Luminize — 20 встреч за 2.5 мес — [Outbound System](https://outboundsystem.com/) (вендорский).
- Michel Lieben (ColdIQ): "4 000 писем → 1 лид" в начале, затем $4M+ ARR, 30 человек (самоотчёт в LinkedIn) — [LinkedIn](https://www.linkedin.com/posts/michel-lieben_how-it-started-4000-cold-emails-sent-1-activity-7320031280744603648-aMPN).
- Агентство лидгена (Indie Hackers): 3-6 новых клиентов в среднем при reply 3-20%; "80% таргетинг / 20% месседж" — [Indie Hackers](https://www.indiehackers.com/post/from-targeting-to-iteration-how-we-use-cold-emails-to-get-paying-clients-4e3d34744b).
- Anythoughts.ai (DEV): 10 AI-персонализированных писем маркетинговым агентствам (30→14→10 контактов), 18 минут, 0 ответов в день 1; узкое место — верифицированные контакты, а не копирайт — [DEV](https://dev.to/alex_wu_anythoughts_ai/we-built-an-ai-agent-to-write-cold-emails-then-we-used-it-to-sell-itself-18ib). Выборка нерепрезентативна.
- ColdClicks (IH): 21%+ reply, 6 trial, 1 paid conversion (малая выборка) — [Indie Hackers](https://www.indiehackers.com/post/our-first-customer-with-personalized-cold-email-d0940bcc57).
- Стоимость инфраструктуры (малый отправитель): ~400 писем/день ≈ $150-200/мес (домены $13-15/год, ящики $4.5-6/мес, инструмент $37-94/мес) — [Prospeo](https://prospeo.io/s/cold-email-for-digital-marketing).

### Inferences
- Любой кейс "10M pipeline" брать как маркетинг; для SMB web/automation услуг реалистична модель: 2 000-3 000 писем/мес → 10-30 ответов (0.5-1%) → 2-6 встреч → 0-2 сделки.

### Gaps
- Не найдены проверяемые кейсы соло-основателей, продавших веб/автоматизацию сервисы с полными цифрами (Reddit r/coldemail не удалось получить через поиск).

## 6. Стоимость встречи и клиента (чек $2k-20k)

### Takeaway
Рыночные цены на встречу $200-500 (SMB) / $400-1 000 (enterprise); собственный DIY — десятки долларов за встречу в инфраструктуре, но основная стоимость — время основателя.

### Cited Findings
- Средняя стоимость квалифицированной B2B-встречи 2025: $550-1 700; для SMB $200-500, enterprise $400-1 000; pay-per-appointment $50-500; ретейнер $1 500-6 000/мес (чаще $2.5-4.5k); гибрид $2-4k + $150-400/встреча; другой диапазон: $21-164 за лид и $53-392 за встречу — [Salesar](https://salesar.io/blog/b2b-appointment-setting-costs-in-2025-pricing-models-explained); [Buzzlead](https://buzzlead.io/blogs/cold-email-agency-pricing-what-youll-actually-pay-in-2025); [Outbound System](https://outboundsystem.com/blog/how-much-does-a-cold-email-agency-cost). Всё агентские прайсы (bias).
- DIY инфраструктурная стоимость: 100K писем/мес $575-657 (инфраструктура $399, секвенсор $97-179, данные ~$79); на 30K $128-236; расчётная стоимость показавшейся встречи $2.6-18 — идеализированная модель с допущениями — [MailDeck](https://maildeck.co/blog/cold-email-cost-per-lead/).
- Для агентств: targeted cold email CPL $100-250, close rate 5-10% (GigRadar, источники: Focus Digital, Belkins, First Page Sage) — [GigRadar](https://gigradar.io/blog/digital-marketing-agency-lead-generation). CAC = CPL / close rate → $1 000-5 000 на клиента.
- AI SDR: $20-200 на встречу в лучших случаях; человек $250-900 — [SushiData](https://sushidata.com/blog/2026/03/24/the-state-of-the-ai-sdr-in-2026/).

### Inferences
- При чеке $2-20k и close rate встреча→сделка 10-25% CAC $1 000-5 000 (рыночная ставка) вполне окупается, но DIY-цифра зависит от оценки стоимости времени.

### Gaps
- Нет независимых данных о close rate "встреча→сделка" для веб/автоматизации услуг SMB.

## 7. Альтернативы cold email для продажи кастомного ПО SMB

### Takeaway
Рефералы и Upwork/маркетплейсы и SEO дают лучшие close rate; LinkedIn сопоставим по цене лида с email, но насыщается.

### Cited Findings
- Ранжирование каналов для агентств (GigRadar, агрегированные данные, небольшие агентства $5-50K/мес): Upwork 12-20% close, CPL $30-100; рефералы 30-50% close, CPL $40-150 (+$375-750 скрытых трудозатрат на сделку); SEO 10-25% close, CPL $50-200, 6-12 мес до эффекта; cold email 5-10%, CPL $100-250; LinkedIn 10-15%, CPL $120-387; платная реклама 8-20%, $247-800+; холодные звонки 2-5% — [GigRadar](https://gigradar.io/blog/digital-marketing-agency-lead-generation). Вендор Upwork-инструмента (bias за Upwork).
- LinkedIn (Belkins/Expandi, 15.1M касаний 2025 + 14 077 записей Belkins): средний reply 7.2% (4.2-10.5% по индустриям), принятие заявок 26%, с заметкой 25.3% (reply 8.2%) против без заметки 27.6% (reply 5.3%), 1.3% подключённых забронировали встречу; США — 6.0% (самое низкое среди крупных) — [Belkins](https://belkins.io/blog/linkedin-outreach-study). Другие источники: reply по агентствам снизился с 15-20% (2022) до 5-10% (2025) — [GigRadar](https://gigradar.io/blog/digital-marketing-agency-lead-generation).
- Для сравнения: Belkins email 0.45% reply vs LinkedIn 7.2% reply (разные определения; LinkedIn считается от подключённых).

### Inferences
- Для кастомного ПО/автоматизации SMB наиболее перспективны гибриды: LinkedIn + email на узкий список, партнёрства (рефералы), локальный SEO/маркетплейсы — но данных именно по продаже кастомного ПО SMB нет.

### Gaps
- Не найдены данные по партнёрствам и локальному SEO для SMB-разработки; региональные особенности (RU/EU/СНГ) кроме Belkins по странам (PL 1.43%) не найдены.
