# WHO PEN Clinical RAG — دليل سريع بالعربي

هذا الريبو يحتوي النسخة النظيفة الجاهزة للـGitHub من مشروع **Production-Oriented Medical RAG** المبني على دليل WHO PEN.

## أهم نقطة قبل الرفع

الـPDF الأصلي غير موجود داخل الريبو عمدًا، والـAPI Keys غير موجودة نهائيًا.

لتشغيل المشروع على Colab:

1. ضع `9789290226666-eng.pdf` داخل:
   `MyDrive/WHO_PEN_RAG/`
2. افتح:
   `notebooks/WHO_PEN_Production_Clinical_RAG_v7_ProductionGUI.ipynb`
3. عرّف:
   - `LLM_BASE_URL`
   - `LLM_API_KEY`
   - `LLM_MODEL`
   - `VERIFIER_MODEL`
4. شغل النوتبوك من البداية.
5. في النهاية شغل واجهة Gradio.

## حالة المشروع

الـRetrieval والـEvidence Pack تم تقييمهم، لكن الـRAGAS النهائي والـheld-out clinician-reviewed evaluation ما زالوا مطلوبين قبل وصف النظام بأنه clinically production-approved.

للتفاصيل الكاملة راجع:
`docs/WHO_PEN_Production_Grade_Medical_RAG_Technical_Guide_AR.pdf`
