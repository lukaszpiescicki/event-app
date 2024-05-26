Functionalities
## ADDITIONALS:
1) add help_texts to models
## USERS
1) Login / Rejestracja - DONE
2) Rozbudowa bazowego Usera - DONE
3) Edycja usera - DONE

# TODO:
1) Testy Jednstkowe #1

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
1) Testy Jednostkowe - DONE

# TODO*
1) Komentarze do artykułów  - DONE
2) Oceny Artykułu skale 1-5 lub łapka w górę w dół. - DONE
3) Tagi artykułów - DONE
4) Pobranie artykułu w formie PDF. - DONE


## BLOG API
1) Pobranie artykułu - DONE
2) Pobranie listy artykułów - DONE

# TODO
1) Testy Jednostkowe

# Tworzenie artykułowa
# Usuwanie arytkułow
# Edycje artykułów

### EVENTS

# TODO
1) Tworzenie wydarzenia (miejsce, tytuł, godzina, data itd.) - DONE
2) Stworzenie modelu wydarzania (Many to Many with User) - DONE
2) Możliwosć zapisania się na wydarzenie - DONE
3) Lista Wydarzeń - DONE
4) Edycja Wydarzenia - DONE
5) Generowanie linku do stworzenia szybkiego wydarzenia w Google Calendar - DONE
6) Powiadomienie e-mail przed wydarzeniem np. 3 dni 1 dzień itd. ( Selery )
7) Testy Jednostkowe - DONE

### MUSIC_NOTES

# TODO
1. Stworzenie modelu MusicNotes z odpowiednimi relacjami. PDF  - DONE
2. Wyświetlanie MusciNotes - DONE
3. Możliwość stworzneie przez osobe z odpowiednimi uprawnieniami nowego obiektu. Django Permissions - DONE
4. Edycja Music Notes - DONE
5. Usuwanie Music Notes - DONE
6*. Ocena przez wszystkich użytkowników, *oprócz owner'a
7. Wyświetlanei PDF. - DONE

### Organizations

# TODO

# NOTES
1. Każdy user bedzie musiał należeć do jakiejś organizacji. BLOCKED
2. Jak user ma być zapraszany do organizacji?
3. Tworzenie organizacji - DONE
4. User może należeć do kilku organizacji na raz. - DONE
5. User może posiadać kilka orgnaizacji (być właścicielm) - DONE


### OTHERS
# TODO
1. Wyświetlanie PDF - DONE

# Questions
1. Blog ogólny, czy per organizcjca czy organizacja i ogólny...  - per organizacja i ogólny

EXAMPLE

Music Notes - PDF... instrument, voice etc.
user instrument voice etc.
filter -> MusicNotes.objects.filter(Q(instrument__in=user.instruments) | Q(voice__in=user.voices))


Rekomendowana lista priorytetów

1 - Music Notes -> DONE
2 - Pierdoły typu komentarze itd. API dla blogu dokończyć itd. - DONE



TESTY Jednostkowe:
1. LoginRequiredMixin - Czy user jest zalogowany, czy nie czy endpoint jest chroniony.
2. UserPermissions - Czy user ma odpowiednie uprawnienia do edycji, usuwania, tworzenia obiektów.
3. UserPassesTestMixin - Jeżeli jest to testujesz zachowanie.

WIDOKI:
1. Create:
    - Tworzenie obiektu
    - Tworzenie obiektu z błędnymi danymi
    - Pobranie strony z formularzem
    - Sprawdzenie użytego templatu

2. Update:
    - Edycja obiektu
    - Edycja obiektu który nie istnieje
    - Edycja obiektu z błędnymi danymi
    - Pobranie stronu z formularzem
    - Sprawdzenie użytego templatu
3. Delete:
    - Usuwanie obiektu
    - Usuwanie obiektu który nie istnieje
    - Usuwanie obiektu który nie jest ownerem
   -  Usuwanie obiektu jak user jest nie zalogowany
4. List:
    - Wyświetlanie listy obiektów
    - Wyświetlanie listy obiektów z paginacją
    - Wyświetlanie listy obiektów z filtrowaniem
    - Wyświetlanie listy obiektów z sortowaniem
    - Sprawdzenie użytego templatu.
5. Detail:
    - Wyświetlanie obiektu
    - Wyświetlanie obiektu który nie istnieje
    - Wyświetlanie obiektu który nie jest ownerem
    - Sprawdzenie użytego templatu

Formularze:
1. Tworzenie obiektu z poprawnymi danymi form.is_valid()
2. Tworzenie obiektu z błędnymi danymi form.is_valid()


Modele:
- Testujesz tylko swoje własne dopisane funkcje
