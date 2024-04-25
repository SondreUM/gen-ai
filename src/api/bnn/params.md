# BNN API request parameters

ref: <https://data.brreg.no/enhetsregisteret/api/docs/index.html#enheter-sok>

| Field Name                                 | Description                                           | Data Type                | Notes |
| ------------------------------------------ | ----------------------------------------------------- | ------------------------ | ----- |
| navn                                       | Enhetens navn                                         | String                   | Fritekst på 1 til 180 tegn |
| organisasjonsnummer                        | Organisasjonsnummeret til enheten                     | String                   | Kommaseparert liste med organisasjonsnummer |
| overordnetEnhet                            | Organisasjonsnummeret til enhetens overordnede enhet   | String                   | Streng med 9 siffer |
| fraAntallAnsatte                           | Minste antall ansatte hos enheten                     | Int                      | Tall må være 0, 1 eller større enn 4 |
| tilAntallAnsatte                           | Største antall ansatte hos enheten                    | Int                      | Tall må være 0, 4, eller over 4 |
| konkurs                                    | Hvorvidt enheten er registrert som konkurs            | Boolean                  | true/false |
| registrertIMvaregisteret                   | Hvorvidt enheten er registrert i Mva-registeret       | Boolean                  | true/false |
| registrertIForetaksregisteret              | Hvorvidt enheten er registrert i Foretaksregisteret   | Boolean                  | true/false |
| registrertIStiftelsesregisteret            | Hvorvidt enheten er registrert i Stiftelsesregisteret | Boolean                  | true/false |
| registrertIFrivillighetsregisteret         | Hvorvidt enheten er registrert i Frivillighetsregisteret | Boolean                | true/false |
| frivilligRegistrertIMvaregisteret          | Frivillig registrert i Merverdiavgiftsregisteret      | String                   | Kommaseparert liste med beskrivelser |
| underTvangsavviklingEllerTvangsopplosning  | Hvorvidt enheten er registrert som underTvangsavvikling eller tvangsopplosning | Boolean | true/false |
| underAvvikling                             | Hvorvidt enheten er registrert som underAvvikling      | Boolean                  | true/false |
| fraRegistreringsdatoEnhetsregisteret        | Tidligste registreringsdato i Enhetsregisteret         | String (yyyy-MM-dd)      | Dato (ISO-8601): yyyy-MM-dd |
| tilRegistreringsdatoEnhetsregisteret        | Seneste registreringsdato i Enhetsregisteret           | String (yyyy-MM-dd)      | Dato (ISO-8601): yyyy-MM-dd |
| fraStiftelsesdato                          | Tidligste stiftelsesdato for enheten                   | String (yyyy-MM-dd)      | Dato (ISO-8601): yyyy-MM-dd |
| tilStiftelsesdato                          | Seneste stiftelsesdato hos enheten                     | String (yyyy-MM-dd)      | Dato (ISO-8601): yyyy-MM-dd |
| organisasjonsform                          | Enhetens organisasjonsform                            | String                   | Kommaseparert liste med organisajonsformer |
| hjemmeside                                 | Enhetens hjemmeside                                   | String                   | Fritekst |
| institusjonellSektorkode                    | Enhetens institusjonelle sektorkode                    | String                   | Kommaseparert liste med sektorkoder på 4 siffer |
| postadresse.kommunenummer                   | Kommunenummer til enhetens postadresse                 | String                   | Kommaseparert liste med kommunenummer på 4 siffer |
| postadresse.postnummer                      | Postnummeret til enhetens postadresse                  | String                   | Kommaseparert liste med postnummer på 4 siffer |
| postadresse.poststed                        | Poststedet til enhetens postadresse                    | String                   | Fritekst |
| postadresse.landkode                        | Landkode til enhetens postadresse                      | String                   | Kommaseparert liste med landkoder |
| postadresse.adresse                         | Adresse til enhetens postadresse                       | String                   | Kommaseparert liste med adresser |
| kommunenummer                              | Kommunenummeret til enhetens forretningsadresse eller postadresse | String          | Kommaseparert liste med kommunenummer på 4 siffer |
| forretningsadresse.kommunenummer            | Kommunenummeret til enhetens forretningsadresse         | String                   | Kommaseparert liste med kommunenummer på 4 siffer |
| forretningsadresse.postnummer               | Postnummer til enhetens forretningsadresse              | String                   | Kommaseparert liste med postnummer på 4 siffer |
| forretningsadresse.poststed                 | Poststedet til enhetens forretningsadresse              | String                   | Fritekst |
| forretningsadresse.landkode                 | Landkode til enhetens forretningsadresse                | String                   | Kommaseparert liste med landkoder |
| forretningsadresse.adresse                  | Adresse til enhetens forretningsadresse                 | String                   | Kommaseparert liste med adresser |
| naeringskode                               | Enhetens næringskode                                   | Array                    | Kommaseparert liste med næringskoder |
| sisteInnsendteAarsregnskap                  | Årstall for siste innsendte årsregnskap for enheten     | String                   | Kommaseparert liste med årstall på 4 siffer |
| sort                                       | Sortering av resultatsett                              | String                   | Feltnavn i enheten. Se Eksempel 3 - Sortere søkeresultat |
| size                                       | Sidestørrelse                                          | Int                      | Tall større enn 0 |
| page                                       | Sidenummer                                             | Int                      | Tall større enn eller lik 0 |
