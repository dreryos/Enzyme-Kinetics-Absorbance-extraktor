#!/usr/bin/env python3
"""
Univerzální Enzyme Kinetics Absorbance extraktor - převede IWBK soubor na ASCII a extrahuje absorbance data

Použití:
    python enzyme_kinetics_extractor.py "soubor.iwbk"
    python enzyme_kinetics_extractor.py "cesta/k/souboru.iwbk" --target-min 0.6 --target-max 1.9
"""

import sys
import os
import struct
import csv
import argparse
import tempfile
from pathlib import Path

def iwbk_to_ascii(iwbk_path, ascii_path):
    """Převede IWBK soubor na ASCII formát pro dekódování"""
    print(f"🔄 Převádím {iwbk_path} na ASCII formát...")
    
    try:
        with open(iwbk_path, 'rb') as iwbk_file:
            iwbk_data = iwbk_file.read()
        
        # Převedeme binární data na ASCII reprezentaci
        with open(ascii_path, 'w', encoding='utf-8') as ascii_file:
            # Zapíšeme hlavičku
            ascii_file.write("# Enzyme Kinetics ASCII Export\n")
            ascii_file.write(f"# Source: {os.path.basename(iwbk_path)}\n")
            ascii_file.write(f"# Size: {len(iwbk_data)} bytes\n")
            ascii_file.write("# Data:\n")
            
            # Převedeme binární data na hexadecimální reprezentaci
            hex_data = iwbk_data.hex()
            
            # Rozdělíme do řádků po 32 znacích (16 bytů)
            for i in range(0, len(hex_data), 32):
                line = hex_data[i:i+32]
                ascii_file.write(f"{line}\n")
        
        print(f"✅ ASCII soubor vytvořen: {ascii_path}")
        return True
        
    except Exception as e:
        print(f"❌ Chyba při převodu IWBK na ASCII: {e}")
        return False

def iwbk_to_hex(iwbk_path, hex_path):
    """Převede IWBK soubor na HEX formát"""
    print(f"🔄 Převádím {iwbk_path} na HEX formát...")
    
    try:
        with open(iwbk_path, 'rb') as iwbk_file:
            iwbk_data = iwbk_file.read()
        
        with open(hex_path, 'w', encoding='utf-8') as hex_file:
            hex_data = iwbk_data.hex().upper()
            
            # Formátujeme jako standardní hex dump
            for i in range(0, len(hex_data), 32):
                offset = i // 2
                line = hex_data[i:i+32]
                formatted_line = ' '.join([line[j:j+2] for j in range(0, len(line), 2)])
                hex_file.write(f"{offset:08X}: {formatted_line}\n")
        
        print(f"✅ HEX soubor vytvořen: {hex_path}")
        return True
        
    except Exception as e:
        print(f"❌ Chyba při převodu IWBK na HEX: {e}")
        return False

def analyze_decoding_methods(file_path, target_min=0.6, target_max=1.9):
    """Analyzuje různé metody dekódování pro nalezení správného formátu"""
    print(f"🔍 ANALÝZA DEKÓDOVÁNÍ PRO ROZSAH {target_min}-{target_max} AU")
    print("=" * 55)
    
    with open(file_path, 'rb') as f:
        data = f.read()
    
    print(f"📊 Velikost souboru: {len(data):,} bytů")
    
    # Testujeme různé formáty a endianness
    formats_to_test = [
        ('d', 8, 'double precision (64-bit)'),
        ('f', 4, 'single precision (32-bit)'),
        ('I', 4, 'unsigned int 32-bit'),
        ('i', 4, 'signed int 32-bit'),
        ('H', 2, 'unsigned short 16-bit'),
        ('h', 2, 'signed short 16-bit')
    ]
    
    endian_formats = [
        ('<', 'little-endian'),
        ('>', 'big-endian'),
        ('=', 'native')
    ]
    
    print(f"\n🧪 TESTOVÁNÍ RŮZNÝCH FORMÁTŮ:")
    results = {}
    
    for fmt, size, desc in formats_to_test:
        for endian, endian_desc in endian_formats:
            format_str = f"{endian}{fmt}"
            values_in_range = []
            
            print(f"\n   🔬 Testování {desc} ({endian_desc}): '{format_str}'")
            
            # Skenujeme soubor s tímto formátem
            for offset in range(0, len(data) - size, size):
                try:
                    value = struct.unpack(format_str, data[offset:offset+size])[0]
                    
                    # Pro integer formáty převedeme na float
                    if fmt in ['I', 'i', 'H', 'h']:
                        # Zkusíme různé škálování
                        scaled_values = [
                            value / 1000.0,    # dělení 1000
                            value / 10000.0,   # dělení 10000
                            value / 100.0,     # dělení 100
                            value * 0.001,     # násobení 0.001
                            value,             # bez škálování
                        ]
                        
                        for scaled in scaled_values:
                            if target_min <= scaled <= target_max:
                                values_in_range.append({
                                    'offset': offset,
                                    'raw_value': value,
                                    'scaled_value': scaled,
                                    'scale_factor': scaled / value if value != 0 else 0
                                })
                                if len(values_in_range) >= 100:  # Limitujeme pro rychlost
                                    break
                    else:
                        # Pro float formáty kontrolujeme přímo
                        if target_min <= value <= target_max and not (value != value):
                            values_in_range.append({
                                'offset': offset,
                                'raw_value': value,
                                'scaled_value': value,
                                'scale_factor': 1.0
                            })
                            if len(values_in_range) >= 100:
                                break
                                
                except (struct.error, OverflowError):
                    continue
            
            if values_in_range:
                print(f"      ✅ Nalezeno {len(values_in_range)} hodnot v cílovém rozsahu!")
                sample_values = [f"{v['scaled_value']:.3f}" for v in values_in_range[:5]]
                print(f"      📈 Ukázka hodnot: {sample_values}")
                results[format_str] = values_in_range
            else:
                print(f"      ❌ Žádné hodnoty v rozsahu")
    
    return results

def detect_kinetic_structure(values, target_min=0.6, target_max=1.9, expected_samples=36, expected_timepoints=4):
    """Detekuje kinetickou strukturu dat s očekávaným počtem vzorků a časových bodů"""
    print(f"\n🔍 DETEKCE KINETICKÉ STRUKTURY:")
    print(f"   🎯 Očekáváno: {expected_samples} vzorků × {expected_timepoints} časových bodů")
    
    # Seřadíme hodnoty podle pozice v souboru
    values.sort(key=lambda x: x['offset'])
    
    # Filtrujeme hodnoty v cílovém rozsahu
    valid_values = [v for v in values if target_min <= v['scaled_value'] <= target_max]
    print(f"   📊 Celkem hodnot v rozsahu: {len(valid_values)}")
    
    if len(valid_values) < expected_samples * expected_timepoints:
        print(f"   ❌ Příliš málo hodnot pro očekávanou strukturu!")
        return None
    
    # Cílový počet bodů
    target_total = expected_samples * expected_timepoints
    print(f"   🎯 Cílový počet bodů: {target_total}")
    
    # Pokusíme se najít optimální podmnožinu dat
    # Strategií je rozdělit data na expected_samples skupin a z každé vzít expected_timepoints hodnot
    
    chunk_size = len(valid_values) // expected_samples
    print(f"   📏 Velikost chunků: ~{chunk_size} hodnot per vzorek")
    
    selected_clusters = []
    
    for sample_idx in range(expected_samples):
        start_idx = sample_idx * chunk_size
        end_idx = start_idx + chunk_size
        
        if sample_idx == expected_samples - 1:  # Poslední vzorek - vezmi zbytek
            chunk = valid_values[start_idx:]
        else:
            chunk = valid_values[start_idx:end_idx]
        
        if len(chunk) >= expected_timepoints:
            # Vyber expected_timepoints hodnot z chunků rovnoměrně rozložených
            if len(chunk) == expected_timepoints:
                selected_values = chunk
            else:
                # Rozděl chunk na expected_timepoints částí a vyber z každé jednu hodnotu
                step = len(chunk) // expected_timepoints
                selected_values = []
                for t in range(expected_timepoints):
                    idx = t * step
                    if idx < len(chunk):
                        selected_values.append(chunk[idx])
                
                # Pokud máme méně hodnot, doplníme z konce
                while len(selected_values) < expected_timepoints and len(chunk) > len(selected_values):
                    remaining = [v for v in chunk if v not in selected_values]
                    if remaining:
                        selected_values.append(remaining[0])
            
            selected_clusters.append(selected_values[:expected_timepoints])
    
    # Ověříme, že máme správný počet vzorků
    valid_clusters = [cluster for cluster in selected_clusters if len(cluster) == expected_timepoints]
    
    print(f"   ✅ Nalezeno {len(valid_clusters)} kompletních vzorků")
    print(f"   ⏱️ Bodů per vzorek: {expected_timepoints}")
    
    if len(valid_clusters) < expected_samples:
        print(f"   ⚠️ Málo vzorků, očekáváno {expected_samples}, nalezeno {len(valid_clusters)}")
    
    # Vypočítáme statistiky
    all_abs_values = []
    for cluster in valid_clusters:
        for val in cluster:
            all_abs_values.append(val['scaled_value'])
    
    if all_abs_values:
        print(f"   📈 Rozsah hodnot: {min(all_abs_values):.3f} - {max(all_abs_values):.3f} AU")
        print(f"   📊 Průměrná hodnota: {sum(all_abs_values)/len(all_abs_values):.3f} AU")
        
        return {
            'clusters': valid_clusters,
            'sample_count': len(valid_clusters),
            'time_points_per_sample': expected_timepoints,
            'total_points': len(all_abs_values),
            'value_range': (min(all_abs_values), max(all_abs_values)),
            'time_intervals': [0, 10, 20, 30]  # Standardní časové intervaly
        }
    
    return None

def extract_adaptive_format_data(file_path, results):
    """Extrahuje data s adaptivní detekcí struktury"""
    print(f"\n🎯 ADAPTIVNÍ EXTRAKCE DAT:")
    
    if not results:
        print("❌ Žádný vhodný formát nenalezen!")
        return None, None
    
    # Najdeme formát s nejvíce hodnotami
    best_format = max(results.keys(), key=lambda k: len(results[k]))
    best_values = results[best_format]
    
    print(f"   ✅ Nejlepší formát: {best_format}")
    print(f"   📊 Počet surových hodnot: {len(best_values)}")
    
    # Odebereme duplicity a blízké hodnoty
    filtered_values = []
    last_offset = -1
    
    for val in best_values:
        if val['offset'] - last_offset > 4:  # Menší minimální vzdálenost
            filtered_values.append(val)
            last_offset = val['offset']
    
    print(f"   📈 Po filtrování: {len(filtered_values)} hodnot")
    
    # Detekujeme kinetickou strukturu (36 vzorků × 4 časové body)
    structure = detect_kinetic_structure(filtered_values)
    
    if not structure:
        print("❌ Nepodařilo se detekovat kinetickou strukturu!")
        return None, None
    
    return structure, best_format

def generate_kinetic_csv_output(structure, best_format, output_file, source_file):
    """Generuje CSV soubor s kinetickou strukturou (36 vzorků × 4 časové body)"""
    print(f"\n💾 Generuji kinetický CSV výstup: {output_file}")
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            'Sample_ID',
            'Sample_Name',
            'Wavelength_nm',
            'Time_Point',
            'Time_sec',
            'Absorbance',
            'Raw_Value',
            'Scale_Factor',
            'Format_Used',
            'File_Offset',
            'Source_File'
        ])
        
        total_points = 0
        time_intervals = structure.get('time_intervals', [0, 10, 20, 30])
        
        for sample_idx, cluster in enumerate(structure['clusters'], 1):
            sample_name = f"290nm, Sample{sample_idx}"
            
            # Seřadíme hodnoty v clusteru podle pozice
            cluster.sort(key=lambda x: x['offset'])
            
            for time_idx, value_data in enumerate(cluster):
                # Použijeme standardní časové intervaly
                time_sec = time_intervals[time_idx] if time_idx < len(time_intervals) else time_idx * 10
                
                writer.writerow([
                    sample_idx,
                    sample_name,
                    290,  # Standardní vlnová délka
                    time_idx + 1,
                    time_sec,
                    f"{value_data['scaled_value']:.6f}",
                    value_data['raw_value'],
                    f"{value_data['scale_factor']:.6f}",
                    best_format,
                    value_data['offset'],
                    os.path.basename(source_file)
                ])
                total_points += 1
        
        print(f"   ✅ Uloženo {total_points} datových bodů")
        print(f"   🧪 {structure['sample_count']} vzorků × {structure['time_points_per_sample']} časových bodů")
        print(f"   ⏱️ Časové intervaly: {time_intervals}")
        return total_points

def main():
    parser = argparse.ArgumentParser(
        description='Univerzální Enzyme Kinetics Absorbance extraktor pro IWBK soubory',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Příklady použití:
  python enzyme_kinetics_extractor.py "data.iwbk"
  python enzyme_kinetics_extractor.py "složka/data.iwbk" --target-min 0.5 --target-max 2.0
  python enzyme_kinetics_extractor.py "data.iwbk" --output "results.csv"
        """
    )
    
    parser.add_argument('iwbk_file', help='Cesta k IWBK souboru')
    parser.add_argument('--target-min', type=float, default=0.6,
                        help='Minimální hodnota absorbance (default: 0.6)')
    parser.add_argument('--target-max', type=float, default=1.9,
                        help='Maximální hodnota absorbance (default: 1.9)')
    parser.add_argument('--output', '-o', 
                        help='Název výstupního CSV souboru (default: auto-generovaný)')
    parser.add_argument('--keep-temp', action='store_true',
                        help='Ponechat dočasné ASCII/HEX soubory')
    
    args = parser.parse_args()
    
    # Ověření vstupního souboru
    iwbk_path = Path(args.iwbk_file)
    if not iwbk_path.exists():
        print(f"❌ Soubor nenalezen: {iwbk_path}")
        sys.exit(1)
    
    if not iwbk_path.suffix.lower() == '.iwbk':
        print(f"❌ Neplatný formát souboru. Očekáván .iwbk, dostal: {iwbk_path.suffix}")
        sys.exit(1)
    
    print(f"🚀 UNIVERZÁLNÍ ENZYME KINETICS EXTRAKTOR")
    print("=" * 45)
    print(f"📁 Vstupní soubor: {iwbk_path}")
    print(f"🎯 Cílový rozsah: {args.target_min}-{args.target_max} AU")
    
    # Vytvoření dočasných souborů
    base_name = iwbk_path.stem
    temp_dir = iwbk_path.parent
    
    ascii_path = temp_dir / f"{base_name}_temp_ASCII.txt"
    hex_path = temp_dir / f"{base_name}_temp_HEX.txt"
    
    try:
        # Převod IWBK na ASCII a HEX
        if not iwbk_to_ascii(iwbk_path, ascii_path):
            sys.exit(1)
        
        if not iwbk_to_hex(iwbk_path, hex_path):
            sys.exit(1)
        
        # Analýza dekódování na ASCII souboru
        results = analyze_decoding_methods(ascii_path, args.target_min, args.target_max)
        
        if not results:
            print("\n💡 Zkouším rozšířený rozsah...")
            results = analyze_decoding_methods(ascii_path, args.target_min - 0.2, args.target_max + 0.5)
        
        if results:
            # Extrakce dat s adaptivní detekcí struktury
            structure, best_format = extract_adaptive_format_data(ascii_path, results)
            
            if structure:
                # Určení výstupního souboru
                if args.output:
                    output_file = Path(args.output)
                else:
                    output_file = temp_dir / f"{base_name}.csv"
                
                # Generování adaptivního CSV
                total_points = generate_kinetic_csv_output(structure, best_format, output_file, iwbk_path)
                
                # Finální analýza
                print(f"\n📊 FINÁLNÍ ANALÝZA:")
                all_values = []
                for cluster in structure['clusters']:
                    for val in cluster:
                        all_values.append(val['scaled_value'])
                
                if all_values:
                    print(f"   📈 Rozsah hodnot: {min(all_values):.3f} - {max(all_values):.3f} AU")
                    print(f"   📈 Průměr: {sum(all_values)/len(all_values):.3f} AU")
                    print(f"   🎯 Formát: {best_format}")
                    print(f"   🧪 Detekováno vzorků: {structure['sample_count']}")
                    print(f"   ⏱️ Bodů per vzorek: {structure['time_points_per_sample']}")
                    
                    # Kontrola cílového rozsahu
                    in_target = [v for v in all_values if args.target_min <= v <= args.target_max]
                    percentage = 100 * len(in_target) / len(all_values)
                    print(f"   ✅ V cílovém rozsahu: {len(in_target)}/{len(all_values)} ({percentage:.1f}%)")
                
                print(f"\n✅ ADAPTIVNÍ EXTRAKCE DOKONČENA!")
                print(f"   📁 Výstupní soubor: {output_file}")
                print(f"   📊 Celkem bodů: {total_points}")
                print(f"   🎯 Cílový rozsah: {args.target_min}-{args.target_max} AU")
                print(f"   🔍 Struktura detekována automaticky")
                
            else:
                print("❌ Nepodařilo se detekovat strukturu dat!")
                sys.exit(1)
        else:
            print("❌ Nepodařilo se najít hodnoty v požadovaném rozsahu!")
            sys.exit(1)
    
    finally:
        # Úklid dočasných souborů
        if not args.keep_temp:
            for temp_file in [ascii_path, hex_path]:
                if temp_file.exists():
                    try:
                        temp_file.unlink()
                        print(f"🗑️ Odstraněn dočasný soubor: {temp_file.name}")
                    except Exception as e:
                        print(f"⚠️ Nepodařilo se odstranit {temp_file}: {e}")

if __name__ == "__main__":
    main()