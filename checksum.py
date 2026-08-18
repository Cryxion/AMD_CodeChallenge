import hashlib

def hash_file(filename):
    sha256_hash = hashlib.sha256()
    try:
        with open(filename, "rb") as f: # Open the file in binary read mode
            # Read and update the hash object in chunks of 4KB to save memory
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block) 
        
        print(f"SHA-256 Hash of {filename}:")
        print(sha256_hash.hexdigest()) 
    except FileNotFoundError:
        print(f"Error: {filename} not found")

if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "AMD image file.JPG"
    hash_file(target) 
