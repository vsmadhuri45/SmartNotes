# SmartNotes Setup Guide

## 📦 Step-by-Step Setup Instructions

### Step 1: Navigate to Your Desired Location
Open Terminal and navigate to where you want to create the project:
```bash
cd ~/Documents  # or wherever you want the project
```

### Step 2: Download Project Files
Download the SmartNotes folder (provided to you) and place it in your desired location.

### Step 3: Navigate to Project Directory
```bash
cd SmartNotes
```

### Step 4: Create Virtual Environment

**Option A: Using Conda (Recommended since you have it)**
```bash
conda create -n smartnotes python=3.13
conda activate smartnotes
```

**Option B: Using venv**
```bash
python -m venv venv
source venv/bin/activate  # On Mac
```

### Step 5: Install Dependencies
```bash
pip install -r requirements.txt
```

**Note**: This will take 5-10 minutes as it downloads all packages.

### Step 6: Download Spacy Language Model
```bash
python -m spacy download en_core_web_sm
```

### Step 7: Test Installation
Run the basic processor to make sure everything works:
```bash
python src/note_processor/basic_processor.py
```

You should see output showing a structured note!

### Step 8: Initialize Git Repository
```bash
git init
git add .
git commit -m "Initial commit: Project setup"
```

### Step 9: (Optional) Create GitHub Repository
1. Go to github.com
2. Create new repository named "SmartNotes"
3. Don't initialize with README (we already have one)
4. Copy the repository URL
5. Link your local repo:
```bash
git remote add origin YOUR_GITHUB_URL
git branch -M main
git push -u origin main
```

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Virtual environment activated
- [ ] All packages installed without errors
- [ ] Spacy model downloaded
- [ ] Basic processor runs successfully
- [ ] Git repository initialized
- [ ] Project structure visible in VS Code

---

## 🚀 What's Next?

1. **Open VS Code**:
   ```bash
   code .
   ```

2. **Explore the code**:
   - `src/note_processor/basic_processor.py` - Our first working prototype!
   - `docs/DEVELOPMENT_JOURNAL.md` - Track daily progress here
   - `docs/innovation_log/INNOVATION_LOG.md` - Document innovations here

3. **Try processing your own note**:
   - Create a text file in `data/raw_notes/`
   - Modify `basic_processor.py` to read from file
   - See the structured output!

---

## 🛠️ Troubleshooting

### Issue: "conda: command not found"
Use venv instead (Option B in Step 4)

### Issue: Package installation fails
Try installing packages one at a time to identify the problematic one:
```bash
pip install numpy pandas transformers
```

### Issue: Spacy model download fails
Try:
```bash
python -m pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.0/en_core_web_sm-3.7.0-py3-none-any.whl
```

### Issue: Import errors when running code
Make sure you're in the project root directory and virtual environment is activated.

---

## 📞 Need Help?

If you encounter issues:
1. Check that you're in the correct directory: `pwd`
2. Check virtual environment is active: you should see `(smartnotes)` or `(venv)` in your terminal
3. Check Python version: `python --version` (should be 3.13.x)

---

## 🎯 Your First Task

Once setup is complete, your first task is to:
1. Run the basic processor successfully
2. Read through the code to understand how it works
3. Update the development journal with today's progress
4. Think about how to improve the key concept extraction

Ready to build! 🚀
