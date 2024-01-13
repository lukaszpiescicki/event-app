Functionalities 

## USERS 
1) Login / Rejestracja - DONE 
2) Rozbudowa bazowego Usera - DONE
3) Edycja usera - DONE 

# TODO
1) Testy Jednstkowe 

# TODO* 
1) System powiadomień 
2) System zawierania znajomości - 1/10

## BLOG 
1) Utworzenie Post Bloga - DONE
2) Usuwanie Post Bloga - DONE 
3) Edycja Post Bloga - DONE 
4) Uprawnienia dla ownera (Czyt. tylko owner artykulu moze go usunac ew. admin) - DONE
5) Wyświetlanie Artykułu - DONE 
6) Wyświetalne listy artykułów wraz z Paginacja - DONE

# TODO 
1) Testy Jednostkowe 

# TODO* 
1) Komentarze do artykułów  
2) Oceny Artykułu skale 1-5 lub łapka w górę w dół. 
3) Tagi artykułów 
4) Pobranie artykułu w formie PDF. 


## BLOG API 
1) Pobranie artykułu - DONE 
2) Pobranie listy artykułów - DONE

# TODO
1) Testy Jednostkowe 

# Tworzenie artykułow 
# Usuwanie arytkułow 
# Edycje artykułów 

### EVENTS

# TODO
1) Tworzenie wydarzenia (miejsce, tytuł, godzina, data itd.)
2) Stworzenie modelu wydarzania (Many to Many with User)
2) Możliwosć zapisania się na wydarzenie 
3) Lista Wydarzeń 
4) Edycja Wydarzenia 
5) Generowanie linku do stworzenia szybkiego wydarzenia w Google Calendar
6) Powiadomienie e-mail przed wydarzeniem np. 3 dni 1 dzień itd. 
7) Testy Jednostkowe

### MUSIC_NOTES 

# TODO
1. Stworzenie modelu MusicNotes z odpowiednimi relacjami. PDF  - DONE
2. Wyświetlanie MusciNotes
3. Możliwość stworzneie przez osobe z odpowiednimi uprawnieniami nowego obiektu. Django Permissions 
4. Edycja Music Notes - DONE
5. Usuwanie Music Notes - DONE
6*. Ocena przez wszystkich użytkowników, *oprócz owner'a
7. Wyświetlanei PDF. 

### Organizations

# TODO 

# NOTES 
1. Każdy user bedzie musiał należeć do jakiejś organizacji. 
2. Jak user ma być zapraszany do organizacji?
3. Tworzenie organizacji 
4. User może należeć do kilku organizacji na raz. 
5. User może posiadać kilka orgnaizacji (być właścicielm)


### OTHERS
# TODO
1. Wyświetlanie PDF 

# Questions
1. Blog ogólny, czy per organizcjca czy organizacja i ogólny...  - per organizacja i ogólny

EXAMPLE 

Music Notes - PDF... instrument, voice etc. 
user instrument voice etc. 
filter -> MusicNotes.objects.filter(Q(instrument__in=user.instruments) | Q(voice__in=user.voices))


Rekomendowana lista priorytetów

1 - Music Notes 
2 - Pierdoły typu komentarze itd. API dla blogu dokończyć itd. 
3 - Organizacje lub Eventy (Z prefrencja organizacji)