"""
Real Medical Dataset Loader for NeuroSmriti

Supports loading data from:
- ADNI (Alzheimer's Disease Neuroimaging Initiative)
- OASIS (Open Access Series of Imaging Studies)
- NACC (National Alzheimer's Coordinating Center)
- DementiaBank speech dataset

Data Access Instructions:
==========================

1. ADNI Dataset:
   - Website: https://adni.loni.usc.edu/
   - Requires registration and data use agreement
   - Download: MRI scans, cognitive scores, biomarkers
   - Place in: data/raw/adni/

2. OASIS Dataset:
   - Website: https://www.oasis-brains.org/
   - Free access with registration
   - OASIS-3: Longitudinal neuroimaging
   - Place in: data/raw/oasis/

3. NACC Dataset:
   - Website: https://naccdata.org/
   - Requires application and approval
   - Clinical and neuropathology data
   - Place in: data/raw/nacc/

4. DementiaBank:
   - Website: https://dementia.talkbank.org/
   - Public access to Pitt Corpus
   - Speech recordings and transcripts
   - Place in: data/raw/dementia_bank/

Data Privacy:
=============
- All data must be de-identified
- Follow HIPAA compliance requirements
- Obtain necessary IRB approvals for research use
- Never commit raw patient data to version control
"""

import os
import pandas as pd
import numpy as np
import nibabel as nib
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json
import warnings


class RealDataLoader:
    """Load and preprocess real medical datasets"""

    def __init__(self, data_root='../data/raw'):
        self.data_root = Path(data_root)
        self.adni_path = self.data_root / 'adni'
        self.oasis_path = self.data_root / 'oasis'
        self.nacc_path = self.data_root / 'nacc'
        self.dementia_bank_path = self.data_root / 'dementia_bank'

        # Create directories if they don't exist
        for path in [self.adni_path, self.oasis_path, self.nacc_path, self.dementia_bank_path]:
            path.mkdir(parents=True, exist_ok=True)

    def check_data_availability(self) -> Dict[str, bool]:
        """Check which datasets are available"""
        availability = {
            'adni': self._check_adni(),
            'oasis': self._check_oasis(),
            'nacc': self._check_nacc(),
            'dementia_bank': self._check_dementia_bank()
        }

        print("\n" + "="*70)
        print("DATASET AVAILABILITY CHECK")
        print("="*70)
        for dataset, available in availability.items():
            status = "✓ Available" if available else "✗ Not found"
            print(f"{dataset.upper():20s}: {status}")

        if not any(availability.values()):
            print("\n" + "⚠"*35)
            print("WARNING: No real datasets found!")
            print("="*70)
            print("\nTo use real clinical data, please download from:")
            print("\n1. ADNI: https://adni.loni.usc.edu/")
            print("   - Requires registration and data use agreement")
            print("   - Place files in: data/raw/adni/")
            print("\n2. OASIS: https://www.oasis-brains.org/")
            print("   - Free access with registration")
            print("   - Place files in: data/raw/oasis/")
            print("\n3. NACC: https://naccdata.org/")
            print("   - Requires application and approval")
            print("   - Place files in: data/raw/nacc/")
            print("\n4. DementiaBank: https://dementia.talkbank.org/")
            print("   - Public access")
            print("   - Place files in: data/raw/dementia_bank/")
            print("\n" + "="*70)

        return availability

    def _check_adni(self) -> bool:
        """Check if ADNI data is available"""
        # Look for common ADNI files
        expected_files = [
            'ADNIMERGE.csv',  # Main merged dataset
            'MRI_3T',  # MRI scans directory
            'PET',  # PET scans directory
        ]

        found = 0
        for file in expected_files:
            if (self.adni_path / file).exists():
                found += 1

        return found >= 1  # At least one file found

    def _check_oasis(self) -> bool:
        """Check if OASIS data is available"""
        # Look for OASIS-3 data files
        expected_dirs = [
            'scans',
            'sessions',
        ]

        csv_files = list(self.oasis_path.glob('*.csv'))

        return len(csv_files) > 0 or any((self.oasis_path / d).exists() for d in expected_dirs)

    def _check_nacc(self) -> bool:
        """Check if NACC data is available"""
        # NACC typically provides CSV files
        csv_files = list(self.nacc_path.glob('*.csv'))
        return len(csv_files) > 0

    def _check_dementia_bank(self) -> bool:
        """Check if DementiaBank data is available"""
        # Look for Pitt corpus
        pitt_path = self.dementia_bank_path / 'Pitt'
        return pitt_path.exists()

    def load_adni_data(self, subset='all') -> Optional[pd.DataFrame]:
        """
        Load ADNI dataset

        Args:
            subset: 'all', 'mri', 'cognitive', 'biomarkers'

        Returns:
            DataFrame with ADNI data or None if not available
        """
        if not self._check_adni():
            warnings.warn("ADNI data not found. Please download from https://adni.loni.usc.edu/")
            return None

        merge_file = self.adni_path / 'ADNIMERGE.csv'

        if not merge_file.exists():
            warnings.warn("ADNIMERGE.csv not found in ADNI directory")
            return None

        print("Loading ADNI data...")
        df = pd.read_csv(merge_file)

        print(f"Loaded {len(df)} records from ADNI")
        print(f"Columns: {list(df.columns[:10])}...")  # Show first 10 columns

        # Basic preprocessing
        df = self._preprocess_adni(df, subset)

        return df

    def _preprocess_adni(self, df: pd.DataFrame, subset: str) -> pd.DataFrame:
        """Preprocess ADNI data"""

        # Select relevant columns based on subset
        if subset == 'cognitive':
            # Cognitive test scores
            cols = ['PTID', 'AGE', 'PTGENDER', 'PTEDUCAT', 'DX', 'MMSE', 'MOCA',
                   'ADAS11', 'ADAS13', 'CDRSB']
        elif subset == 'mri':
            # MRI volumetry
            cols = ['PTID', 'AGE', 'DX', 'Hippocampus', 'Entorhinal', 'WholeBrain',
                   'Ventricles', 'MidTemp']
        elif subset == 'biomarkers':
            # CSF biomarkers
            cols = ['PTID', 'AGE', 'DX', 'ABETA', 'TAU', 'PTAU', 'APOE4']
        else:
            # Keep all columns
            return df

        # Select columns that exist
        available_cols = [col for col in cols if col in df.columns]

        if not available_cols:
            warnings.warn(f"No columns found for subset '{subset}'")
            return df

        df_subset = df[available_cols].copy()

        # Remove rows with all NaN values
        df_subset = df_subset.dropna(how='all')

        print(f"Preprocessing complete. Shape: {df_subset.shape}")

        return df_subset

    def load_oasis_data(self) -> Optional[pd.DataFrame]:
        """
        Load OASIS dataset

        Returns:
            DataFrame with OASIS data or None if not available
        """
        if not self._check_oasis():
            warnings.warn("OASIS data not found. Please download from https://www.oasis-brains.org/")
            return None

        print("Loading OASIS data...")

        # Look for main CSV file
        csv_files = list(self.oasis_path.glob('*.csv'))

        if not csv_files:
            warnings.warn("No CSV files found in OASIS directory")
            return None

        # Load the first CSV file (typically contains subject demographics)
        df = pd.read_csv(csv_files[0])

        print(f"Loaded {len(df)} records from OASIS")
        print(f"Columns: {list(df.columns[:10])}...")

        return df

    def load_nacc_data(self) -> Optional[pd.DataFrame]:
        """
        Load NACC dataset

        Returns:
            DataFrame with NACC data or None if not available
        """
        if not self._check_nacc():
            warnings.warn("NACC data not found. Please download from https://naccdata.org/")
            return None

        print("Loading NACC data...")

        # NACC provides multiple CSV files
        csv_files = list(self.nacc_path.glob('*.csv'))

        if not csv_files:
            warnings.warn("No CSV files found in NACC directory")
            return None

        # Load and merge NACC files
        dataframes = []
        for csv_file in csv_files:
            df = pd.read_csv(csv_file)
            dataframes.append(df)
            print(f"  Loaded {csv_file.name}: {len(df)} records")

        # If multiple files, try to merge on common ID
        if len(dataframes) > 1:
            # NACC uses NACCID as primary key
            merged_df = dataframes[0]
            for df in dataframes[1:]:
                common_cols = set(merged_df.columns) & set(df.columns)
                if 'NACCID' in common_cols:
                    merged_df = merged_df.merge(df, on='NACCID', how='outer')

            df = merged_df
        else:
            df = dataframes[0]

        print(f"Final NACC dataset: {len(df)} records")

        return df

    def load_dementia_bank_data(self) -> Optional[Dict]:
        """
        Load DementiaBank speech data

        Returns:
            Dictionary with speech data or None if not available
        """
        if not self._check_dementia_bank():
            warnings.warn("DementiaBank data not found. Download from https://dementia.talkbank.org/")
            return None

        print("Loading DementiaBank data...")

        pitt_path = self.dementia_bank_path / 'Pitt'

        # DementiaBank contains control and dementia directories
        control_path = pitt_path / 'Control'
        dementia_path = pitt_path / 'Dementia'

        data = {
            'control': [],
            'dementia': []
        }

        # Load control subjects
        if control_path.exists():
            for file in control_path.glob('**/*.cha'):  # CHAT transcript files
                data['control'].append({
                    'file': str(file),
                    'subject_id': file.stem,
                    'diagnosis': 'control'
                })

        # Load dementia subjects
        if dementia_path.exists():
            for file in dementia_path.glob('**/*.cha'):
                data['dementia'].append({
                    'file': str(file),
                    'subject_id': file.stem,
                    'diagnosis': 'dementia'
                })

        print(f"Found {len(data['control'])} control and {len(data['dementia'])} dementia transcripts")

        return data

    def create_unified_dataset(self) -> pd.DataFrame:
        """
        Create a unified dataset from all available sources

        Returns:
            DataFrame combining data from all available datasets
        """
        print("\n" + "="*70)
        print("CREATING UNIFIED DATASET FROM AVAILABLE SOURCES")
        print("="*70)

        all_data = []

        # Load ADNI
        adni_df = self.load_adni_data()
        if adni_df is not None:
            adni_df['source'] = 'ADNI'
            all_data.append(adni_df)

        # Load OASIS
        oasis_df = self.load_oasis_data()
        if oasis_df is not None:
            oasis_df['source'] = 'OASIS'
            all_data.append(oasis_df)

        # Load NACC
        nacc_df = self.load_nacc_data()
        if nacc_df is not None:
            nacc_df['source'] = 'NACC'
            all_data.append(nacc_df)

        if not all_data:
            warnings.warn("No real datasets available. Using synthetic data only.")
            return pd.DataFrame()

        # Combine datasets
        # Note: This is a simplified merge. In practice, you'd need to
        # harmonize column names and data formats across datasets
        print("\nCombining datasets...")

        # For now, just concatenate
        # TODO: Implement proper data harmonization
        combined_df = pd.concat(all_data, ignore_index=True)

        print(f"\nUnified dataset created with {len(combined_df)} records")
        print(f"Sources: {combined_df['source'].value_counts().to_dict()}")

        return combined_df


def main():
    """Demo usage of RealDataLoader"""

    loader = RealDataLoader()

    # Check what data is available
    availability = loader.check_data_availability()

    # Try to create unified dataset
    if any(availability.values()):
        unified_df = loader.create_unified_dataset()

        if not unified_df.empty:
            print("\n✓ Successfully loaded real clinical data!")
            print(f"Shape: {unified_df.shape}")
            print(f"\nSample columns: {list(unified_df.columns[:10])}")
        else:
            print("\n⚠ No data could be loaded")
    else:
        print("\n⚠ Please download real datasets to use this loader")
        print("   For now, the system will continue using synthetic data")


if __name__ == "__main__":
    main()
