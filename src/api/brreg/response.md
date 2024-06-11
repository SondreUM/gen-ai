# BRREG API V2 response parameters

ref: <https://data.brreg.no/enhetsregisteret/api/docs/index.html#enheter-sok>

| Path                               | Type    | Description                                                                        |
|------------------------------------|---------|------------------------------------------------------------------------------------|
| _embedded.enheter[].organisasjonsnummer | String  | Enhetens organisasjonsnummer                                                       |
| _embedded.enheter[].navn           | String  | Enhetens navn                                                                      |
| _embedded.enheter[].organisasjonsform   | Object  | Enhetens organisasjonsform                                                         |
| _embedded.enheter[].organisasjonsform.kode  | String  | Organisasjonsformen                                                                |
| _embedded.enheter[].organisasjonsform.beskrivelse | String  | Tekstlig beskrivelse av organisasjonsformen                                        |
| _embedded.enheter[].organisasjonsform.utgaatt   | String  | Dato når organisasjonsformen evt. ble ugyldig                                      |
| _embedded.enheter[].organisasjonsform._links.self.href | String  | Lenke til egen ressurs                                                             |
| _embedded.enheter[].hjemmeside     | String  | Enhetens hjemmeside                                                                |
| _embedded.enheter[].postadresse    | Object  | Enhetens postadresse                                                               |
| _embedded.enheter[].postadresse.adresse | Array   | Adresse (postadresse)                                                              |
| _embedded.enheter[].postadresse.postnummer | String  | Postnummer (postadresse)                                                           |
| _embedded.enheter[].postadresse.poststed | String  | Poststed (postadresse)                                                             |
| _embedded.enheter[].postadresse.kommunenummer | String  | Kommunenummer (postadresse)                                                        |
| _embedded.enheter[].postadresse.kommune | String  | Kommune (postadresse)                                                              |
| _embedded.enheter[].postadresse.landkode | String  | Landkode (postadresse)                                                             |
| _embedded.enheter[].postadresse.land | String  | Land (postadresse)                                                                 |
| _embedded.enheter[].registreringsdatoEnhetsregisteret | String  | Enhetens registreringsdato i Enhetsregisteret                                       |
| _embedded.enheter[].registrertIMvaregisteret | Boolean | Hvorvidt enheten er registrert i MVA-registeret                                     |
| _embedded.enheter[].frivilligMvaRegistrertBeskrivelser | Array   | Enheter som i utgangspunktet ikke er mva-pliktig, kan søke om frivillig registrering i Merverdiavgiftsregisteret. |
| _embedded.enheter[].naeringskode1  | Object  | Næringskode 1                                                                      |
| _embedded.enheter[].naeringskode1.kode | String  | Næringskoden                                                                       |
| _embedded.enheter[].naeringskode1.beskrivelse | String  | Tekstlig beskrivelse av næringskoden                                                |
| _embedded.enheter[].naeringskode2  | Object  | Næringskode 2                                                                      |
| _embedded.enheter[].naeringskode2.kode | String  | Næringskoden                                                                       |
| _embedded.enheter[].naeringskode2.beskrivelse | String  | Tekstlig beskrivelse av næringskoden                                                |
| _embedded.enheter[].naeringskode3  | Object  | Næringskode 3                                                                      |
| _embedded.enheter[].naeringskode3.kode | String  | Næringskoden                                                                       |
| _embedded.enheter[].naeringskode3.beskrivelse | String  | Tekstlig beskrivelse av næringskoden                                                |
| _embedded.enheter[].hjelpeenhetskode | Object  | Hjelpeenhetskode                                                                   |
| _embedded.enheter[].hjelpeenhetskode.kode | String  | Hjelpeenhetskode                                                                   |
| _embedded.enheter[].hjelpeenhetskode.beskrivelse | String  | Tekstlig beskrivelse av hjelpeenhetskode                                            |
| _embedded.enheter[].antallAnsatte  | Number  | Antall ansatte                                                                     |
| _embedded.enheter[].harRegistrertAntallAnsatte | Boolean | Angir om enheten har registrert ansatte                                            |
| _embedded.enheter[].overordnetEnhet | String  | Organisasjonsnummeret til overordnet enhet i offentlig sektor                       |
| _embedded.enheter[].forretningsadresse | Object  | Enhetens forretningsadresse                                                        |
| _embedded.enheter[].forretningsadresse.adresse | Array   | Adresse (forretningsadresse)                                                       |
| _embedded.enheter[].forretningsadresse.postnummer | String  | Postnummer (forretningsadresse)                                                    |
| _embedded.enheter[].forretningsadresse.poststed | String  | Poststed (forretningsadresse)                                                      |
| _embedded.enheter[].forretningsadresse.kommunenummer | String  | Kommunenummer (forretningsadresse)                                                 |
| _embedded.enheter[].forretningsadresse.kommune | String  | Kommune (forretningsadresse)                                                       |
| _embedded.enheter[].forretningsadresse.landkode | String  | Landkode (forretningsadresse)                                                      |
| _embedded.enheter[].forretningsadresse.land | String  | Land (forretningsadresse)                                                          |
| _embedded.enheter[].stiftelsesdato | String  | Enhetens stiftelsesdato                                                            |
| _embedded.enheter[].institusjonellSektorkode | Object  | Enhetens sektorkode                                                                |
| _embedded.enheter[].institusjonellSektorkode.kode | String  | Sektorkoden                                                                        |
| _embedded.enheter[].institusjonellSektorkode.beskrivelse | String  | Tekstlig beskrivelse av sektorkoden                                                 |
| _embedded.enheter[].registrertIForetaksregisteret | Boolean | Hvorvidt enheten er registrert i Foretaksregisteret                                 |
| _embedded.enheter[].registrertIStiftelsesregisteret | Boolean | Hvorvidt enheten er registrert i Stiftelsesregisteret                               |
| _embedded.enheter[].registrertIFrivillighetsregisteret | Boolean | Hvorvidt enheten er registrert i Frivillighetsregisteret                           |
| _embedded.enheter[].sisteInnsendteAarsregnskap | String  | Dato for siste innsendte årsregnskap                                               |
| _embedded.enheter[].konkurs         | Boolean | Hvorvidt enheten er konkurs                                                        |
| _embedded.enh

eter[].konkursdato     | String  | Kjennelsesdato for konkursen. Format: yyyy-MM-dd                                   |
| _embedded.enheter[].underAvvikling  | Boolean | Hvorvidt enheten er under avvikling                                                 |
|_embedded.enheter[].underAvviklingDato | String  | Dato virksomheten er meldt oppløst. Format: yyyy-MM-dd                             |
| _embedded.enheter[].underTvangsavviklingEllerTvangsopplosning | Boolean | Hvorvidt enheten er under tvangsavvikling eller tvangsoppløsning                  |
|_embedded.enheter[].tvangsavvikletPgaManglendeSlettingDato | String  | Dato virksomheten ble tvangsavviklet pga manglende sletting. Format: yyyy-mm-dd    |
| _embedded.enheter[].tvangsopplostPgaManglendeDagligLederDato | String  | Dato virksomheten ble tvangsoppløst pga manglende daglig leder. Format: yyyy-mm-dd |
|_embedded.enheter[].tvangsopplostPgaManglendeRevisorDato | String  | Dato virksomheten ble tvangsoppløst pga manglende revisor. Format: yyyy-mm-dd       |
| _embedded.enheter[].tvangsopplostPgaManglendeRegnskapDato | String  | Dato virksomheten ble tvangsoppløst pga manglende regnskap. Format: yyyy-mm-dd       |
|_embedded.enheter[].tvangsopplostPgaMangelfulltStyreDato | String  | Dato virksomheten ble tvangsoppløst pga manglende styre. Format: yyyy-mm-dd          |
| _embedded.enheter[].maalform        | String  | Målform                                                                            |
|_embedded.enheter[].vedtektsdato   | String  | Enhetens vedtektsdato. Format: yyyy-MM-dd                                           |
| _embedded.enheter[].vedtektsfestetFormaal | Array   | Enhetens formål                                                                    |
|_embedded.enheter[].aktivitet      | Array   | Enhetens aktivitet                                                                 |
| _embedded.enheter[]._links.self.href | String  | Lenke til egen ressurs                                                             |
| _embedded.enheter[]._links.overordnetEnhet.href | String  | Lenke til enhetens overordnede enhet i offentlig sektor                             |
| page.size                          | Number  | Sidestørrelse på resultatet                                                        |
| page.totalElements                | Number  | Totalt antall elementer i resultatet                                                |
| page.totalPages                   | Number  | Totalt antall sider i resultatet                                                    |
| page.number                       | Number  | Nummer på gjeldende side                                                            |
| _links.first.href                 | String  | Lenke til første side med resultater                                                |
|_links.prev.href                  | String  | Lenke til forrige side med resultater                                               |
| _links.self.href                  | String  | Lenke til egen ressurs                                                              |
|_links.next.href                  | String  | Lenke til neste side med resultater                                                 |
| _links.last.href                  | String  | Lenke til siste side med resultater                                                 |
