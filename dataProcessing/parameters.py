import prefix as prefixPckg



class Parameter:
    def __init__(self, champ, prefix="dbo", prefix_url=None, filtre_langues=True, langues=["EN", "FR", "DE"]):
        self.prefixGestionary = prefixPckg.PrefixGestionary()
        self.champ = champ
        self.prefix = prefix
        self.prefix_url = prefix_url or self.get_prefix_url_from_file()
        self.filtre_langues = filtre_langues
        self.langues = langues
        # Si le prefix_url n'est pas dans le fichier, on l'ajoute
        if self.prefix not in self.get_all_prefixes():
            self.save_prefix_to_file()

    def get_filtre_langue_query(self):
        if self.filtre_langues:
            langues_condition = " || ".join([f'langMatches(lang(?{self.champ}), "{lang}")' for lang in self.langues])
            return True, f"BIND(lang(?{self.champ}) AS ?lang) .",  f"FILTER({langues_condition})", "?lang"
        return False, "", "", ""

    def get_prefix(self):
        return self.prefix

    def get_prefix_url(self):
        return self.prefix_url

    def get_champ(self):
        return self.champ

    def get_prefix_url_from_file(self):
        """Recherche du prefix_url dans le fichier de stockage des préfixes"""
        prefixes = self.get_all_prefixes()
        return prefixes.get(self.prefix)

    def get_all_prefixes(self):
        """Retourne tous les préfixes et leurs URL depuis le fichier"""
        return self.prefixGestionary.loadPrefix()

    def save_prefix_to_file(self):
        """Ajoute ou met à jour le préfixe dans le fichier JSON"""
        prefixes = self.get_all_prefixes()
        prefixes[self.prefix] = self.prefix_url
        self.prefixGestionary.savePrefix(prefixes)