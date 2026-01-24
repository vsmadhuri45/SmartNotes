# SmartNotes: Intelligent Knowledge Retention Assistant

## Project Overview
AI-powered system for automatic note structuring, personalized forgetting prediction, and knowledge graph integration.

## 🎯 Project Objectives
1. **Automatic Note Structuring** - Transform raw notes into retention-optimized formats
2. **Personalized Forgetting Prediction** - ML model predicting when you'll forget concepts
3. **Knowledge Graph Integration** - Automatically connect new knowledge to existing concepts

## 📁 Project Structure
```
SmartNotes/
├── src/
│   ├── note_processor/      # Module 1: Note structuring
│   ├── forgetting_predictor/ # Module 2: Forgetting prediction
│   ├── knowledge_graph/      # Module 3: Knowledge graph
│   └── utils/                # Shared utilities
├── data/
│   ├── raw_notes/           # Input notes
│   ├── structured_notes/    # Processed outputs
│   └── training_data/       # For ML models
├── tests/                   # Unit tests
├── docs/
│   ├── technical/           # Technical documentation
│   ├── research/            # Research notes
│   └── innovation_log/      # Patent documentation
├── notebooks/               # Jupyter notebooks for experiments
├── database/                # Database files
└── frontend/                # Web UI (future)
```

## 🚀 Quick Start

### 1. Setup Virtual Environment
```bash
# Create conda environment
conda create -n smartnotes python=3.13
conda activate smartnotes

# Or use venv
python -m venv venv
source venv/bin/activate  # On Mac/Linux
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run First Prototype
```bash
python src/note_processor/basic_processor.py
```

## 📊 Development Timeline
- **Week 1**: Foundation + Basic Note Processor ← WE ARE HERE
- **Week 2**: Note Structuring Module
- **Week 3**: Data Collection System
- **Week 4**: Knowledge Graph Basics

## 📝 Documentation
All innovations and technical decisions are documented in `docs/innovation_log/`

## 🧪 Current Status
- [x] Project structure created
- [ ] Basic NLP pipeline
- [ ] First working prototype
- [ ] Database setup
- [ ] ML model training
- [ ] Knowledge graph implementation
- [ ] Web interface

---
**Last Updated**: January 24, 2026
**Developer**: Madhuri
**Phase**: Week 1 - Foundation
