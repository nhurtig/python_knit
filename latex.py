from abc import ABC, abstractmethod

import subprocess
import os
from typing import Optional, Sequence
from category.object import PrimitiveObject

class Latex(ABC):
    @abstractmethod
    def to_latex(self, x: int, y: int, context: Sequence[PrimitiveObject]) -> str:
        pass

    @abstractmethod
    def latex_height(self) -> int:
        pass

    @abstractmethod
    def context_out(self, context: Sequence[PrimitiveObject]) -> Sequence[PrimitiveObject]:
        pass

    def compile_latex(self, filename: str, context: Optional[Sequence[PrimitiveObject]]=None, cleanup: bool=True) -> None:
        """Compiles the LaTeX code from to_latex, writes it to a file, and converts it to PDF.

        Args:
            filename (str): The name of the file to write the LaTeX code to (without extension).
        """
        if context is None:
            context = []
        # Create the figs/ directory if it doesn't exist
        figs_directory = 'figs'
        os.makedirs(figs_directory, exist_ok=True)

        # Generate the LaTeX code
        latex_code = self.to_latex(0, 0, context)

        # Write the LaTeX code to a .tex file in the figs/ directory
        tex_filename = os.path.join(figs_directory, f"{filename}.tex")
        with open(tex_filename, 'w', encoding="utf-8") as file:
            file.write("""\\documentclass{standalone}
\\usepackage{knit}
\\begin{document}
\\begin{knitdiagram}
""")
            file.write(latex_code)
            file.write("""\\end{knitdiagram}
\\end{document}
""")

        # Compile the .tex file to generate a .pdf in the figs/ directory
        try:
            subprocess.run(['pdflatex', f"{filename}.tex"], check=True, cwd=figs_directory)
            subprocess.run(['convert', "-density", "1200", f"{filename}.pdf", f"png/{filename}.png"], check=True, cwd=figs_directory)
        finally:
            # Clean up auxiliary files generated by pdflatex in the figs/ directory
            for ext in ['aux', 'log', 'tex']:
                if not cleanup and ext == 'tex':
                    continue
                aux_file = os.path.join(figs_directory, f"{filename}.{ext}")
                if os.path.exists(aux_file):
                    os.remove(aux_file)

        print(f"Successfully created {os.path.join(figs_directory, f'{filename}.pdf')}")
