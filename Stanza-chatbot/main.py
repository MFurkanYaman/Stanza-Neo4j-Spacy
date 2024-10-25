# main.py
import warnings
import logging

from chatbot import process_sentence, get_answer, answer
from db_operations import close_connection
from config import setup_logging


def main():
    warnings.filterwarnings("ignore")
    setup_logging()

    try:
        # Soru al
        question = "Ankara'da yemek nerede ?"
        
        # Soruyu işle
        lemma_list, node_list, doc = process_sentence(question)
        
        # Cevabı al
        db_result = get_answer(question, lemma_list, node_list)
        
        # Cevabı oluştur ve göster
        answer(db_result, question, doc)

        # Veritabanı bağlantısını kapat
        close_connection()

        logging.info("Code executed successfuly")
    except Exception as e:
        logging.error(f"On main file -> {e}")

if __name__ == "__main__":
    main()
