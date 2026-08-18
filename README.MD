### 1. Generate RSA Keys
This will create `private_key.pem` and `public_key.pem` in the current directory.

```bash
python keygen.py
```

### 2. Encrypt a File
To encrypt a file, use the `encrypt` mode. By default, it uses `public_key.pem` to encrypt and outputs to `encrypted_file.bin`.

```bash
python encryptor.py encrypt <filename>
```
Example:
```bash
python encryptor.py encrypt "AMD image file.JPG"
```

### 3. Decrypt a File
Use the `decrypt` mode. By default, it uses `private_key.pem` to decrypt and outputs to `recovered_file.jpg`.

```bash
python encryptor.py decrypt <filename>
```
Example:
```bash
python encryptor.py decrypt encrypted_file.bin
```

### 4. Verify File Integrity (Checksum)
To calculate the SHA-256 hash of a file to verify its integrity:

```bash
python checksum.py <filename>
```
If no filename is provided, it defaults to `AMD image file.JPG`.

