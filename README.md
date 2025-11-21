🧠 RAG APP — FULL RUN COMMANDS (START TO END)
🔥 1️⃣ Go to project folder
cd C:\Users\IAST356\Documents\rag-app

🔥 2️⃣ Activate virtual environment
.venv\Scripts\activate

🔥 3️⃣ Start Ollama (if not already running)

(if Ollama gives port error — skip this step)

ollama serve

🔥 4️⃣ Pull model (only first time)
ollama pull tinyllama

🔥 5️⃣ Put documents in folder
rag-app/data/raw/

🔥 6️⃣ Ingest documents (run ONLY when documents are changed or new ones added)
python ingest.py

🔥 7️⃣ Run the RAG interactive chat
python rag_cli_stream.py

🧪 Example flow (exact order)
cd rag-app
.venv\Scripts\activate
ollama serve
ollama pull tinyllama
python ingest.py
python rag_cli_stream.py

💬 Usage inside terminal
❓ Question: who is the md of iast in document?

Exit:

exit

⚠️ IMPORTANT NOTES
Action When to do
Run ollama serve First time only
Run ollama pull tinyllama First time only
Run python ingest.py Only when documents change
Run python rag_cli_stream.py Every time you want to chat
