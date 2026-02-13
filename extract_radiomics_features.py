import os
import glob
import csv
import argparse
import pandas as pd
from radiomics import featureextractor


# ==============================
# ARGPARSE
# ==============================

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Estrazione feature radiomiche da immagini CT e maschere polmonari"
    )

    parser.add_argument(
        "--data_path",
        type=str,
        required=True,
        help="Cartella contenente immagini CT (.nii.gz)"
    )

    parser.add_argument(
        "--mask_path",
        type=str,
        required=True,
        help="Cartella contenente maschere polmonari (_Lung.nii.gz)"
    )

    parser.add_argument(
        "--param_file",
        type=str,
        required=True,
        help="File YAML con parametri PyRadiomics"
    )

    parser.add_argument(
        "--output_dir",
        type=str,
        default="Features",
        help="Cartella di output per feature individuali"
    )

    parser.add_argument(
        "--total_csv",
        type=str,
        default="Total_features.csv",
        help="Nome file CSV finale"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Stampa dettagli configurazione extractor"
    )

    return parser.parse_args()


# ==============================
# FUNZIONI
# ==============================

def get_sorted_files(data_path, mask_path):
    images = glob.glob(os.path.join(data_path, "*.nii.gz"))
    masks = glob.glob(os.path.join(mask_path, "*_Lung.nii.gz"))

    images.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))
    masks.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))

    if len(images) != len(masks):
        raise ValueError("Numero immagini diverso dal numero maschere.")

    return images, masks


def extract_features(images, masks, extractor, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    all_results = []

    for i, (image_path, mask_path) in enumerate(zip(images, masks)):
        print(f"\n[{i+1}/{len(images)}] Estrazione feature")
        print("Image:", image_path)
        print("Mask:", mask_path)

        try:
            result = extractor.execute(image_path, mask_path)
            result["image_ID"] = os.path.basename(image_path)
            all_results.append(result)

            numeric_id = os.path.basename(image_path).replace(".nii.gz", "").split("-")[-1]

            df_single = pd.DataFrame({
                "feature": list(result.keys()),
                f"value_{numeric_id}": list(result.values())
            })

            df_single.to_csv(
                os.path.join(output_dir, f"features_{numeric_id}.csv"),
                index=False
            )

            print("Completato.")

        except Exception as e:
            print(f"Errore su {image_path}: {e}")

    return all_results


def save_total_csv(all_results, total_csv):
    if not all_results:
        print("Nessun risultato da salvare.")
        return

    csv_columns = list(all_results[0].keys())

    with open(total_csv, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns, extrasaction="ignore")
        writer.writeheader()
        for data in all_results:
            writer.writerow(data)

    print(f"\nFile totale salvato: {total_csv}")


# ==============================
# MAIN
# ==============================

def main():
    args = parse_arguments()

    print("Inizializzazione Radiomics Extractor...")
    extractor = featureextractor.RadiomicsFeatureExtractor(args.param_file)

    if args.verbose:
        print("\nExtraction parameters:\n", extractor.settings)
        print("\nEnabled filters:\n", extractor.enabledImagetypes)
        print("\nEnabled features:\n", extractor.enabledFeatures)

    images, masks = get_sorted_files(args.data_path, args.mask_path)

    print("\nImmagini trovate:", len(images))
    print("Maschere trovate:", len(masks))

    all_results = extract_features(images, masks, extractor, args.output_dir)

    save_total_csv(all_results, args.total_csv)

    print("\nPipeline completata.")


if __name__ == "__main__":
    main()