from pathlib import Path


def find_separator(content):
    """Encontra o primeiro '=' não escapado."""
    escaped = False

    for i, char in enumerate(content):
        if char == "\\" and not escaped:
            escaped = True
            continue

        if char == "=" and not escaped:
            return i

        escaped = False

    return -1


def clean_properties(input_file):
    input_path = Path(input_file)

    output_path = input_path.with_name(
        f"{input_path.stem}_cleaned{input_path.suffix}"
    )

    with open(input_path, "r", encoding="utf-8", newline="") as f:
        lines = f.readlines()

    cleaned_lines = []
    inside_fastlane = False

    for line in lines:
        content = line.rstrip("\r\n")
        newline = line[len(content):]
        stripped = content.strip()

        # Identifica o início da seção Fastlane
        if stripped.lower() == "# fastlane":
            inside_fastlane = True
            continue

        # Remove o marcador de tradução
        if stripped == "# Require translation !":
            continue

        # Preserva comentários e linhas vazias fora de Fastlane
        if not stripped or stripped.startswith(("#", "!")):
            if not inside_fastlane:
                cleaned_lines.append(line)
            continue

        separator = find_separator(content)

        if separator == -1:
            if not inside_fastlane:
                cleaned_lines.append(line)
            continue

        key = content[:separator].strip()

        # Remove as chaves Fastlane e seus valores
        if key.startswith("Fastlane_"):
            continue

        # Ao encontrar uma chave não Fastlane, encerra a seção
        # e volta a processar normalmente o restante do arquivo.
        inside_fastlane = False

        # Preserva a chave e limpa seu valor
        cleaned_lines.append(content[:separator] + "=" + newline)

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