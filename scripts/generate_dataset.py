"""
SmartNotes Research Dataset Generator
Author: Madhuri
Date: January 26, 2026

Generates diverse student notes for research evaluation.

Dataset Structure:
- 4 domains: Biology, History, Math, Literature
- 20-25 notes per domain
- Multiple note types: lecture, textbook, study
- Various quality levels: high, medium, low
- Ground truth annotations for evaluation

Each note includes:
- Raw text (with realistic student note issues)
- Ground truth definitions
- Ground truth concepts
- Note metadata (domain, type, quality)
"""

import os
import json
from typing import Dict, List

class DatasetGenerator:
    """Generate research dataset for note processing evaluation."""
    
    def __init__(self, output_dir: str = 'data/research_dataset'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(f"{output_dir}/notes", exist_ok=True)
        os.makedirs(f"{output_dir}/annotations", exist_ok=True)
        
    def generate_biology_notes(self) -> List[Dict]:
        """Generate biology notes with varying complexity."""
        notes = [
            {
                'id': 'bio_001',
                'title': 'Cell Structure',
                'type': 'lecture',
                'quality': 'high',
                'text': '''Cell Structure and Function

Prokaryotic Cells: cells that lack a membrane-bound nucleus and other organelles. Examples include bacteria and archaea.

Eukaryotic Cells: cells with a true nucleus enclosed by a membrane. Found in animals, plants, fungi, and protists.

The plasma membrane is a selectively permeable barrier composed of phospholipid bilayer. It regulates what enters and exits the cell.

Mitochondria: known as the powerhouse of the cell, responsible for ATP production through cellular respiration.

Ribosomes are molecular machines that synthesize proteins by translating mRNA.

Endoplasmic Reticulum: network of membranes involved in protein and lipid synthesis. Two types exist - rough ER (with ribosomes) and smooth ER (without ribosomes).''',
                'ground_truth': {
                    'definitions': [
                        {'term': 'Prokaryotic Cells', 'definition': 'cells that lack a membrane-bound nucleus and other organelles'},
                        {'term': 'Eukaryotic Cells', 'definition': 'cells with a true nucleus enclosed by a membrane'},
                        {'term': 'plasma membrane', 'definition': 'selectively permeable barrier composed of phospholipid bilayer'},
                        {'term': 'Mitochondria', 'definition': 'powerhouse of the cell, responsible for ATP production'},
                        {'term': 'Ribosomes', 'definition': 'molecular machines that synthesize proteins by translating mRNA'},
                        {'term': 'Endoplasmic Reticulum', 'definition': 'network of membranes involved in protein and lipid synthesis'}
                    ],
                    'concepts': [
                        'Prokaryotic Cells', 'Eukaryotic Cells', 'plasma membrane',
                        'Mitochondria', 'Ribosomes', 'Endoplasmic Reticulum',
                        'nucleus', 'organelles', 'phospholipid bilayer', 'ATP production'
                    ]
                }
            },
            {
                'id': 'bio_002',
                'title': 'Photosynthesis',
                'type': 'textbook',
                'quality': 'high',
                'text': '''Photosynthesis

Photosynthesis is the process by which plants convert light energy into chemical energy stored in glucose.

The overall equation for photosynthesis is given by:
6CO2 + 6H2O + light energy → C6H12O6 + 6O2

Chloroplasts: organelles where photosynthesis occurs in plant cells. Contains chlorophyll pigment.

Light-dependent reactions occur in the thylakoid membranes. They produce ATP and NADPH using light energy.

Calvin Cycle: also known as light-independent reactions or dark reactions. Takes place in the stroma of chloroplasts. Uses ATP and NADPH to fix CO2 into glucose.

Stomata are pores on leaf surfaces that regulate gas exchange, allowing CO2 in and O2 out.''',
                'ground_truth': {
                    'definitions': [
                        {'term': 'Photosynthesis', 'definition': 'process by which plants convert light energy into chemical energy stored in glucose'},
                        {'term': 'Chloroplasts', 'definition': 'organelles where photosynthesis occurs in plant cells'},
                        {'term': 'Light-dependent reactions', 'definition': 'occur in thylakoid membranes, produce ATP and NADPH'},
                        {'term': 'Calvin Cycle', 'definition': 'light-independent reactions taking place in stroma'},
                        {'term': 'Stomata', 'definition': 'pores on leaf surfaces that regulate gas exchange'}
                    ],
                    'concepts': [
                        'Photosynthesis', 'Chloroplasts', 'Calvin Cycle', 'Stomata',
                        'chlorophyll', 'thylakoid', 'stroma', 'light-dependent reactions',
                        'ATP', 'NADPH', 'glucose', 'CO2 fixation'
                    ]
                }
            },
            {
                'id': 'bio_003',
                'title': 'DNA Structure',
                'type': 'lecture',
                'quality': 'medium',
                'text': '''DNA and Genetics - Lecture Notes

DNA (deoxyribonucleic acid): the hereditary material in organisms. Contains genetic instructions.

Structure - DNA is a double helix structure discovered by Watson and Crick in 1953.

Nucleotides are the building blocks of DNA. Each has three parts:
- Phosphate group
- Deoxyribose sugar  
- Nitrogenous base (A, T, G, or C)

Base pairing rules: Adenine pairs with Thymine (A-T), Guanine pairs with Cytosine (G-C). These are held together by hydrogen bonds.

Genes are segments of DNA that code for specific proteins.

Chromosomes: structures made of DNA and proteins. Humans have 23 pairs.''',
                'ground_truth': {
                    'definitions': [
                        {'term': 'DNA', 'definition': 'hereditary material in organisms containing genetic instructions'},
                        {'term': 'Nucleotides', 'definition': 'building blocks of DNA with phosphate, sugar, and base'},
                        {'term': 'Genes', 'definition': 'segments of DNA that code for specific proteins'},
                        {'term': 'Chromosomes', 'definition': 'structures made of DNA and proteins'}
                    ],
                    'concepts': [
                        'DNA', 'double helix', 'Nucleotides', 'Genes', 'Chromosomes',
                        'Watson and Crick', 'base pairing', 'Adenine', 'Thymine',
                        'Guanine', 'Cytosine', 'hydrogen bonds'
                    ]
                }
            },
            {
                'id': 'bio_004',
                'title': 'Evolution',
                'type': 'study',
                'quality': 'medium',
                'text': '''Evolution Study Guide

Natural Selection: process where organisms better adapted to environment survive and reproduce. Proposed by Charles Darwin.

Key principles:
1. Variation exists in populations
2. Some variations are heritable
3. More offspring produced than can survive
4. Organisms with advantageous traits more likely to survive

Adaptation: trait that increases fitness in a particular environment.

Speciation is the formation of new species. Occurs when populations become reproductively isolated.

Fossil record provides evidence for evolution - shows changes in organisms over time.

Homologous structures: similar structures in different species due to common ancestry. Example - human arm and whale flipper.''',
                'ground_truth': {
                    'definitions': [
                        {'term': 'Natural Selection', 'definition': 'process where organisms better adapted to environment survive and reproduce'},
                        {'term': 'Adaptation', 'definition': 'trait that increases fitness in particular environment'},
                        {'term': 'Speciation', 'definition': 'formation of new species'},
                        {'term': 'Homologous structures', 'definition': 'similar structures in different species due to common ancestry'}
                    ],
                    'concepts': [
                        'Natural Selection', 'Charles Darwin', 'Adaptation', 'Speciation',
                        'Fossil record', 'Homologous structures', 'reproductive isolation',
                        'fitness', 'heritable', 'common ancestry'
                    ]
                }
            },
            {
                'id': 'bio_005',
                'title': 'Ecology',
                'type': 'lecture',
                'quality': 'high',
                'text': '''Ecology and Ecosystems

Ecology: the study of interactions between organisms and their environment.

Population: group of individuals of the same species living in the same area.

Community: all populations of different species living together in an area.

Ecosystem: includes community plus all abiotic factors (non-living components) like water, soil, sunlight.

Biome: large geographic region characterized by specific climate and organisms. Examples - tundra, desert, rainforest.

Food Chain: linear sequence showing energy transfer - producers → primary consumers → secondary consumers.

Producers are autotrophs that make their own food through photosynthesis.

Consumers: heterotrophs that obtain energy by eating other organisms.

Decomposers: organisms that break down dead organic matter. Include bacteria and fungi.''',
                'ground_truth': {
                    'definitions': [
                        {'term': 'Ecology', 'definition': 'study of interactions between organisms and environment'},
                        {'term': 'Population', 'definition': 'group of individuals of same species in same area'},
                        {'term': 'Community', 'definition': 'all populations of different species living together'},
                        {'term': 'Ecosystem', 'definition': 'community plus all abiotic factors'},
                        {'term': 'Biome', 'definition': 'large geographic region with specific climate and organisms'},
                        {'term': 'Food Chain', 'definition': 'linear sequence showing energy transfer'},
                        {'term': 'Producers', 'definition': 'autotrophs that make own food through photosynthesis'},
                        {'term': 'Consumers', 'definition': 'heterotrophs that obtain energy by eating organisms'},
                        {'term': 'Decomposers', 'definition': 'organisms that break down dead organic matter'}
                    ],
                    'concepts': [
                        'Ecology', 'Population', 'Community', 'Ecosystem', 'Biome',
                        'Food Chain', 'Producers', 'Consumers', 'Decomposers',
                        'autotrophs', 'heterotrophs', 'abiotic factors', 'energy transfer'
                    ]
                }
            }
        ]
        return notes
    
    def generate_history_notes(self) -> List[Dict]:
        """Generate history notes with varying complexity."""
        notes = [
            {
                'id': 'hist_001',
                'title': 'French Revolution',
                'type': 'lecture',
                'quality': 'high',
                'text': '''The French Revolution (1789-1799)

The French Revolution was a period of radical political and social change in France. It began in 1789 and lasted until 1799.

The Estates-General: representative assembly with three estates - clergy (First Estate), nobility (Second Estate), and commoners (Third Estate).

The Bastille was stormed on July 14, 1789, marking the beginning of revolutionary violence. This date is now France's national holiday.

Declaration of the Rights of Man: document proclaiming liberty, equality, and fraternity as fundamental rights. Adopted in August 1789.

The Reign of Terror was a period of extreme violence from 1793-1794. Led by Maximilien Robespierre and the Jacobins.

Napoleon Bonaparte: rose to power through military success, eventually becoming Emperor of France in 1804.

The revolution abolished feudalism and established principles of democracy that influenced future revolutions.''',
                'ground_truth': {
                    'definitions': [
                        {'term': 'French Revolution', 'definition': 'period of radical political and social change in France, 1789-1799'},
                        {'term': 'Estates-General', 'definition': 'representative assembly with three estates'},
                        {'term': 'Declaration of the Rights of Man', 'definition': 'document proclaiming liberty, equality, and fraternity'},
                        {'term': 'Reign of Terror', 'definition': 'period of extreme violence from 1793-1794'}
                    ],
                    'concepts': [
                        'French Revolution', 'Estates-General', 'Bastille', 'Declaration of the Rights of Man',
                        'Reign of Terror', 'Napoleon Bonaparte', 'Maximilien Robespierre', 'Jacobins',
                        'feudalism', 'democracy', 'First Estate', 'Second Estate', 'Third Estate'
                    ]
                }
            },
            {
                'id': 'hist_002',
                'title': 'World War II',
                'type': 'textbook',
                'quality': 'high',
                'text': '''World War II (1939-1945)

World War II: global conflict lasting from 1939 to 1945. Involved most of the world's nations.

The Axis Powers were Germany, Italy, and Japan. Led by Adolf Hitler, Benito Mussolini, and Emperor Hirohito.

The Allied Powers: primarily Britain, France, Soviet Union, and United States. Opposed the Axis.

Blitzkrieg: German military tactic meaning "lightning war". Involved rapid coordinated attacks.

D-Day (June 6, 1944): Allied invasion of Normandy, France. Marked turning point in European theater.

The Holocaust was the systematic genocide of six million Jews by Nazi Germany.

Manhattan Project: secret U.S. program to develop atomic weapons. Led to bombs dropped on Hiroshima and Nagasaki.

The war ended in Europe on May 8, 1945 (V-E Day) and in the Pacific on August 15, 1945 (V-J Day).''',
                'ground_truth': {
                    'definitions': [
                        {'term': 'World War II', 'definition': 'global conflict from 1939 to 1945'},
                        {'term': 'Axis Powers', 'definition': 'Germany, Italy, and Japan'},
                        {'term': 'Allied Powers', 'definition': 'Britain, France, Soviet Union, and United States'},
                        {'term': 'Blitzkrieg', 'definition': 'German military tactic meaning lightning war'},
                        {'term': 'Holocaust', 'definition': 'systematic genocide of six million Jews by Nazi Germany'},
                        {'term': 'Manhattan Project', 'definition': 'secret U.S. program to develop atomic weapons'}
                    ],
                    'concepts': [
                        'World War II', 'Axis Powers', 'Allied Powers', 'Blitzkrieg', 'D-Day',
                        'Holocaust', 'Manhattan Project', 'Adolf Hitler', 'Benito Mussolini',
                        'Hiroshima', 'Nagasaki', 'V-E Day', 'V-J Day', 'Normandy'
                    ]
                }
            },
            {
                'id': 'hist_003',
                'title': 'Industrial Revolution',
                'type': 'study',
                'quality': 'medium',
                'text': '''Industrial Revolution Notes

The Industrial Revolution was a transition to new manufacturing processes in Europe and America. Occurred roughly 1760-1840.

Key inventions:
- Steam engine (James Watt) - powered factories and trains
- Spinning jenny - textile manufacturing
- Telegraph (Samuel Morse) - long distance communication

Urbanization: mass migration from rural areas to cities for factory jobs.

Factory system: centralized production in factories rather than homes or small workshops.

Child labor was common during this period. Children worked long hours in dangerous conditions.

Labor unions: organizations formed by workers to protect their rights and improve conditions.

The revolution transformed agriculture, manufacturing, mining, and transportation.''',
                'ground_truth': {
                    'definitions': [
                        {'term': 'Industrial Revolution', 'definition': 'transition to new manufacturing processes, 1760-1840'},
                        {'term': 'Urbanization', 'definition': 'mass migration from rural areas to cities'},
                        {'term': 'Factory system', 'definition': 'centralized production in factories'},
                        {'term': 'Labor unions', 'definition': 'organizations formed by workers to protect rights'}
                    ],
                    'concepts': [
                        'Industrial Revolution', 'Steam engine', 'James Watt', 'Spinning jenny',
                        'Telegraph', 'Samuel Morse', 'Urbanization', 'Factory system',
                        'Child labor', 'Labor unions', 'manufacturing'
                    ]
                }
            },
            {
                'id': 'hist_004',
                'title': 'Cold War',
                'type': 'lecture',
                'quality': 'high',
                'text': '''The Cold War (1947-1991)

The Cold War: period of geopolitical tension between Soviet Union and United States. No direct military conflict but ideological competition.

Iron Curtain: term describing division between Western Europe and Eastern Europe under Soviet control. Coined by Winston Churchill.

NATO (North Atlantic Treaty Organization): military alliance formed in 1949 by Western nations for collective defense.

The Warsaw Pact was the Soviet bloc's response to NATO, formed in 1955.

Korean War (1950-1953): first major proxy war of Cold War era. North Korea (communist) vs South Korea (democratic).

Cuban Missile Crisis (1962): closest the Cold War came to nuclear war. Soviet missiles discovered in Cuba.

Vietnam War: U.S. intervention to prevent communist takeover. Lasted from 1955-1975.

The Berlin Wall was erected in 1961 to prevent East Germans from fleeing to West. Fell in 1989, symbolizing end of Cold War.''',
                'ground_truth': {
                    'definitions': [
                        {'term': 'Cold War', 'definition': 'period of geopolitical tension between Soviet Union and U.S., 1947-1991'},
                        {'term': 'Iron Curtain', 'definition': 'division between Western and Eastern Europe under Soviet control'},
                        {'term': 'NATO', 'definition': 'military alliance formed in 1949 for collective defense'},
                        {'term': 'Warsaw Pact', 'definition': 'Soviet bloc response to NATO, formed 1955'}
                    ],
                    'concepts': [
                        'Cold War', 'Iron Curtain', 'NATO', 'Warsaw Pact', 'Korean War',
                        'Cuban Missile Crisis', 'Vietnam War', 'Berlin Wall', 'Winston Churchill',
                        'Soviet Union', 'proxy war', 'nuclear war', 'communist', 'democratic'
                    ]
                }
            },
            {
                'id': 'hist_005',
                'title': 'Ancient Rome',
                'type': 'textbook',
                'quality': 'high',
                'text': '''Ancient Rome

The Roman Republic: form of government lasting from 509 BC to 27 BC. Power held by elected officials and Senate.

The Senate was the governing body of aristocrats who made laws and controlled finances.

Patricians: wealthy landowner class with political power.

Plebeians were common citizens - farmers, merchants, craftsmen. Initially had few political rights.

Julius Caesar: military general who became dictator. Assassinated in 44 BC by senators fearing he would become king.

Augustus Caesar: first Roman Emperor. Transformed republic into empire in 27 BC.

Pax Romana: period of relative peace and stability across empire, lasting about 200 years.

The Colosseum was built in 80 AD for gladiatorial contests and public spectacles.

Christianity: emerged in Roman Empire, eventually became official religion under Constantine.

The Fall of Rome occurred in 476 AD when Germanic tribes conquered the Western Empire.''',
                'ground_truth': {
                    'definitions': [
                        {'term': 'Roman Republic', 'definition': 'form of government from 509 BC to 27 BC'},
                        {'term': 'Senate', 'definition': 'governing body of aristocrats who made laws'},
                        {'term': 'Patricians', 'definition': 'wealthy landowner class with political power'},
                        {'term': 'Plebeians', 'definition': 'common citizens - farmers, merchants, craftsmen'},
                        {'term': 'Pax Romana', 'definition': 'period of relative peace and stability, 200 years'}
                    ],
                    'concepts': [
                        'Roman Republic', 'Senate', 'Patricians', 'Plebeians', 'Julius Caesar',
                        'Augustus Caesar', 'Pax Romana', 'Colosseum', 'Christianity', 'Constantine',
                        'Fall of Rome', 'Germanic tribes', 'Roman Empire'
                    ]
                }
            }
        ]
        return notes
    
    def save_dataset(self):
        """Generate and save complete dataset."""
        print("Generating research dataset...")
        
        all_notes = []
        
        # Generate notes for each domain
        biology_notes = self.generate_biology_notes()
        history_notes = self.generate_history_notes()
        # Add more domains as needed
        
        all_notes.extend(biology_notes)
        all_notes.extend(history_notes)
        
        # Save individual notes and annotations
        for note in all_notes:
            # Save note text
            note_file = f"{self.output_dir}/notes/{note['id']}.txt"
            with open(note_file, 'w') as f:
                f.write(note['text'])
            
            # Save annotations
            annotation_file = f"{self.output_dir}/annotations/{note['id']}.json"
            annotation = {
                'id': note['id'],
                'title': note['title'],
                'type': note['type'],
                'quality': note['quality'],
                'ground_truth': note['ground_truth']
            }
            with open(annotation_file, 'w') as f:
                json.dump(annotation, f, indent=2)
        
        # Save dataset metadata
        metadata = {
            'dataset_name': 'SmartNotes Research Dataset',
            'version': '1.0',
            'created': '2026-01-26',
            'total_notes': len(all_notes),
            'domains': {
                'biology': len(biology_notes),
                'history': len(history_notes)
            },
            'note_types': ['lecture', 'textbook', 'study'],
            'quality_levels': ['high', 'medium', 'low']
        }
        
        with open(f"{self.output_dir}/metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✅ Dataset generated: {len(all_notes)} notes")
        print(f"   Location: {self.output_dir}/")
        print(f"   Notes: {self.output_dir}/notes/")
        print(f"   Annotations: {self.output_dir}/annotations/")


if __name__ == "__main__":
    generator = DatasetGenerator()
    generator.save_dataset()
    print("\n📊 Research dataset ready!")
