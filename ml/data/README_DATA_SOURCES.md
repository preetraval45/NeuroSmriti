# Real Medical Datasets for NeuroSmriti

This document provides instructions for obtaining and using real clinical datasets for Alzheimer's disease research.

## 🚨 Important Notice

**Current Status**: NeuroSmriti models are currently trained on **synthetic data** generated from published clinical research parameters. While based on real-world studies, this is NOT real patient data.

**For Production Use**: Real clinical datasets must be obtained from authorized sources with proper data use agreements and IRB approval.

---

## Available Public Datasets

### 1. ADNI (Alzheimer's Disease Neuroimaging Initiative)

**Website**: https://adni.loni.usc.edu/

**Description**: The gold standard for Alzheimer's research data. Includes:
- Longitudinal MRI and PET scans
- Cognitive assessment scores (MMSE, ADAS-Cog, CDR)
- CSF biomarkers (Amyloid-β, Tau, P-Tau)
- Genetic data (APOE genotypes)
- Clinical diagnoses over time

**Access Requirements**:
- Free registration required
- Data Use Agreement must be signed
- Approval takes 1-2 weeks
- Suitable for academic research

**Data Files**:
- `ADNIMERGE.csv` - Main merged dataset with all key variables
- MRI scans in NIfTI format
- PET scans (FDG, Amyloid, Tau)
- FreeSurfer processed volumetry

**Setup**:
```bash
# 1. Register at https://adni.loni.usc.edu/
# 2. Sign Data Use Agreement
# 3. Download data using LONI IDA
# 4. Place files in: ml/data/raw/adni/
```

---

### 2. OASIS (Open Access Series of Imaging Studies)

**Website**: https://www.oasis-brains.org/

**Description**: Free neuroimaging dataset with three releases:
- **OASIS-1**: Cross-sectional MRI (416 subjects aged 18-96)
- **OASIS-2**: Longitudinal MRI (150 subjects, 2+ visits)
- **OASIS-3**: Longitudinal multimodal neuroimaging (1,000+ subjects)

**Data Included**:
- T1-weighted MRI scans
- FreeSurfer processed brain volumes
- Clinical Dementia Rating (CDR)
- Cognitive assessments

**Access Requirements**:
- Free registration
- Immediate access after registration
- Open to researchers worldwide

**Setup**:
```bash
# 1. Register at https://www.oasis-brains.org/
# 2. Download OASIS-3 (most comprehensive)
# 3. Place files in: ml/data/raw/oasis/
```

---

### 3. NACC (National Alzheimer's Coordinating Center)

**Website**: https://naccdata.org/

**Description**: Uniform Data Set (UDS) from 30+ Alzheimer's Disease Research Centers:
- Clinical evaluations
- Neuropsychological test batteries
- Neuropathology data
- Diverse demographic representation

**Data Included**:
- Comprehensive cognitive assessments
- Medical history
- Medications
- Clinical diagnoses
- Neuropathology (autopsy data)

**Access Requirements**:
- Research proposal required
- Institutional review
- Approval process: 4-8 weeks
- Academic/research institutions only

**Setup**:
```bash
# 1. Submit research proposal at https://naccdata.org/
# 2. Wait for approval
# 3. Download CSV files
# 4. Place files in: ml/data/raw/nacc/
```

---

### 4. DementiaBank

**Website**: https://dementia.talkbank.org/

**Description**: Pitt Corpus - speech recordings for language analysis:
- Audio recordings of Cookie Theft picture description
- Transcripts with linguistic annotations
- Control and Alzheimer's patient groups
- Publicly accessible

**Data Included**:
- Audio files (.mp3, .wav)
- CHAT transcripts (.cha)
- Demographic information
- CDR ratings

**Access Requirements**:
- Publicly accessible
- No registration required
- Citation required in publications

**Setup**:
```bash
# 1. Download Pitt Corpus from https://dementia.talkbank.org/
# 2. Extract to: ml/data/raw/dementia_bank/
```

---

### 5. UK Biobank

**Website**: https://www.ukbiobank.ac.uk/

**Description**: Large-scale biomedical database with neuroimaging:
- 500,000+ participants
- Brain MRI scans (100,000+ participants)
- Genetic data
- Cognitive assessments
- Health outcomes

**Access Requirements**:
- Research proposal required
- Application fee (~£3,500-6,000)
- Approval process: 2-3 months
- Institutional sponsorship required

**Not Included in Default Setup** (due to access restrictions)

---

### 6. AIBL (Australian Imaging, Biomarker & Lifestyle)

**Website**: https://aibl.csiro.au/

**Description**: Longitudinal study of aging and Alzheimer's:
- MRI and PET imaging
- Blood-based biomarkers
- Cognitive assessments
- Lifestyle factors

**Access Requirements**:
- Application required
- Approval process
- Collaborative research encouraged

---

## Data Structure

Once downloaded, organize data as follows:

```
ml/data/raw/
├── adni/
│   ├── ADNIMERGE.csv
│   ├── MRI_3T/
│   ├── PET/
│   └── biomarkers/
├── oasis/
│   ├── scans/
│   └── oasis3_demographics.csv
├── nacc/
│   ├── investigator_nacc.csv
│   └── clinical_data.csv
└── dementia_bank/
    └── Pitt/
        ├── Control/
        └── Dementia/
```

---

## Usage

### Check Available Data

```python
from ml.data.real_data_loader import RealDataLoader

loader = RealDataLoader()
availability = loader.check_data_availability()
```

### Load ADNI Data

```python
# Load all ADNI data
df = loader.load_adni_data(subset='all')

# Load specific subset
cognitive_df = loader.load_adni_data(subset='cognitive')
mri_df = loader.load_adni_data(subset='mri')
biomarkers_df = loader.load_adni_data(subset='biomarkers')
```

### Load OASIS Data

```python
oasis_df = loader.load_oasis_data()
```

### Create Unified Dataset

```python
# Combine all available datasets
unified_df = loader.create_unified_dataset()
```

---

## Data Preprocessing Pipeline

For training the NeuroSmriti models with real data:

1. **Download data** from authorized sources
2. **Place files** in appropriate directories (see structure above)
3. **Run data checker**:
   ```bash
   cd ml/data
   python real_data_loader.py
   ```
4. **Preprocess and harmonize** data across sources
5. **Train with Nested CV**:
   ```bash
   cd ml/scripts
   python train_nested_cv.py
   ```

---

## Ethical Considerations

### Data Privacy

- ✓ All datasets must be de-identified
- ✓ Follow HIPAA compliance requirements
- ✓ Never commit raw patient data to version control
- ✓ Store data securely with access controls
- ✓ Use encrypted storage for sensitive data

### Research Ethics

- ✓ Obtain IRB approval for your institution
- ✓ Follow data use agreements strictly
- ✓ Cite original data sources in publications
- ✓ Share processed/aggregated data when permitted
- ✓ Report findings back to data providers

### Clinical Use

⚠️ **WARNING**: Models trained even on real data require:
- Clinical validation studies
- FDA/regulatory approval
- Healthcare professional oversight
- Continuous monitoring and updates

**Do NOT use NeuroSmriti for actual medical diagnosis without proper validation and regulatory approval.**

---

## Data Citations

If you use these datasets, please cite:

**ADNI**:
```
Data used in preparation of this article were obtained from the Alzheimer's
Disease Neuroimaging Initiative (ADNI) database (adni.loni.usc.edu). As such,
the investigators within the ADNI contributed to the design and implementation
of ADNI and/or provided data but did not participate in analysis or writing
of this report.
```

**OASIS**:
```
OASIS-3: Longitudinal Neuroimaging, Clinical, and Cognitive Dataset for
Normal Aging and Alzheimer's Disease. P LaMontagne, et al. (2019).
medRxiv. doi:10.1101/2019.12.13.19014902
```

**NACC**:
```
The NACC database is funded by NIA/NIH Grant U24 AG072122. NACC data are
contributed by the NIA-funded ADRCs: P30 AG019610, P30 AG013846, P50 AG008702...
[See full citation list at naccdata.org]
```

**DementiaBank**:
```
Becker, J., Boiler, F., Lopez, O., Saxton, J., & McGonigle, K. (1994).
The natural history of Alzheimer's disease: Description of study cohort
and accuracy of diagnosis. Archives of Neurology, 51, 585-594.
```

---

## Synthetic Data (Current Default)

**Location**: `ml/data/generate_large_dataset.py`

The current system uses synthetic data generated based on clinical research parameters from the above datasets. This synthetic data:

✓ Reflects realistic distributions from published research
✓ Maintains clinical plausibility
✓ Enables development without data access restrictions
✗ **NOT suitable for clinical deployment**
✗ **NOT validated against real patients**

For production use, **real data is required**.

---

## Support

For questions about data access:
- ADNI: adni@loni.usc.edu
- OASIS: oasis@wustl.edu
- NACC: naccmail@uw.edu
- DementiaBank: talkbank@talkbank.org

For NeuroSmriti data integration questions:
- Open an issue on GitHub
- Contact the development team

---

## Updates

This document was last updated: **December 2024**

Data access requirements and procedures may change. Always check the official websites for current information.
