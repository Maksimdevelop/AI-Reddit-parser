import os
from pathlib import Path

# Имя итогового текстового файла
OUTPUT_FILE = "project_summary.txt"

# Папки, которые нужно проигнорировать
IGNORE_DIRS = {".venv", ".git", "__pycache__", "node_modules", ".idea", ".vscode"}

# Расширения файлов, которые стоит пропустить (картинки, архивы, бинарники)
IGNORE_EXTS = {".pyc", ".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".zip", ".tar", ".gz", ".db", ".sqlite3"}


def collect_project_files(root_dir: str = "."):
    root_path = Path(root_dir).resolve()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
        # Walk обходит директории вглубь (DFS по умолчанию)
        for root, dirs, files in os.walk(root_path):
            # Модифицируем dirs "на лету", чтобы os.walk не заходил в игнорируемые папки
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith(".")]

            for file in sorted(files):
                file_path = Path(root) / file

                # Пропускаем сам итоговый файл и нетекстовые расширения
                if file_path.name == OUTPUT_FILE or file_path.suffix.lower() in IGNORE_EXTS:
                    continue

                # Относительный путь для красивого заголовка
                rel_path = file_path.relative_to(root_path)

                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as infile:
                        content = infile.read()

                    # Записываем разделитель и имя файла
                    outfile.write(f"\n{'=' * 80}\n")
                    outfile.write(f"FILE: {rel_path}\n")
                    outfile.write(f"{'=' * 80}\n\n")
                    outfile.write(content)
                    outfile.write("\n")

                    print(f"Добавлен: {rel_path}")

                except Exception as e:
                    print(f"Ошибка при чтении {rel_path}: {e}")


if __name__ == "__main__":
    collect_project_files()
    print(f"\nГотово! Весь проект собран в файл: {OUTPUT_FILE}")