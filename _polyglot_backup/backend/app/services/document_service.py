"""
Document Translation Service
Parses structured files (.txt, .md, .json, .csv), translates text content
while preserving formatting, markup tags, and key structures.
"""
import json
import csv
import io
import re
from typing import Dict, Any, List
from .translation_service import translation_service

class DocumentService:
    def translate_document(self, content: str, filename: str, doc_format: str, source_lang: str, target_lang: str) -> Dict[str, Any]:
        """Translates document content according to format."""
        doc_format = doc_format.lower().strip('.')

        if doc_format == "json":
            return self._translate_json(content, filename, source_lang, target_lang)
        elif doc_format == "csv":
            return self._translate_csv(content, filename, source_lang, target_lang)
        elif doc_format in ["md", "markdown"]:
            return self._translate_markdown(content, filename, source_lang, target_lang)
        else:
            return self._translate_plaintext(content, filename, source_lang, target_lang)

    def _translate_plaintext(self, content: str, filename: str, source_lang: str, target_lang: str) -> Dict[str, Any]:
        lines = content.splitlines()
        translated_lines = []
        for line in lines:
            if not line.strip():
                translated_lines.append("")
                continue
            res = translation_service.translate(line, source_lang=source_lang, target_lang=target_lang, include_back_translation=False)
            translated_lines.append(res["translated_text"])
            
        translated_content = "\n".join(translated_lines)
        return {
            "filename": filename,
            "format": "txt",
            "original_content": content,
            "translated_content": translated_content,
            "line_count": len(lines)
        }

    def _translate_markdown(self, content: str, filename: str, source_lang: str, target_lang: str) -> Dict[str, Any]:
        lines = content.splitlines()
        translated_lines = []
        in_code_block = False

        for line in lines:
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                translated_lines.append(line)
                continue

            if in_code_block or not line.strip():
                translated_lines.append(line)
                continue

            # Preserve markdown headers
            header_match = re.match(r'^(#+\s*)(.*)', line)
            list_match = re.match(r'^(\s*[-*+]\s+)(.*)', line)
            num_match = re.match(r'^(\s*\d+\.\s+)(.*)', line)

            prefix = ""
            text_to_trans = line
            if header_match:
                prefix = header_match.group(1)
                text_to_trans = header_match.group(2)
            elif list_match:
                prefix = list_match.group(1)
                text_to_trans = list_match.group(2)
            elif num_match:
                prefix = num_match.group(1)
                text_to_trans = num_match.group(2)

            res = translation_service.translate(text_to_trans, source_lang=source_lang, target_lang=target_lang, include_back_translation=False)
            translated_lines.append(f"{prefix}{res['translated_text']}")

        return {
            "filename": filename,
            "format": "md",
            "original_content": content,
            "translated_content": "\n".join(translated_lines),
            "line_count": len(lines)
        }

    def _translate_json(self, content: str, filename: str, source_lang: str, target_lang: str) -> Dict[str, Any]:
        try:
            data = json.loads(content)
        except Exception:
            # Fallback to plaintext if invalid JSON
            return self._translate_plaintext(content, filename, source_lang, target_lang)

        def translate_node(node):
            if isinstance(node, dict):
                return {k: translate_node(v) for k, v in node.items()}
            elif isinstance(node, list):
                return [translate_node(item) for item in node]
            elif isinstance(node, str) and node.strip():
                res = translation_service.translate(node, source_lang=source_lang, target_lang=target_lang, include_back_translation=False)
                return res["translated_text"]
            else:
                return node

        translated_data = translate_node(data)
        translated_content = json.dumps(translated_data, indent=2, ensure_ascii=False)

        return {
            "filename": filename,
            "format": "json",
            "original_content": content,
            "translated_content": translated_content,
            "line_count": len(content.splitlines())
        }

    def _translate_csv(self, content: str, filename: str, source_lang: str, target_lang: str) -> Dict[str, Any]:
        f_in = io.StringIO(content.strip())
        reader = list(csv.reader(f_in))
        if not reader:
            return self._translate_plaintext(content, filename, source_lang, target_lang)

        f_out = io.StringIO()
        writer = csv.writer(f_out)

        # Header kept as is or translated
        header = reader[0]
        writer.writerow(header)

        for row in reader[1:]:
            new_row = []
            for cell in row:
                if cell.strip() and not cell.isnumeric():
                    res = translation_service.translate(cell, source_lang=source_lang, target_lang=target_lang, include_back_translation=False)
                    new_row.append(res["translated_text"])
                else:
                    new_row.append(cell)
            writer.writerow(new_row)

        return {
            "filename": filename,
            "format": "csv",
            "original_content": content,
            "translated_content": f_out.getvalue(),
            "line_count": len(reader)
        }

document_service = DocumentService()
