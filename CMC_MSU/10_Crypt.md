## Broadcast attack on RSA with small public exponent

### Hm...
- Multiple ciphertexts encrypted with different moduli `n_i` but the same small exponent `e`
- The same plaintext `m` was sent to several recipients
- If the number of ciphertexts ≥ `e`, we can recover `m` without the private key

### Solution

**1. Extract public keys**
From `*.pub.pem` files, obtain moduli `n_i` and exponent `e`

**2. Read ciphertexts**
Read `*.enc` files as binary and convert to integers `c_i`.

**3. Apply Chinese Remainder Theorem (CRT)**
Solve the system of congruences:

```
m^e ≡ c₁ (mod n₁)
m^e ≡ c₂ (mod n₂)
...
m^e ≡ cₖ (mod nₖ)   where k ≥ e
```

Get `x = m^e` as an integer.  
Since `m < n_i`, we have `m^e < ∏ n_i` → `x` is exactly `m^e`.

**4. Take the e‑th root**
Compute `m = x^(1/e)` (integer root).

**5. Convert to string**
Number → bytes → string → **flag** 🎉

> [!TIP]
> This attack works when `e` is small (e.g., 3 or 5) and you have at least `e` ciphertexts with different moduli.
