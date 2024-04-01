import bitcoin
import binascii
import time 
import multiprocessing

CHUNKS = 2
MIN = 0x8000
MAX = 0xffff
WALLETS = '1BDyrQ6WoF8VN3g9SAS1iKZcPzFfnDVieY'

def time_delay(funcao):
    def wrapper(*args, **kwargs):
        inicio = time.time()
        funcao(*args, **kwargs)
        fim = time.time() - inicio
        print(f"Time: {fim:.2f}s")
        return 
    return wrapper

def generatePublic(privateKey):
    _key = bitcoin.encode_privkey(binascii.unhexlify(privateKey), 'wif_compressed')
    return bitcoin.pubkey_to_address(bitcoin.privkey_to_pubkey(_key))

   
def run_bf(start, end, found_event):
    key = start
    running= key < end
    results = []

    while running:
        if found_event.is_set():
            break

        pkey = hex(key)[2:].zfill(64) # format hexadecimal
        public = generatePublic(pkey)

        if public == WALLETS:
            print(f"Encontrado! => {pkey}")
            print(f"Foram geradas: {key - start} hash")
            results.append(pkey)
            found_event.set()
            running = False

        key += 1

    return results

@time_delay
def main():
    manager = multiprocessing.Manager()
    found_event = manager.Event()
    
    chunk_size = (MAX - MIN) // CHUNKS
    pool = multiprocessing.Pool(processes=CHUNKS)

    for i in range(CHUNKS):
        start = MIN + i * chunk_size
        end = start + chunk_size if i < CHUNKS - 1 else MAX
        print(f"[{i}] {start} - {end}")
        pool.apply_async(run_bf, args=(start, end, found_event))

    pool.close()
    pool.join()
    

if __name__ == "__main__":
    main()