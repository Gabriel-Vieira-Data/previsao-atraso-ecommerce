from pathlib import Path
import os
import shutil
import subprocess
import zipfile


DATASET_ID = "olistbr/brazilian-ecommerce"
OUTPUT_DIR = Path("data/raw/olist")
ZIP_PATH = OUTPUT_DIR / "brazilian-ecommerce.zip"


def run_command(command: list[str], description: str) -> subprocess.CompletedProcess[str]:
    print(description)
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"{description} falhou.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    return result


def download_with_kaggle_cli() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()

    command = ["kaggle", "datasets", "download", "-d", DATASET_ID, "-p", str(OUTPUT_DIR)]
    print("Baixando dataset via Kaggle CLI...")
    env = os.environ.copy()
    env["KAGGLE_DISABLE_SSL_VERIFICATION"] = "1"

    result = subprocess.run(command, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        print("Falha inicial do Kaggle CLI. Tentando fallback com SSL desativado...")
        result = subprocess.run(command, capture_output=True, text=True, env=env)

    if result.returncode != 0:
        raise RuntimeError(
            f"Falha no download do Kaggle CLI.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )

    if not ZIP_PATH.exists():
        raise FileNotFoundError(f"Arquivo zip não encontrado em {ZIP_PATH}")

    with zipfile.ZipFile(ZIP_PATH, "r") as archive:
        archive.extractall(OUTPUT_DIR)

    ZIP_PATH.unlink(missing_ok=True)

    print(f"Arquivos salvos em: {OUTPUT_DIR}")
    print("Conteúdo encontrado:")
    for path in sorted(OUTPUT_DIR.iterdir()):
        print(f"- {path.name}")


def download_with_kagglehub() -> None:
    try:
        import kagglehub
    except ImportError as exc:
        raise RuntimeError("kagglehub não está instalado. Rode: python -m pip install kaggle") from exc

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    dataset_path = kagglehub.dataset_download(DATASET_ID)
    source_dir = Path(dataset_path)

    for item in source_dir.iterdir():
        target = OUTPUT_DIR / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        else:
            shutil.copy2(item, target)

    print(f"Arquivos salvos em: {OUTPUT_DIR}")


def main() -> None:
    print(f"Destino do download: {OUTPUT_DIR.resolve()}")

    try:
        subprocess.run(["kaggle", "--version"], check=True, capture_output=True, text=True)
        download_with_kaggle_cli()
    except FileNotFoundError:
        print("Kaggle CLI não encontrado. Tentando kagglehub...")
        download_with_kagglehub()
    except subprocess.CalledProcessError as exc:
        print("O Kaggle CLI está instalado, mas o comando falhou.")
        print(exc.stderr)
        raise
    except Exception as exc:
        print("Não foi possível baixar o dataset automaticamente.")
        print("Passos manuais:")
        print("1. Crie uma conta no Kaggle e gere uma API token.")
        print("2. Coloque o arquivo kaggle.json em %USERPROFILE%\\.kaggle\\kaggle.json")
        print("3. Rode: python -m pip install kaggle")
        print("4. Rode: kaggle datasets download -d olistbr/brazilian-ecommerce -p data/raw/olist")
        print(f"Erro detalhado: {exc}")
        raise


if __name__ == "__main__":
    main()
