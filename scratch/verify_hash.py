import bcrypt
hash_val = '$2b$12$LJ3m5ZQnJdGp1S5x5r5cTuO8X8Pk5JZ8YV7gN5wE2rA4bH6cK9dWu'
print(f"Checking hash for 'supplier123'...")
result = bcrypt.checkpw(b'supplier123', hash_val.encode('utf-8'))
print(f"Result: {result}")
