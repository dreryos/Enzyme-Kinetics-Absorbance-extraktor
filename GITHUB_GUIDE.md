# GitHub Publication Guide

Návod pro publikaci Enzyme Kinetics Extractor na GitHub.

## 🚀 Kroky pro publikaci

### 1. Příprava repositáře na GitHub
1. Přihlaste se na [GitHub.com](https://github.com)
2. Klikněte na "New repository"
3. Název: `enzyme-kinetics-extractor`
4. Popis: `Universal tool for extracting enzyme kinetics data from IWBK files with automatic structure detection`
5. Zvolte "Public" (pro open source)
6. **NEVYTVÁŘEJTE** README, .gitignore, nebo LICENSE (máme je již připravené)

### 2. Inicializace Git repositáře
```bash
# V této složce spusťte:
git init
git add .
git commit -m "Initial commit: Enzyme Kinetics Extractor v1.0.0"
```

### 3. Propojení s GitHub
```bash
# Nahraďte YOUR_USERNAME svým GitHub jménem
git remote add origin https://github.com/YOUR_USERNAME/enzyme-kinetics-extractor.git
git branch -M main
git push -u origin main
```

### 4. Aktualizace odkazů
Po publikaci aktualizujte odkazy v souborech:
- `README.md`: Nahraďte `your-username` skutečným jménem
- `setup.py`: Aktualizujte URL a email

### 5. Vytvoření release
1. Na GitHub jděte do sekce "Releases"
2. Klikněte "Create a new release"
3. Tag: `v1.0.0`
4. Název: `Enzyme Kinetics Extractor v1.0.0`
5. Popis: Zkopírujte z `CHANGELOG.md`

## 📝 Doporučení

### Topics (štítky) pro repositář
- `enzyme-kinetics`
- `spectrophotometry`
- `iwbk`
- `thermo-scientific`
- `data-extraction`
- `python`
- `biochemistry`
- `laboratory`

### README badges
Všechny potřebné badges jsou již v README.md

### Struktura repositáře
```
enzyme-kinetics-extractor/
├── 📄 README.md              # Hlavní dokumentace
├── 🐍 enzyme_kinetics_extractor.py  # Hlavní nástroj
├── 📋 requirements.txt       # Python závislosti
├── 📜 LICENSE               # MIT licence
├── 📦 setup.py              # Instalační skript
├── 🔧 .gitignore            # Git ignore rules
├── 📈 CHANGELOG.md          # Historie změn
├── 📁 docs/                 # Dokumentace
├── 📁 examples/             # Příklady použití
└── 📄 GITHUB_GUIDE.md       # Tento soubor
```

## ✅ Checklist před publikací

- [x] README.md je kompletní a informativní
- [x] .gitignore obsahuje všechny potřebné exclusions
- [x] LICENSE je přítomen (MIT)
- [x] requirements.txt je vytvořen
- [x] Kód je funkční a otestovaný
- [x] Dokumentace je úplná
- [x] CHANGELOG.md popisuje verzi 1.0.0
- [ ] GitHub repositář je vytvořen
- [ ] Odkazy jsou aktualizované
- [ ] První commit je proveden
- [ ] Release v1.0.0 je vytvořen

## 🎉 Po publikaci

1. **Sdílení**: Sdílejte odkaz s kolegy a komunitou
2. **Issues**: Sledujte GitHub Issues pro feedback
3. **Contributions**: Vítejte pull requests od ostatních
4. **Updates**: Pravidelně aktualizujte nástroj dle potřeb
5. **Documentation**: Rozšiřujte dokumentaci na základě dotazů uživatelů

---

**Tip**: Po publikaci můžete nástroj instalovat přímo z GitHub:
```bash
pip install git+https://github.com/YOUR_USERNAME/enzyme-kinetics-extractor.git
```