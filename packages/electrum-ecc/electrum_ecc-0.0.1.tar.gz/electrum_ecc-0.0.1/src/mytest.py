import electrum_ecc as ecc


ecc_pk1 = ecc.ECPrivkey(32*b'\x01')
ecc_pk2 = ecc.ECPrivkey(32*b'\x02')
ecc_pubkey1 = ecc.ECPubkey(ecc_pk1.get_public_key_bytes(compressed=True))
ecc_pubkey2 = ecc.ECPubkey(ecc_pk2.get_public_key_bytes(compressed=True))

print(ecc_pubkey1)
print(ecc_pubkey2)

print(ecc_pk1.ecdh(ecc_pubkey2, hashfn=ecc.HASHFN_COPY_X))
print(ecc_pk2.ecdh(ecc_pubkey1, hashfn=ecc.HASHFN_COPY_X))
