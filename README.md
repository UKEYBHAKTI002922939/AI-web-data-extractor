# AI-web-data-extractor

virtual environment
pip install .e -- setup.py

python -m rufus.main --url https://ai.pydantic.dev/ --depth 2 --output output.json



challenges:
not added logging logic crawled 81 urls

python main.py --url "https://www.sfgov.com" \
               --depth 2 \
               --instructions "scrape customer FAQ's" \
               --output "sfgov_report.json"




python main.py --url "https://ai.pydantic.dev" \
               --depth 2 \
               --instructions "scrape anything related to RAG" \
               --output "pydantic_report.json"

issues with the summarizer part with sequential fetching initially
concurrent fetching
issues faced and improvement on working with 