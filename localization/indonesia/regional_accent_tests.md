# Regional accent test record

Target: Javanese-influenced Indonesian speech (Central Java), a prototype target outside standard Jakarta speech. Source: synthetic/manual prototype utterances; native-speaker validation is unavailable.

| phrase | expected | actual | impact | mitigation |
|---|---|---|---|---|
| Saya mau cek cicilan saya | same | same | none | retain |
| Nggak usah panjang-panjang, kapan jatuh temponya? | same | Tidak usah panjang-panjang, kapan jatuh temponya? | usable normalization | colloquial lexicon |
| Angsuran bulan ini kena denda? | same | Angsuran bulan ini kena data? | finance intent risk | confirm key term |
| Bisa follow-up soal tenor dan installment? | same | Bisa follow up soal tenor dan instalmen? | usable spelling variant | accept variants |
| Monggo dibantu cek cicilane | same | same | regional form may be OOV | ask standard restatement |

Qualitative observations only; no WER or percentage is claimed. Regional-accent behavior was tested using available prototype speech material; native-speaker validation remains a limitation.
