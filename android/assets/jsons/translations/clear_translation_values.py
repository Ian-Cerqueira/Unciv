
from pathlib import Path


def clean_properties(input_file):
    input_path = Path(input_file)

    output_path = input_path.with_name(
        f"{input_path.stem}_cleaned{input_path.suffix}"
    )

    with open(input_path, "r", encoding="utf-8", newline="") as f:
        lines = f.readlines()

    cleaned_lines = []

    for line in lines:
        # Separa o conteúdo da quebra de linha original
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

        if separator != -1:
            key = content[:separator]
            cleaned_lines.append(key + "=" + newline)
        else:
            cleaned_lines.append(line)

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
