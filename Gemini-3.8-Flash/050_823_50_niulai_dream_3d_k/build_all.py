# Build complete index.html from module parts
import part1
import part2
import part3
import part4
import part5
import part6
import part7

full_html = (
    part1.part1 +
    part2.part2 +
    part3.part3 +
    part4.part4 +
    part5.part5 +
    part6.part6 +
    part7.part7
)

with open("index.html", "w") as f:
    f.write(full_html)

print(f"Successfully generated index.html (size: {len(full_html)} bytes, lines: {len(full_html.splitlines())})")
