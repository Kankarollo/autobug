# Autobug


## Notes:
1. Wyszukiwanie leaków na githubie 
2. Sprawdzanie zmian w aplikacjach
	1. Zrobić hashe z odpowiedzi z aplikacji i porownac je z nowymi odpowiedziami - tutaj not sure, ale chyba odpowiedź zwrotna jest za bardzo losowa eg. headery mogą być w różnej kolejności więc może nie wyjść
	2. Najpierw używać HEAD requestów
3. Słownikowe sprawdzanie leaków danych - .git, /actuator itp. 
	1. Najlepiej puszczać jedno słowo na wszystkie domeny niż cały słownik na pojedyncza domene
	2. Jakiś mały, wyselekcjonowany słownik
4. Wyszukwanie nowych subdomen
5. Wyszukiwanie subdomain takeoverów
6. Otwarte porty - szukanie zmian
7. DNS zone transfer  
8. HTTP Request smuggling


--------------------
## Tools

### Recon of scope
- amass
- httpx
- masscan
- github-subdomains.py
- shuffledns
### Postrecon
- nmap
- brutespray - service scanning