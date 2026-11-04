
from pathlib import Path


# Chaves cujos valores devem ser preservados
PRESERVED_KEYS = {
    "Fastlane_short_description ",
    "Fastlane_full_description "
}


def clean_properties(input_file):
    input_path = Path(input_file)

    output_path = input_path.with_name(
        f"{input_path.stem}_cleaned{input_path.suffix}"
    )

    with open(input_path, "r", encoding="utf-8", newline="") as f:
        lines = f.readlines()

    cleaned_lines = []

    for line in lines:
        content = line.rstrip("\r\n")
        newline = line[len(content):]

        stripped = content.lstrip()

        # Preserva comentários e linhas vazias
        if not stripped or stripped.startswith(("#", "!")):
            cleaned_lines.append(line)
            continue

        # Procura o primeiro '=' não escapado
        escaped = False
        separator = -1

        for i, char in enumerate(content):
            if char == "\\" and not escaped:
                escaped = True
                continue

            if char == "=" and not escaped:
                separator = i
                break

            escaped = False

        if separator == -1:
            cleaned_lines.append(line)
            continue

        key = content[:separator]

        # Preserva integralmente as linhas das chaves protegidas
        if key in PRESERVED_KEYS:
            cleaned_lines.append(line)
        else:
            cleaned_lines.append(key + "=" + newline)

    with open(output_path, "w", encoding="utf-8", newline="") as f:
        f.writelines(cleaned_lines)

    print(f"Gerado: {output_path}")


def main():
    folder = Path(".")

    for file in folder.glob("*.properties"):
        if file.stem.endswith("_cleaned"):
            continue

        clean_properties(file)


if __name__ == "__main__":
    main()
