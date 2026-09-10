# PDF Ingestion

Use this reference only when the primary source is a PDF. Text extraction is a convenience, not proof that the source was read faithfully.

## Read and verify

1. Inspect page count, metadata, encryption, and whether a usable text layer exists.
2. Extract text with page boundaries using available PDF tooling such as `pypdf` or `pdfplumber`. Preserve heading, paragraph, table, footnote, caption, and page relationships where possible.
3. Render pages to images and inspect them when layout carries meaning. At minimum, inspect samples across the document plus every page suspected to contain tables, figures, formulas, multi-column text, or sparse/garbled extraction.
4. If the PDF is scanned or a page's text layer is missing, use OCR or visual reading on the rendered page. For a short PDF, inspect every page. For a long PDF, first identify risky pages, but do not skip pages whose extraction is empty or anomalously sparse.
5. Compare extracted content against the rendered pages for reading order, missing regions, table relationships, captions, symbols, and qualifiers.

## Knowledge units and locators

Create semantic units only after the document's global structure is understood. Attach locators such as `p. 4, section heading`, `p. 7 table`, or `pp. 9-10 figure and discussion`. A table row, figure annotation, or footnote can be an independent knowledge unit when it changes the claim.

Keep extraction mechanics out of the main learning narrative unless they are themselves part of the subject. Put extraction method, visually recovered content, and limitations in the companion knowledge diff.

## Failure handling

Do not guess unreadable text, formulas, or diagram meaning. If an important region remains unreliable after available extraction, rendering, OCR, or visual inspection:

- identify the affected page or region;
- explain what is uncertain;
- preserve surrounding context;
- ask for a clearer source when the uncertainty would materially change the learning artifact.

Do not claim complete coverage when pages, attachments, fonts, or images could not be inspected.

## Audit fields

Record:

- PDF page count and processed range;
- text extraction method;
- pages visually inspected;
- OCR or visual recovery used;
- tables, figures, formulas, or footnotes carried into the main artifact;
- unresolved extraction limitations.

Use the source filename and page locators in the audit without exposing unnecessary absolute paths.
