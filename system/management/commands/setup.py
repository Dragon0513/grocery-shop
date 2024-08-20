from django.core.management.base import BaseCommand

from personal.models import Category, Food, Section


class Command(BaseCommand):
    help = "Setup default categories, sections, and foods"

    def handle(self, *args, **kwargs):
        # Kategorien erstellen
        categories = [
            {"name": "Gemüse", "icon": "carrot"},
            {"name": "Früchte", "icon": "food-apple"},
            {"name": "Fisch", "icon": "fish"},
            {"name": "Fleisch", "icon": "food-drumstick"},
            {"name": "Milch / Eier", "icon": "egg"},
            {"name": "Öle", "icon": "seed"},
        ]

        for category_data in categories:
            category, created = Category.objects.get_or_create(
                name=category_data["name"],
                defaults={"icon": category_data["icon"]},
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Category '{category.name}' created.")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Category '{category.name}' already exists.")
                )

        # Sektionen erstellen
        sections = [
            {"category": "Fleisch", "name": "Wurstwaren"},
            {"category": "Fleisch", "name": "Wildfleisch"},
            {"category": "Fleisch", "name": "Lammfleisch"},
            {"category": "Fleisch", "name": "Geflügel"},
            {"category": "Fleisch", "name": "Schweinefleisch"},
            {"category": "Fleisch", "name": "Rindfleisch"},
            {"category": "Fisch", "name": "Meeresfrüchte"},
            {"category": "Fisch", "name": "Süsswasserfisch"},
            {"category": "Fisch", "name": "Seefisch"},
            {"category": "Öle", "name": "Blüten- und Distelöle"},
            {"category": "Öle", "name": "Fruchtöle"},
            {"category": "Öle", "name": "Kern- und Keimöle"},
            {"category": "Öle", "name": "Samenöle"},
            {"category": "Öle", "name": "Nussöle"},
            {"category": "Milch / Eier", "name": "Eier"},
            {"category": "Milch / Eier", "name": "Käsesorten"},
            {"category": "Milch / Eier", "name": "Buttersorten"},
            {"category": "Milch / Eier", "name": "Milchsorten"},
            {"category": "Früchte", "name": "Zitrusfrüchte"},
            {"category": "Früchte", "name": "Steinobst"},
            {"category": "Früchte", "name": "Kernobst"},
            {"category": "Früchte", "name": "Hartschalenobst"},
            {"category": "Früchte", "name": "Exotische Früchte"},
            {"category": "Früchte", "name": "Beerenobst"},
            {"category": "Gemüse", "name": "Zwiebelgemüse"},
            {"category": "Gemüse", "name": "Fruchtgemüse"},
            {"category": "Gemüse", "name": "Hülsen- und Samengemüse"},
            {"category": "Gemüse", "name": "Stängel- und Sprossengemüse"},
            {"category": "Gemüse", "name": "Spinatartige Blattgemüse"},
            {"category": "Gemüse", "name": "Blattstielgemüse"},
            {"category": "Gemüse", "name": "Kohlgemüse"},
            {"category": "Gemüse", "name": "Salatartige Blattgemüse"},
            {"category": "Gemüse", "name": "Blütengemüse und Blütenstände"},
            {"category": "Gemüse", "name": "Knollen – und Wurzelgemüse"},
        ]

        section_objects = {}
        for section_data in sections:
            category = Category.objects.get(name=section_data["category"])
            section, created = Section.objects.get_or_create(
                name=section_data["name"],
                category=category,
            )
            section_objects[f"{category.name} - {section.name}"] = section
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Section '{section.name}' under '{category.name}' created."
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Section '{section.name}' under '{category.name}' already exists."
                    )
                )

        # Definieren Sie die Zuordnung von Lebensmitteln zu Sektionen
        foods_by_section = {
            "Fleisch - Rindfleisch": [
                "Steak",
                "Hackfleisch",
                "Braten",
                "Gulasch",
                "Filet",
            ],
            "Fleisch - Schweinefleisch": [
                "Kotelett",
                "Schnitzel",
                "Speck",
                "Schinken",
                "Hackfleisch",
            ],
            "Fleisch - Geflügel": ["Hähnchen", "Pute", "Ente", "Gans"],
            "Fleisch - Lammfleisch": ["Kotelett", "Keule", "Filet"],
            "Fleisch - Wildfleisch": ["Hirsch", "Wildschwein", "Reh", "Kaninchen"],
            "Fleisch - Wurstwaren": [
                "Salami",
                "Schinkenwurst",
                "Bratwurst",
                "Blutwurst",
                "Leberwurst",
            ],
            "Fisch - Seefisch": ["Kabeljau", "Lachs", "Thunfisch", "Hering", "Makrele"],
            "Fisch - Süsswasserfisch": [
                "Forelle",
                "Zander",
                "Karpfen",
                "Wels",
                "Hecht",
            ],
            "Fisch - Meeresfrüchte": [
                "Garnelen",
                "Muscheln",
                "Tintenfisch",
                "Hummer",
                "Krabben",
            ],
            "Öle - Blüten- und Distelöle": ["Baumnussöl", "Distelöl"],
            "Öle - Fruchtöle": ["Olivenöl"],
            "Öle - Kern- und Keimöle": ["Maiskeimöl"],
            "Öle - Samenöle": ["Sesamöl", "Rapsöl"],
            "Öle - Nussöle": ["Erdnussöl", "Haselnussöl"],
            "Milch / Eier - Milchsorten": [
                "Vollmilch",
                "Rohmilch",
                "Entrahmte Milch",
                "Lactosefreie Milch",
                "Schafmilch",
                "Büffelmilch",
                "Ziegenmilch",
            ],
            "Milch / Eier - Buttersorten": [
                "Dreiviertelfettbutter",
                "Halbfettbutter",
                "Gesalzene Butter",
                "Entwässerte Butter",
            ],
            "Milch / Eier - Käsesorten": [
                "Saanenkäse",
                "Sbrinz",
                "Parmesan",
                "Hartkäse",
                "Emmentaler",
                "Appenzeller",
                "Bergkäse",
                "Freiburger Vacherin",
                "Raclettekäse",
                "Schabziger",
                "Tete de Moine",
                "Tilsiter",
                "Brie",
                "Camembert",
                "Tomme",
                "Gorgonzola",
                "Roquefort",
                "Stilton",
                "Reblochon",
                "Münster",
                "Taleggio",
                "Vacherin Mont-d Or",
                "Feta",
                "Hüttenkäse",
                "Mascarpone",
                "Mozzarella",
                "Quark",
                "Ricotta",
            ],
            "Milch / Eier - Eier": [
                "Strausseneier",
                "Gänseeier",
                "Enteneier",
                "Wachteleier",
                "Eier vom Haushuhn",
            ],
            "Früchte - Zitrusfrüchte": [
                "Bergamotten",
                "Grapefruits",
                "Kumquats",
                "Limetten",
                "Mandarinen",
                "Orange",
                "Zitronen",
            ],
            "Früchte - Steinobst": [
                "Aprikosen",
                "Kirschen",
                "Mirabellen",
                "Nektarinen",
                "Pfirsiche",
                "Pflaumen",
                "Zwetschgen",
            ],
            "Früchte - Kernobst": ["Apfel", "Birnen", "Quitten"],
            "Früchte - Hartschalenobst": [
                "Baumnüsse",
                "Cashewnüsse",
                "Erdnüsse",
                "Haselnüsse",
                "Kastanien",
                "Kokosnüsse",
                "Macadamianüsse",
                "Mandeln",
                "Paranüsse",
                "Pecannüsse",
                "Pinienkerne",
                "Pistazien",
            ],
            "Früchte - Exotische Früchte": [
                "Ananas",
                "Avocados",
                "Bananen",
                "Cherimoyas",
                "Datteln",
                "Feigen",
                "Granatäpfel",
                "Kapstachelbeeren",
                "Kiwis",
                "Litschis",
                "Mangos",
                "Mangostanen",
                "Oliven",
                "Papayas",
                "Passionsfrüchte",
                "Pitahayas",
                "Rambutans",
            ],
            "Früchte - Beerenobst": [
                "Brombeeren",
                "Erdbeeren",
                "Heidelbeeren",
                "Himbeeren",
                "Holunder",
                "Johannisbeeren",
                "Preiselbeeren",
                "Stachelbeeren",
                "Tafeltrauben",
            ],
            "Gemüse - Zwiebelgemüse": ["Knoblauch", "Lauch", "Schalotten", "Zwiebeln"],
            "Gemüse - Fruchtgemüse": [
                "Auberginen",
                "Gurken",
                "Kürbis",
                "Peperoni",
                "Tomaten",
                "Zucchetti",
                "Zuckermais",
            ],
            "Gemüse - Hülsen- und Samengemüse": ["Bohnen", "Erbsen", "Kefen"],
            "Gemüse - Stängel- und Sprossengemüse": ["Kohlrabi", "Spargeln"],
            "Gemüse - Spinatartige Blattgemüse": ["Blattspinat", "Schnittmangold"],
            "Gemüse - Blattstielgemüse": [
                "Fenchel",
                "Kardy",
                "Krautstiele",
                "Rhabarber",
                "Stangensellerie",
            ],
            "Gemüse - Kohlgemüse": [
                "Chinakohl",
                "Federkohl",
                "Rosenkohl",
                "Rotkohl",
                "Weisskohl",
                "Wirz/Wirsing",
            ],
            "Gemüse - Salatartige Blattgemüse": [
                "Batavia",
                "Brüsseler Endivie",
                "Catalonia",
                "Cicorino",
                "Eichblattsalat",
                "Eisberg",
                "Endivie",
                "Kopfsalat",
                "Kresse",
                "Lattich",
                "Lollo",
                "Löwenzahn",
                "Nüsslisalat",
                "Rucola",
                "Zuckerhut",
            ],
            "Gemüse - Blütengemüse und Blütenstände": [
                "Artischocken",
                "Blumenkohl",
                "Broccoli",
                "Romanesco",
            ],
            "Gemüse - Knollen – und Wurzelgemüse": [
                "Karotten",
                "Pastinaken",
                "Petersilienwurzeln",
                "Radieschen",
                "Randen",
                "rote Bete",
                "Rettiche",
                "Schwarzwurzeln",
                "Sellerie",
                "Stachys",
                "Topinamburen",
                "Weissrüben",
            ],
        }

        # Bereinigung der Datenbank: Löschen aller vorhandenen Lebensmittel
        Food.objects.all().delete()

        # Erstellen und eindeutiges Zuordnen der Lebensmittel zu den Sektionen
        for section_key, foods in foods_by_section.items():
            category_name, section_name = section_key.split(" - ")
            section = Section.objects.get(
                name=section_name, category__name=category_name
            )

            for food_name in foods:
                # Lebensmittel direkt der richtigen Sektion zuordnen
                food, created = Food.objects.get_or_create(
                    name=food_name, section=section
                )

                if created:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Food '{food.name}' in section '{section.name}' created."
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Food '{food.name}' in section '{section.name}' already exists."
                        )
                    )
