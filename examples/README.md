# Examples

Tato složka obsahuje příklady použití Enzyme Kinetics Extractor nástroje.

## Dostupné příklady

### Základní použití
```bash
# Jednoduché spuštění s výchozími hodnotami
python ../enzyme_kinetics_extractor.py "sample_data.iwbk"
```

### Pokročilé použití
```bash
# Vlastní rozsah absorbance pro specifický enzym
python ../enzyme_kinetics_extractor.py "sample_data.iwbk" --target-min 0.3 --target-max 2.5 --output "custom_results.csv"
```

## Vzorová data

Pro testování můžete použít vlastní IWBK soubory z vašeho spektrofotometru.

**Poznámka:** Vzorové IWBK soubory nejsou zahrnuty v repositáři kvůli velikosti a licenčním omezením.