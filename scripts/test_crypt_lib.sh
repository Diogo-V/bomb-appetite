
echo "Unit Testing!"
echo ""

python3 storage_service.py
python3 key_storage.py
python3 key_derivate.py
python3 encrypt_elliptic_curve.py
python3 json_storage.py


echo ""
echo "Integration Testing!"
echo ""

# alice sender
# bob receiver

python3 crypt_lib.py generate-key-pair alice_private_key_py.pem alice_public_key_py.pem

python3 crypt_lib.py generate-key-pair bob_private_key_py.pem bob_public_key_py.pem

python3 crypt_lib.py protect example_input.json example_cyphertext_py.json alice_private_key_py.pem bob_public_key_py.pem

python3 crypt_lib.py check example_cyphertext_py.json alice_private_key_py.pem bob_public_key_py.pem

python3 crypt_lib.py check example_cyphertext_py.json bob_private_key_py.pem alice_public_key_py.pem

python3 crypt_lib.py unprotect example_cyphertext_py.json example_output_py.json bob_private_key_py.pem alice_public_key_py.pem

echo "file diff: "
diff example_input.json example_output_py.json


echo ""
echo ""
echo "Unit Testing!"
echo ""

node encryptEllipticCurve.js
node keyDerivate.js
node keyStorage.js
node storageService.js
node jsonStorage.js


echo ""
echo "Integration Testing!"
echo ""

# alice sender
# bob receiver

node cryptLib.js generate-key-pair alice_private_key_js.pem alice_public_key_js.pem

node cryptLib.js generate-key-pair bob_private_key_js.pem bob_public_key_js.pem

node cryptLib.js protect example_input.json example_cyphertext_js.json alice_private_key_js.pem bob_public_key_js.pem

node cryptLib.js check example_cyphertext_js.json alice_private_key_js.pem bob_public_key_js.pem

node cryptLib.js check example_cyphertext_js.json bob_private_key_js.pem alice_public_key_js.pem

node cryptLib.js unprotect example_cyphertext_js.json example_output_js.json bob_private_key_js.pem alice_public_key_js.pem

echo "file diff: "
diff example_input.json example_output_js.json


echo ""
echo ""
echo "Integration Testing Python + JavaScript!"
echo ""

# chalie sender python
# dave receiver javascript

python3 crypt_lib.py generate-key-pair charlie_private_key.pem charlie_public_key.pem

node cryptLib.js generate-key-pair dave_private_key.pem dave_public_key.pem

python3 crypt_lib.py protect example_input.json example_cyphertext_py_2.json charlie_private_key.pem dave_public_key.pem

python3 crypt_lib.py check example_cyphertext_py_2.json charlie_private_key.pem dave_public_key.pem

python3 crypt_lib.py check example_cyphertext_py_2.json dave_private_key.pem charlie_public_key.pem

node cryptLib.js check example_cyphertext_py_2.json dave_private_key.pem charlie_public_key.pem

node cryptLib.js check example_cyphertext_py_2.json charlie_private_key.pem dave_public_key.pem

node cryptLib.js unprotect example_cyphertext_py_2.json example_output_js_2.json dave_private_key.pem charlie_public_key.pem

echo "file diff: "
diff example_input.json example_output_js_2.json


echo ""
echo ""
echo "Integration Testing JavaScript + Python!"
echo ""

# ethan sender javascript
# frank receiver python

node cryptLib.js generate-key-pair ethan_private_key.pem ethan_public_key.pem

python3 crypt_lib.py generate-key-pair frank_private_key.pem frank_public_key.pem

node cryptLib.js protect example_input.json example_cyphertext_js_2.json ethan_private_key.pem frank_public_key.pem

node cryptLib.js check example_cyphertext_js_2.json ethan_private_key.pem frank_public_key.pem

node cryptLib.js check example_cyphertext_js_2.json frank_private_key.pem ethan_public_key.pem

python3 crypt_lib.py check example_cyphertext_js_2.json frank_private_key.pem ethan_public_key.pem

python3 crypt_lib.py check example_cyphertext_js_2.json ethan_private_key.pem frank_public_key.pem

python3 crypt_lib.py unprotect example_cyphertext_js_2.json example_output_py_2.json frank_private_key.pem ethan_public_key.pem

echo "file diff: "
diff example_input.json example_output_py_2.json







