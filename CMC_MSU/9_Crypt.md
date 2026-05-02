## SSH private key recovery via RSA modulus collision

**Attack name:** GCD factorization – shared prime due to low entropy

We are given 1000 public SSH keys (RSA) generated on a machine with low entropy.  
Because of this, some keys may share a common prime factor, allowing us to factor the modulus and recover the private key.  
Goal: SSH access to a machine on the network.

---

### Background

RSA modulus: `n = p * q`, where `p` and `q` are large primes.  
If two different moduli `n1` and `n2` share a common factor `p`, then:

```
gcd(n1, n2) = p
```

Once we have `p`, we compute `q = n1 / p`, then `φ = (p-1)*(q-1)`, and finally the private exponent `d = e^(-1) mod φ`.  
With these parameters we can generate a private key in PEM format.

---

### Steps

**1. Prepare the data**  
Public keys are in the folder `keys/`, named `id_rsa_0` … `id_rsa_999`.  
Each file contains one line in OpenSSH format, e.g.:

```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQD...
```

**2. Extract moduli and exponents**  
Write a Python script that:
- Reads all files
- Parses each public key to extract `n` (modulus) and `e` (exponent)
- Stores them in a list

**3. Find collisions**  
Compute GCD for every pair. If `gcd > 1`, a collision is found.

**4. Recover the private key**  
For the colliding pair:
```
p = gcd(n1, n2)
q = n1 // p
φ = (p-1)*(q-1)
d = pow(e, -1, φ)
```
Then assemble the private key in PKCS#1 PEM format.

**5. SSH connection**  
Use the recovered private key to log into the target host.

---

**4. Connect via SSH**
```bash
ssh -i private_key.pem user@target_host
```

> [!NOTE]
> This attack works when the random number generator is weak, causing repeated primes.  
> It is also known as the "GCD attack" or "common prime factor attack".
