import hashlib
from core.config_manager import load_config, save_config

def hash_data(data):
    return hashlib.sha256(data.encode()).hexdigest()

def setup_credentials(password, question, answer):
    save_config({
        "password": hash_data(password),
        "question": question,
        "answer": hash_data(answer)
    })

def verify_password(password):
    return hash_data(password) == load_config()["password"]

def verify_answer(answer):
    return hash_data(answer) == load_config()["answer"]

def reset_password(new_password):
    config = load_config()
    config["password"] = hash_data(new_password)
    save_config(config)

def update_recovery(question, answer):
    config = load_config()
    config["question"] = question
    config["answer"] = hash_data(answer)
    save_config(config)