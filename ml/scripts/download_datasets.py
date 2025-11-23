"""
Download real Alzheimer's datasets from public sources
"""

import os
import requests
import zipfile
import kaggle
from pathlib import Path
import gdown
from tqdm import tqdm

# Setup paths
DATA_DIR = Path(__file__).parent.parent / "data"
RAW_DIR = DATA_DIR / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

print("🧠 NeuroSmriti - Dataset Downloader")
print("=" * 60)


def download_hackathon_dataset():
    """Download Hack4Health provided dataset"""
    print("\n📥 Downloading Hack4Health Dataset...")

    # Google Drive folder ID from the link
    folder_url = "https://drive.google.com/drive/folders/1jGfWOHuA3kSbOQ4y26TI_ogBtDetw1SW"

    print(f"Dataset URL: {folder_url}")
    print("\n⚠️  Manual Download Required:")
    print("1. Open the URL above in your browser")
    print("2. Download all files to: ml/data/raw/hackathon/")
    print("3. Come back and press Enter when done")

    input("\nPress Enter after you've downloaded the files...")

    hackathon_dir = RAW_DIR / "hackathon"
    if hackathon_dir.exists() and any(hackathon_dir.iterdir()):
        print("✅ Hack4Health dataset found!")
        return True
    else:
        print("❌ Files not found. Please download manually.")
        return False


def download_kaggle_dataset():
    """Download Kaggle Alzheimer's dataset"""
    print("\n📥 Downloading Kaggle Alzheimer's Dataset...")

    try:
        # Requires: pip install kaggle
        # And kaggle.json in ~/.kaggle/ or set KAGGLE_USERNAME and KAGGLE_KEY

        print("Checking Kaggle credentials...")
        kaggle.api.authenticate()

        # Download Alzheimer's 4-class dataset
        dataset_name = "tourist55/alzheimers-dataset-4-class-of-images"
        output_dir = RAW_DIR / "kaggle_alzheimers"
        output_dir.mkdir(exist_ok=True)

        print(f"Downloading {dataset_name}...")
        kaggle.api.dataset_download_files(
            dataset_name,
            path=str(output_dir),
            unzip=True
        )

        print("✅ Kaggle dataset downloaded!")
        return True

    except Exception as e:
        print(f"⚠️  Kaggle download failed: {e}")
        print("\nTo use Kaggle API:")
        print("1. Create account at kaggle.com")
        print("2. Go to Account → API → Create New API Token")
        print("3. Place kaggle.json in ~/.kaggle/")
        print("4. Run: chmod 600 ~/.kaggle/kaggle.json")
        return False


def download_oasis_sample():
    """Download OASIS sample dataset (smaller subset)"""
    print("\n📥 Downloading OASIS Sample Dataset...")

    # Note: Full OASIS requires registration, here's a public sample
    oasis_dir = RAW_DIR / "oasis"
    oasis_dir.mkdir(exist_ok=True)

    print("⚠️  OASIS Full Dataset Requires Registration:")
    print("1. Visit: https://www.oasis-brains.org/")
    print("2. Register for free account")
    print("3. Download OASIS-1 (cross-sectional dataset)")
    print("4. Extract to: ml/data/raw/oasis/")

    print("\n💡 For hackathon, you can use synthetic data or Kaggle dataset!")
    return True


def download_sample_mri():
    """Download sample MRI scans for testing"""
    print("\n📥 Downloading Sample MRI Images...")

    sample_dir = RAW_DIR / "samples"
    sample_dir.mkdir(exist_ok=True)

    # These are public domain sample brain MRIs
    sample_urls = [
        "https://github.com/matterport/Mask_RCNN/raw/master/images/brain_mri.jpg",
    ]

    for i, url in enumerate(sample_urls):
        try:
            print(f"Downloading sample {i+1}...")
            response = requests.get(url, stream=True)
            filename = sample_dir / f"sample_mri_{i+1}.jpg"

            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"✅ Saved: {filename}")
        except Exception as e:
            print(f"⚠️  Failed to download sample {i+1}: {e}")

    return True


def create_data_summary():
    """Create summary of downloaded datasets"""
    print("\n" + "=" * 60)
    print("📊 Dataset Summary")
    print("=" * 60)

    datasets = {
        "Hack4Health": RAW_DIR / "hackathon",
        "Kaggle": RAW_DIR / "kaggle_alzheimers",
        "OASIS": RAW_DIR / "oasis",
        "Samples": RAW_DIR / "samples",
        "Synthetic": DATA_DIR / "synthetic"
    }

    for name, path in datasets.items():
        if path.exists():
            file_count = len(list(path.rglob("*")))
            size_mb = sum(f.stat().st_size for f in path.rglob("*") if f.is_file()) / (1024 * 1024)
            print(f"✅ {name:15s}: {file_count:4d} files ({size_mb:.1f} MB)")
        else:
            print(f"❌ {name:15s}: Not downloaded")

    print("\n" + "=" * 60)


def main():
    """Main download orchestrator"""
    print("\nWhich datasets do you want to download?")
    print("1. Hack4Health Dataset (Recommended for hackathon)")
    print("2. Kaggle Alzheimer's Dataset (Requires Kaggle account)")
    print("3. OASIS Dataset (Requires registration)")
    print("4. Sample MRI Images (Quick test)")
    print("5. All available datasets")
    print("6. Skip - Use synthetic data only")

    choice = input("\nEnter choice (1-6): ").strip()

    if choice == "1":
        download_hackathon_dataset()
    elif choice == "2":
        download_kaggle_dataset()
    elif choice == "3":
        download_oasis_sample()
    elif choice == "4":
        download_sample_mri()
    elif choice == "5":
        download_hackathon_dataset()
        download_kaggle_dataset()
        download_oasis_sample()
        download_sample_mri()
    elif choice == "6":
        print("\n✅ Will use synthetic data only (fine for hackathon!)")
    else:
        print("Invalid choice. Using synthetic data only.")

    create_data_summary()

    print("\n" + "=" * 60)
    print("🎉 Setup Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Run: jupyter notebook notebooks/02_data_preprocessing.ipynb")
    print("2. Or run: python scripts/train_memory_gnn.py")
    print("\n💡 Tip: Synthetic data works great for hackathons!")


if __name__ == "__main__":
    main()
