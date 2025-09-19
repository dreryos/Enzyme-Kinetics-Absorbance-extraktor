# Enzyme Kinetics Extractor

🧬 Univerzální nástroj pro extrakci a analýzu dat enzymové kinetiky z IWBK souborů (Thermo Scientific) s **automatickou detekcí struktury**.

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Unlicense-brightgreen.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()

## 📋 Přehled

Tento nástroj automaticky převádí IWBK soubory na analyzovatelný formát a extrahuje spektrofotometrická data absorbance pro analýzu enzymové kinetiky. **Automaticky detekuje strukturu dat** (počet vzorků, časových bodů) ze souboru bez nutnosti zadávat pevné parametry.

### 🎯 Účel
- Automatická extrakce dat z proprietárního IWBK formátu (Thermo Scientific)
- Převod na standardní CSV formát pro další analýzu
- Podpora různých typů enzymů a experimentálních protokolů
- Inteligentní detekce experimentální struktury

## 🚀 Rychlý start

### Požadavky
- Python 3.7 nebo novější
- Základní Python knihovny (standardní součást instalace)

### Instalace

1. **Klonování repositáře:**
   ```bash
   git clone https://github.com/your-username/enzyme-kinetics-extractor.git
   cd enzyme-kinetics-extractor
   ```

2. **Instalace závislostí:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Spuštění:**
   ```bash
   python enzyme_kinetics_extractor.py "your_data.iwbk"
   ```

## ✨ Klíčové vlastnosti

- 🔍 **Automatická detekce struktury** - nástroj sám odhalí počet vzorků a časových bodů
- 🎯 **Adaptivní clustering** - inteligentně rozdělí data do logických skupin
- 📊 **Vysoké rozlišení** - zachová všechny datové body pro detailní analýzu
- 🧬 **Univerzální** - funguje s různými typy enzymů a experimentů
- 🚀 **Jednoduché použití** - stačí zadat IWBK soubor

## 🚀 Základní použití

```bash
# Základní extrakce s výchozími hodnotami (0.6-1.9 AU)
python enzyme_kinetics_extractor.py "data.iwbk"

# Vlastní rozsah absorbance
python enzyme_kinetics_extractor.py "data.iwbk" --target-min 0.3 --target-max 2.5

# Vlastní název výstupního souboru
python enzyme_kinetics_extractor.py "data.iwbk" --output "results.csv"
```

## 📊 Výstupní formát

Výstupní CSV soubor obsahuje:

| Sloupec | Popis |
|---------|-------|
| `Sample_ID` | Identifikátor vzorku (1-36) |
| `Sample_Name` | Název vzorku (např. "290nm, Sample1") |
| `Wavelength_nm` | Vlnová délka měření (nm) |
| `Time_Point` | Pořadové číslo časového bodu |
| `Time_sec` | Čas měření (sekundy) |
| `Absorbance` | Hodnota absorbance (AU) |
| `Raw_Value` | Surová hodnota z dekódování |
| `Scale_Factor` | Škálovací faktor |
| `Format_Used` | Použitý dekódovací formát |
| `File_Offset` | Pozice v souboru |
| `Source_File` | Zdrojový IWBK soubor |

## 🧬 Konfigurace pro různé enzymy

### APX (Ascorbate Peroxidase)
```bash
python enzyme_kinetics_extractor.py "data.iwbk" --target-min 0.6 --target-max 1.9
```
- **Rozsah:** 0.6-1.9 AU
- **Použití:** Antioxidační aktivita, stresové podmínky rostlin

### Peroxidase (obecná)
```bash
python enzyme_kinetics_extractor.py "data.iwbk" --target-min 0.3 --target-max 2.5
```
- **Rozsah:** 0.3-2.5 AU
- **Použití:** Široký spektrum peroxidasových reakcí

### Catalase
```bash
python enzyme_kinetics_extractor.py "data.iwbk" --target-min 0.1 --target-max 1.5
```
- **Rozsah:** 0.1-1.5 AU
- **Použití:** Rozklad peroxidu vodíku

### Polyphenol Oxidase
```bash
python enzyme_kinetics_extractor.py "data.iwbk" --target-min 0.2 --target-max 2.0
```
- **Rozsah:** 0.2-2.0 AU
- **Použití:** Oxidace fenolických sloučenin

## ⚙️ Parametry

| Parametr | Výchozí | Popis |
|----------|---------|-------|
| `--target-min` | 0.6 | Minimální hodnota absorbance (AU) |
| `--target-max` | 1.9 | Maximální hodnota absorbance (AU) |
| `--output`, `-o` | `{název_souboru}.csv` | Název výstupního CSV souboru |
| `--keep-temp` | False | Ponechat dočasné ASCII/HEX soubory |
| `--help`, `-h` | - | Zobrazit nápovědu |

## 🔧 Jak to funguje

1. **Konverze formátu:** IWBK → ASCII + HEX
2. **Analýza dekódování:** Testuje různé formáty (double, float, int, short) s různým endianness
3. **🆕 Automatická detekce struktury:** Analyzuje data a automaticky detekuje počet vzorků a časových bodů
4. **Adaptivní clustering:** Inteligentně rozděluje data do logických skupin na základě pozice v souboru
5. **Export CSV:** Vytvoří strukturovaný výstup zachovávající původní rozlišení dat

## 📈 Typické výsledky

- **Automaticky detekovaný počet vzorků** (např. 36, 50, 120...)
- **Vysoké rozlišení dat** (tisíce bodů per vzorek pro detailní kinetiku)
- **Adaptivní časové body** (podle skutečného měření)
- **Vlnová délka:** 290nm (typicky)
- **Rozsah:** Podle typu enzymu a nastaveného filtru

## 🔍 Řešení problémů

### Žádné hodnoty v rozsahu
- Zkuste rozšířit rozsah pomocí `--target-min` a `--target-max`
- Ověřte, že IWBK soubor obsahuje spektrofotometrická data

### Neočekávané hodnoty
- Zkontrolujte typ enzymu a použijte odpovídající rozsah
- Pro debugging použijte `--keep-temp` a prohlédněte si ASCII soubor

### Chyby při zpracování
- Ověřte, že soubor má příponu `.iwbk`
- Zkontrolujte, že soubor není poškozený

## 📁 Struktura souborů

```
projekt/
├── enzyme_kinetics_extractor.py    # Hlavní extraktor
├── README.md                       # Tento soubor
├── data.iwbk                      # Vstupní IWBK soubor
└── data.csv                       # Výstupní CSV (auto-generovaný)
```

## 🧪 Příklad výstupu

```csv
Sample_ID,Sample_Name,Wavelength_nm,Time_Point,Time_sec,Absorbance,Raw_Value,Scale_Factor,Format_Used,File_Offset,Source_File
1,"290nm, Sample1",290,1,0,0.827000,8270,0.000100,>H,12345,data.iwbk
1,"290nm, Sample1",290,2,10,1.245000,12450,0.000100,>H,12350,data.iwbk
1,"290nm, Sample1",290,3,20,1.654000,16540,0.000100,>H,12355,data.iwbk
1,"290nm, Sample1",290,4,30,1.432000,14320,0.000100,>H,12360,data.iwbk
...
```

**Poznámka:** Skutečný výstup obsahuje automaticky detekovaný počet vzorků a časových bodů podle struktury vašich dat.

## 🤝 Přispívání

Vítáme příspěvky! Prosím:

1. Forkněte repositář
2. Vytvořte feature branch (`git checkout -b feature/AmazingFeature`)
3. Commitněte změny (`git commit -m 'Add some AmazingFeature'`)
4. Pushněte do branch (`git push origin feature/AmazingFeature`)
5. Otevřete Pull Request

## 📜 Technické detaily

### Formát IWBK
- Proprietární binární formát Thermo Scientific
- Obsahuje spektrofotometrická data UV-VIS
- Automatická detekce enkódování (little/big endian)
- Podporované formáty: 16-bit unsigned short (>H, <H)

### Algoritmus detekce
1. **Dekódování**: Testování různých binárních formátů
2. **Filtrování**: Výběr hodnot v cílovém rozsahu absorbance
3. **Clustering**: Inteligentní seskupování do vzorků
4. **Validace**: Ověření struktury proti očekávaným parametrům

## 📄 Licence

Tento projekt je uvolněn do veřejné domény pod Unlicense - viz [LICENSE](LICENSE) soubor pro detaily.

Můžete jej volně kopírovat, upravovat, publikovat, používat, kompilovat, prodávat nebo distribuovat jakýmkoliv způsobem.

## 👨‍💻 Autor

Vytvořeno pro analýzu enzymové kinetiky v laboratorním výzkumu.

## 🙏 Poděkování

- Thermo Scientific za IWBK formát
- Python komunitě za výborné nástroje
- Všem, kteří přispěli k testování a vývoji
